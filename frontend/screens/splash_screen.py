from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
import io
import base64
import os

class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        self.start_loading_animation()
    
    def build_ui(self):
        """Build the splash screen UI"""
        app = MDApp.get_running_app()
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=dp(20),
            padding=[dp(40), dp(40), dp(40), dp(40)]
        )
        
        # Logo container
        logo_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 0.8),
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Logo image (using the actual logo file)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "assets", "Logo for Travel Mate App - Iconographic Style.png")
        logo_path = os.path.abspath(logo_path)
        print(f"Looking for logo at: {logo_path}")
        print(f"Logo exists: {os.path.exists(logo_path)}")
        if os.path.exists(logo_path):
            logo_image = KivyImage(
                source=logo_path,
                size_hint=(None, None),
                size=(dp(200), dp(200)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            # Fallback logo using MDIconButton
            logo_image = MDBoxLayout(
                size_hint=(None, None),
                size=(dp(200), dp(200)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                md_bg_color=app.theme_cls.primary_color,
                radius=[dp(100)]
            )
            logo_icon = MDLabel(
                text="✈️",
                font_size=dp(80),
                halign="center",
                valign="center"
            )
            logo_image.add_widget(logo_icon)
        
        logo_container.add_widget(logo_image)
        
        # App name
        app_name = MDLabel(
            text="Travel Mate",
            theme_text_color="Primary",
            font_style="H3",
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )
        logo_container.add_widget(app_name)
        
        # Tagline
        tagline = MDLabel(
            text="Your Perfect Travel Companion",
            theme_text_color="Secondary",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        logo_container.add_widget(tagline)
        
        main_layout.add_widget(logo_container)
        
        # Loading section
        loading_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            spacing=dp(10),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Loading text
        self.loading_text = MDLabel(
            text="Loading...",
            theme_text_color="Primary",
            font_style="Body1",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        loading_container.add_widget(self.loading_text)
        
        # Loading dots animation
        self.loading_dots = MDLabel(
            text="...",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        loading_container.add_widget(self.loading_dots)
        
        main_layout.add_widget(loading_container)
        
        self.add_widget(main_layout)
    
    
    def start_loading_animation(self):
        """Start the loading animation"""
        # Animate the logo
        logo_widget = self.children[0].children[1].children[0]  # Get the logo widget
        if hasattr(logo_widget, 'opacity'):
            logo_widget.opacity = 0
            anim = Animation(opacity=1, duration=1.0, t='out_quad')
            anim.start(logo_widget)
        
        # Animate loading dots
        self.animate_loading_dots()
        
        # Start authentication check after a short delay
        Clock.schedule_once(self.check_authentication, 2.0)
    
    def animate_loading_dots(self):
        """Animate the loading dots"""
        def animate_dots(dt):
            current_text = self.loading_dots.text
            if current_text == "...":
                self.loading_dots.text = "."
            elif current_text == "..":
                self.loading_dots.text = "..."
            else:
                self.loading_dots.text = ".."
        
        # Schedule the animation to repeat
        Clock.schedule_interval(animate_dots, 0.5)
    
    def check_authentication(self, dt):
        """Check if user is authenticated"""
        app = MDApp.get_running_app()
        
        # Update loading text
        self.loading_text.text = "Checking authentication..."
        
        def do_auth_check(dt):
            # Check if user has valid token
            if app.store.exists('access_token'):
                # Validate token with backend
                user_data, error = app.api_client.get_current_user()
                if user_data:
                    # User is authenticated, go to dashboard
                    self.loading_text.text = "Welcome back!"
                    Clock.schedule_once(lambda dt: self.go_to_dashboard(), 1.0)
                else:
                    # Token is invalid, go to login
                    self.loading_text.text = "Please log in"
                    Clock.schedule_once(lambda dt: self.go_to_login(), 1.0)
            else:
                # No token, go to login
                self.loading_text.text = "Please log in"
                Clock.schedule_once(lambda dt: self.go_to_login(), 1.0)
        
        Clock.schedule_once(do_auth_check, 0.5)
    
    def go_to_dashboard(self):
        """Navigate to dashboard"""
        app = MDApp.get_running_app()
        app.screen_manager.current = 'dashboard'
        app.dashboard_screen.load_trips()
    
    def go_to_login(self):
        """Navigate to login screen"""
        app = MDApp.get_running_app()
        app.screen_manager.current = 'auth'
