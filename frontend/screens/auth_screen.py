from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button as MDRaisedButton, Button as MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.metrics import dp
import re
from utils.email_service import EmailService

class AuthScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[40, 40, 40, 40],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # App title
        title = MDLabel(
            text="TravelMate",
            theme_text_color="Primary",
            size_hint_y=None,
            height=60,
            font_style="H3"
        )
        main_layout.add_widget(title)
        
        subtitle = MDLabel(
            text="Your Personal Vacation Planner",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=40,
            font_style="Subtitle1"
        )
        main_layout.add_widget(subtitle)
        
        # Login form
        self.email_field = MDTextField(
            hint_text="Email",
            helper_text="We'll never share your email.",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60,
            icon_left="email"
        )
        main_layout.add_widget(self.email_field)
        
        self.password_field = MDTextField(
            hint_text="Password",
            helper_text="Minimum 6 characters",
            helper_text_mode="on_focus",
            password=True,
            size_hint_y=None,
            height=60,
            icon_left="lock"
        )
        main_layout.add_widget(self.password_field)

        # Show/Hide password toggle icon
        def toggle_pw(*_):
            self.password_field.password = not self.password_field.password
        pw_toggle = MDIconButton(icon="eye-off", on_release=toggle_pw)
        self.password_field.right_widget = pw_toggle
        
        # Login button
        login_btn = MDRaisedButton(
            text="Login",
            size_hint_y=None,
            height=50,
            on_release=self.login
        )
        main_layout.add_widget(login_btn)
        
        # Register button
        register_btn = MDTextButton(
            text="Don't have an account? Register",
            size_hint_y=None,
            height=40,
            on_release=self.show_register_dialog
        )
        main_layout.add_widget(register_btn)
        
        self.add_widget(main_layout)
    
    def login(self, instance):
        """Handle login"""
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()
        
        if not email or not password:
            self.show_error("Please fill in all fields")
            return
        # Simple email format validation
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.show_error("Please enter a valid email address")
            return
        
        # Get app instance
        app = MDApp.get_running_app()
        
        # Show loading
        self.show_loading("Logging in...")
        
        # Make API call
        def do_login(dt):
            result, error = app.api_client.login(email, password)
            if result:
                token = result.get('access_token')
                if token:
                    # Store token before fetching /auth/me (both app and api client stores)
                    app.store.put('access_token', token=token)
                    app.api_client.store.put('access_token', token=token)
                    user_info, user_error = app.api_client.get_current_user()
                    if user_info:
                        # Check if email verification is required
                        if not EmailService().is_email_verified(email):
                            self.hide_loading()
                            self.show_email_verification_dialog(email)
                        else:
                            app.login_user(user_info, token)
                            self.hide_loading()
                    else:
                        self.hide_loading()
                        self.show_error(f"Login failed: {user_error}")
                else:
                    self.hide_loading()
                    self.show_error("Login failed: missing token")
            else:
                self.hide_loading()
                self.show_error(f"Login failed: {error}")
        
        Clock.schedule_once(do_login, 0.1)
    
    def show_email_verification_dialog(self, email):
        """Show email verification dialog"""
        app = MDApp.get_running_app()
        
        # Create content
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Email Verification Required",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # Description
        desc = MDLabel(
            text=f"We've sent a verification code to {email}",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(desc)
        
        # Verification code input
        self.verification_field = MDTextField(
            hint_text="Enter 6-digit code",
            helper_text="Check your email for the verification code",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(60),
            input_filter="int",
            max_text_length=6
        )
        content.add_widget(self.verification_field)
        
        # Resend button
        resend_btn = MDTextButton(
            text="Resend Code",
            theme_text_color="Custom",
            text_color=app.theme_cls.primary_color,
            on_release=lambda x: self.resend_verification_code(email)
        )
        content.add_widget(resend_btn)
        
        content.height = dp(200)
        
        # Create dialog
        self.verification_dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: self.verification_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Verify",
                    on_release=lambda x: self.verify_email_code(email)
                )
            ]
        )
        
        # Send initial verification code
        self.send_verification_code(email)
        self.verification_dialog.open()
    
    def send_verification_code(self, email):
        """Send verification code to email"""
        email_service = EmailService()
        code = email_service.generate_verification_code()
        success, error = email_service.send_verification_email(email, code)
        
        if not success:
            app = MDApp.get_running_app()
            app.show_error_snackbar(f"Failed to send verification code: {error}")
    
    def resend_verification_code(self, email):
        """Resend verification code"""
        self.send_verification_code(email)
        app = MDApp.get_running_app()
        app.show_success_snackbar("Verification code sent!")
    
    def verify_email_code(self, email):
        """Verify the entered code"""
        code = self.verification_field.text.strip()
        
        if not code or len(code) != 6:
            self.show_error("Please enter a valid 6-digit code")
            return
        
        email_service = EmailService()
        success, message = email_service.verify_code(email, code)
        
        if success:
            self.verification_dialog.dismiss()
            app = MDApp.get_running_app()
            app.show_success_snackbar("Email verified successfully!")
            app.go_to_dashboard()
        else:
            self.show_error(message)
    
    def show_register_dialog(self, instance):
        """Show registration dialog"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=200
        )
        
        self.reg_email_field = MDTextField(
            hint_text="Email",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.reg_email_field)
        
        self.reg_username_field = MDTextField(
            hint_text="Username",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.reg_username_field)
        
        self.reg_password_field = MDTextField(
            hint_text="Password",
            password=True,
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.reg_password_field)
        
        self.register_dialog = MDDialog(
            title="Create Account",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.register_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Register",
                    on_release=self.register
                )
            ]
        )
        self.register_dialog.open()
    
    def register(self, instance):
        """Handle registration"""
        email = self.reg_email_field.text.strip()
        username = self.reg_username_field.text.strip()
        password = self.reg_password_field.text.strip()
        
        if not email or not username or not password:
            self.show_error("Please fill in all fields")
            return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.show_error("Please enter a valid email address")
            return
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return
        
        # Get app instance
        app = MDApp.get_running_app()
        
        # Show loading
        self.show_loading("Creating account...")
        
        # Make API call
        def do_register(dt):
            result, error = app.api_client.register(email, username, password)
            if result:
                token = result.get('access_token')
                if token:
                    # Store token before fetching /auth/me (both app and api client stores)
                    app.store.put('access_token', token=token)
                    app.api_client.store.put('access_token', token=token)
                    user_info, user_error = app.api_client.get_current_user()
                    if user_info:
                        app.login_user(user_info, token)
                        self.hide_loading()
                        self.register_dialog.dismiss()
                    else:
                        self.hide_loading()
                        self.show_error(f"Registration failed: {user_error}")
                else:
                    self.hide_loading()
                    self.show_error("Registration failed: missing token")
            else:
                self.hide_loading()
                self.show_error(f"Registration failed: {error}")
        
        Clock.schedule_once(do_register, 0.1)
    
    def show_error(self, message):
        """Show error dialog"""
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_loading(self, message):
        """Show loading dialog"""
        self.loading_dialog = MDDialog(
            title=message,
            type="custom",
            content_cls=MDLabel(text="Please wait...")
        )
        self.loading_dialog.open()
    
    def hide_loading(self):
        """Hide loading dialog"""
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.dismiss()
