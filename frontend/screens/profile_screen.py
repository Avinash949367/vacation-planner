from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button as MDRaisedButton, Button as MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
import requests
import base64
import io
import os
import cloudinary
import cloudinary.uploader

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name="dwgwtx0jz",
            api_key="523154331876144",
            api_secret="j-XAGu4EUdSjqw9tGwa85ZbQ0v0"
        )
        self.build_ui()
    
    def on_enter(self):
        """Called when the screen is entered"""
        super().on_enter()
        # Refresh user data when entering the screen with smooth loading
        Clock.schedule_once(lambda dt: self.load_user_data(), 0.05)
    
    def build_ui(self):
        """Build the profile screen UI"""
        app = MDApp.get_running_app()
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=0
        )
        
        # Top app bar
        self.top_bar = MDTopAppBar(
            title="Profile",
            elevation=2,
            md_bg_color=app.theme_cls.primary_color,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            specific_text_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.top_bar)
        
        # Scroll view for content
        self.scroll_view = MDScrollView()
        
        # Content container
        self.content_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            size_hint_y=None
        )
        self.content_container.bind(minimum_height=self.content_container.setter('height'))
        
        # Profile picture section
        self.add_profile_picture_section()
        
        # User info section
        self.add_user_info_section()
        
        # Password section
        self.add_password_section()
        
        self.scroll_view.add_widget(self.content_container)
        main_layout.add_widget(self.scroll_view)
        
        self.add_widget(main_layout)
        
        # Load user data
        Clock.schedule_once(lambda dt: self.load_user_data(), 0.1)
    
    def add_profile_picture_section(self):
        """Add profile picture section"""
        app = MDApp.get_running_app()
        
        # Profile picture card
        pic_card = MDCard(
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        pic_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # Title
        title = MDLabel(
            text="Profile Picture",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        pic_content.add_widget(title)
        
        # Profile picture container
        pic_container = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(20)
        )
        
        # Profile picture placeholder
        self.profile_pic = MDCard(
            size_hint_x=None,
            width=dp(80),
            height=dp(80),
            elevation=2,
            radius=[40],
            md_bg_color=(0.9, 0.9, 0.9, 1)
        )
        
        # Default profile icon
        self.profile_icon = MDIconButton(
            icon="account",
            size_hint=(1, 1),
            theme_icon_color="Secondary",
            icon_size=dp(40)
        )
        self.profile_pic.add_widget(self.profile_icon)
        
        pic_container.add_widget(self.profile_pic)
        
        # Upload button
        upload_btn = MDRaisedButton(
            text="Upload Photo",
            icon="camera",
            size_hint_x=None,
            width=dp(120),
            on_release=self.upload_profile_picture
        )
        pic_container.add_widget(upload_btn)
        
        pic_content.add_widget(pic_container)
        pic_card.add_widget(pic_content)
        self.content_container.add_widget(pic_card)
    
    def add_user_info_section(self):
        """Add user information section"""
        app = MDApp.get_running_app()
        
        # User info card
        info_card = MDCard(
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        info_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # Title
        title = MDLabel(
            text="Personal Information",
            theme_text_color="Primary",
            font_style="H6"
        )
        info_content.add_widget(title)
        
        # Name field
        name_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )
        
        name_label = MDLabel(
            text="Name:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        name_layout.add_widget(name_label)
        
        self.name_field = MDTextField(
            hint_text="Your name",
            mode="rectangle",
            size_hint_x=0.7,
            readonly=False
        )
        name_layout.add_widget(self.name_field)
        
        info_content.add_widget(name_layout)
        
        # Email field (readonly)
        email_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )
        
        email_label = MDLabel(
            text="Email:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        email_layout.add_widget(email_label)
        
        self.email_field = MDTextField(
            hint_text="Your email address",
            mode="rectangle",
            readonly=True,
            size_hint_x=0.7
        )
        email_layout.add_widget(self.email_field)
        
        info_content.add_widget(email_layout)
        
        # Save button
        save_btn = MDRaisedButton(
            text="Save Changes",
            icon="content-save",
            size_hint_y=None,
            height=dp(48),
            on_release=self.save_user_info
        )
        info_content.add_widget(save_btn)
        
        info_card.add_widget(info_content)
        self.content_container.add_widget(info_card)
    
    def add_password_section(self):
        """Add password change section"""
        app = MDApp.get_running_app()
        
        # Password card
        pwd_card = MDCard(
            size_hint_y=None,
            height=dp(250),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        pwd_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # Title
        title = MDLabel(
            text="Change Password",
            theme_text_color="Primary",
            font_style="H6"
        )
        pwd_content.add_widget(title)
        
        # Current password
        current_pwd_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )
        
        current_pwd_label = MDLabel(
            text="Current:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        current_pwd_layout.add_widget(current_pwd_label)
        
        self.current_pwd_field = MDTextField(
            hint_text="Current password",
            mode="rectangle",
            password=True,
            size_hint_x=0.7
        )
        current_pwd_layout.add_widget(self.current_pwd_field)
        
        pwd_content.add_widget(current_pwd_layout)
        
        # New password
        new_pwd_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )
        
        new_pwd_label = MDLabel(
            text="New:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        new_pwd_layout.add_widget(new_pwd_label)
        
        self.new_pwd_field = MDTextField(
            hint_text="New password",
            mode="rectangle",
            password=True,
            size_hint_x=0.7
        )
        new_pwd_layout.add_widget(self.new_pwd_field)
        
        pwd_content.add_widget(new_pwd_layout)
        
        # Confirm password
        confirm_pwd_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )
        
        confirm_pwd_label = MDLabel(
            text="Confirm:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        confirm_pwd_layout.add_widget(confirm_pwd_label)
        
        self.confirm_pwd_field = MDTextField(
            hint_text="Confirm new password",
            mode="rectangle",
            password=True,
            size_hint_x=0.7
        )
        confirm_pwd_layout.add_widget(self.confirm_pwd_field)
        
        pwd_content.add_widget(confirm_pwd_layout)
        
        # Change password button
        change_pwd_btn = MDRaisedButton(
            text="Change Password",
            icon="lock-reset",
            size_hint_y=None,
            height=dp(48),
            on_release=self.change_password
        )
        pwd_content.add_widget(change_pwd_btn)
        
        pwd_card.add_widget(pwd_content)
        self.content_container.add_widget(pwd_card)
    
    def load_user_data(self):
        """Load current user data"""
        app = MDApp.get_running_app()
        
        # Get fresh user data from API
        user_data, error = app.api_client.get_current_user()
        
        if user_data:
            self.current_user = user_data
            # Set the actual values in the text fields
            # Use name if available, otherwise fallback to username
            name = user_data.get('name') or user_data.get('username', '')
            email = user_data.get('email', '')
            
            self.name_field.text = name
            self.email_field.text = email
            
            # Load profile picture if available
            profile_pic_url = user_data.get('profile_picture')
            if profile_pic_url:
                self.load_profile_picture(profile_pic_url)
        else:
            # Fallback to cached user data
            if hasattr(app, 'current_user') and app.current_user:
                self.current_user = app.current_user
                # Set the actual values in the text fields
                # Use name if available, otherwise fallback to username
                name = app.current_user.get('name') or app.current_user.get('username', '')
                email = app.current_user.get('email', '')
                
                self.name_field.text = name
                self.email_field.text = email
    
    def load_profile_picture(self, image_url):
        """Load profile picture from URL"""
        try:
            # For demo, we'll just change the icon
            # In a real app, you'd download and display the actual image
            self.profile_icon.icon = "account-check"
            self.profile_icon.theme_icon_color = "Primary"
        except Exception as e:
            print(f"Error loading profile picture: {e}")
    
    def upload_profile_picture(self, instance):
        """Upload profile picture"""
        app = MDApp.get_running_app()
        
        # Create file picker dialog
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Upload Profile Picture",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # Instructions
        instructions = MDLabel(
            text="Enter image URL to upload to Cloudinary",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(instructions)
        
        # File input
        file_input = MDTextField(
            hint_text="Enter image URL",
            mode="rectangle",
            multiline=False
        )
        content.add_widget(file_input)
        
        content.height = dp(150)
        
        # Create dialog
        dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Upload",
                    on_release=lambda x: self.process_image_upload(file_input.text, dialog)
                )
            ]
        )
        dialog.open()
    
    def process_image_upload(self, image_url, dialog):
        """Process the image upload to Cloudinary"""
        app = MDApp.get_running_app()
        
        if not image_url.strip():
            app.show_error_snackbar("Please enter an image URL")
            return
        
        try:
            # Upload to Cloudinary
            print(f"Uploading image to Cloudinary: {image_url}")
            
            # Upload image to Cloudinary
            result = cloudinary.uploader.upload(
                image_url,
                folder="profile_pictures",
                public_id=f"user_{app.current_user.get('id', 'unknown')}",
                overwrite=True
            )
            
            # Get the secure URL from Cloudinary
            profile_pic_url = result['secure_url']
            print(f"Upload successful: {profile_pic_url}")
            
            # Update the profile icon
            self.profile_icon.icon = "account-check"
            self.profile_icon.theme_icon_color = "Primary"
            
            # Update user data
            if self.current_user:
                self.current_user['profile_picture'] = profile_pic_url
            
            # Update profile picture in database via API
            self.update_profile_picture_in_db(profile_pic_url)
            
            app.show_success_snackbar("Profile picture updated successfully!")
            dialog.dismiss()
            
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            app.show_error_snackbar(f"Failed to upload image: {str(e)}")
    
    def update_profile_picture_in_db(self, profile_pic_url):
        """Update profile picture URL in database"""
        app = MDApp.get_running_app()
        
        try:
            # Update profile picture via API
            user_data = {
                "profile_picture": profile_pic_url
            }
            
            result, error = app.api_client.update_user_profile(user_data)
            if result:
                print("Profile picture URL updated in database")
            else:
                print(f"Failed to update profile picture in database: {error}")
                
        except Exception as e:
            print(f"Error updating profile picture in database: {e}")
    
    def save_user_info(self, instance):
        """Save user information"""
        app = MDApp.get_running_app()
        
        name = self.name_field.text.strip()
        if not name:
            app.show_error_snackbar("Please enter a name")
            return
        
        # Update user info via API
        user_data = {
            "name": name
        }
        
        success, error = app.api_client.update_user_profile(user_data)
        if success:
            app.show_success_snackbar("Profile updated successfully!")
            # Update current user data
            if hasattr(app, 'current_user'):
                app.current_user['name'] = name
            if self.current_user:
                self.current_user['name'] = name
        else:
            app.show_error_snackbar(f"Failed to update profile: {error}")
    
    def change_password(self, instance):
        """Change user password"""
        app = MDApp.get_running_app()
        
        current_pwd = self.current_pwd_field.text
        new_pwd = self.new_pwd_field.text
        confirm_pwd = self.confirm_pwd_field.text
        
        # Validation
        if not current_pwd or not new_pwd or not confirm_pwd:
            app.show_error_snackbar("Please fill in all password fields")
            return
        
        if new_pwd != confirm_pwd:
            app.show_error_snackbar("New passwords do not match")
            return
        
        if len(new_pwd) < 6:
            app.show_error_snackbar("New password must be at least 6 characters")
            return
        
        # Update password via API
        password_data = {
            "current_password": current_pwd,
            "new_password": new_pwd
        }
        
        success, error = app.api_client.change_password(password_data)
        if success:
            app.show_success_snackbar("Password changed successfully!")
            # Clear password fields
            self.current_pwd_field.text = ""
            self.new_pwd_field.text = ""
            self.confirm_pwd_field.text = ""
        else:
            app.show_error_snackbar(f"Failed to change password: {error}")
    
    def go_back(self):
        """Go back to dashboard"""
        app = MDApp.get_running_app()
        app.screen_manager.current = 'dashboard'
