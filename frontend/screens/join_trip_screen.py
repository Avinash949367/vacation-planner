from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button as MDRaisedButton, Button as MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.metrics import dp

class JoinTripScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=0
        )
        
        # Top app bar
        app = MDApp.get_running_app()
        self.top_bar = MDTopAppBar(
            title="Join Trip",
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
        
        # Welcome message
        welcome_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        welcome_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        welcome_title = MDLabel(
            text="Join a Trip",
            theme_text_color="Primary",
            font_style="H5",
            halign="center"
        )
        welcome_content.add_widget(welcome_title)
        
        welcome_desc = MDLabel(
            text="Enter a Trip ID or scan a QR code to join someone's trip",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        welcome_content.add_widget(welcome_desc)
        
        welcome_card.add_widget(welcome_content)
        self.content_container.add_widget(welcome_card)
        
        # Trip ID input section
        trip_id_card = MDCard(
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        trip_id_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        trip_id_title = MDLabel(
            text="Enter Trip ID",
            theme_text_color="Primary",
            font_style="H6"
        )
        trip_id_content.add_widget(trip_id_title)
        
        self.trip_id_field = MDTextField(
            hint_text="Enter the Trip ID shared by your friend",
            helper_text="Trip ID is usually a short code like 'ABC123'",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(60),
            icon_left="key"
        )
        trip_id_content.add_widget(self.trip_id_field)
        
        join_btn = MDRaisedButton(
            text="Join Trip",
            size_hint_y=None,
            height=dp(48),
            on_release=self.join_trip_by_id
        )
        trip_id_content.add_widget(join_btn)
        
        trip_id_card.add_widget(trip_id_content)
        self.content_container.add_widget(trip_id_card)
        
        # QR Code section
        qr_card = MDCard(
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        qr_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        qr_title = MDLabel(
            text="Scan QR Code",
            theme_text_color="Primary",
            font_style="H6"
        )
        qr_content.add_widget(qr_title)
        
        qr_desc = MDLabel(
            text="Point your camera at the QR code shared by your friend",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        qr_content.add_widget(qr_desc)
        
        scan_btn = MDRaisedButton(
            text="Scan QR Code",
            size_hint_y=None,
            height=dp(48),
            icon="qrcode-scan",
            on_release=self.scan_qr_code
        )
        qr_content.add_widget(scan_btn)
        
        qr_card.add_widget(qr_content)
        self.content_container.add_widget(qr_card)
        
        # Help section
        help_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=1,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        help_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        help_title = MDLabel(
            text="Need Help?",
            theme_text_color="Primary",
            font_style="H6"
        )
        help_content.add_widget(help_title)
        
        help_text = MDLabel(
            text="Ask your friend to share their Trip ID or QR code from the trip details screen",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        help_content.add_widget(help_text)
        
        help_card.add_widget(help_content)
        self.content_container.add_widget(help_card)
        
        self.scroll_view.add_widget(self.content_container)
        main_layout.add_widget(self.scroll_view)
        
        self.add_widget(main_layout)
    
    def join_trip_by_id(self, instance):
        """Join trip using Trip ID"""
        trip_id = self.trip_id_field.text.strip()
        
        if not trip_id:
            self.show_error("Please enter a Trip ID")
            return
        
        self.show_loading("Joining trip...")
        
        def do_join(dt):
            app = MDApp.get_running_app()
            trip_data, error = app.api_client.join_trip(trip_id)
            
            self.hide_loading()
            
            if trip_data:
                self.show_success(f"Successfully joined trip: {trip_data.get('title', 'Unknown Trip')}")
                # Refresh the dashboard to show the new trip
                Clock.schedule_once(lambda dt: self.refresh_dashboard_and_go_back(), 2)
            else:
                self.show_error(f"Failed to join trip: {error}")
        
        Clock.schedule_once(do_join, 0.5)
    
    def refresh_dashboard_and_go_back(self):
        """Refresh dashboard and go back"""
        app = MDApp.get_running_app()
        # Refresh trips in dashboard
        if hasattr(app, 'dashboard_screen'):
            app.dashboard_screen.load_trips()
        app.go_back_to_dashboard()
    
    def scan_qr_code(self, instance):
        """Scan QR code to join trip"""
        # For now, we'll simulate QR scanning
        # In a real implementation, you'd use a camera scanner
        self.show_info("QR Scanner", "QR code scanning will be available in a future update. Please use Trip ID for now.")
    
    def go_back(self):
        """Go back to dashboard"""
        app = MDApp.get_running_app()
        app.go_back_to_dashboard()
    
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
    
    def show_success(self, message):
        """Show success dialog"""
        dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_info(self, title, message):
        """Show info dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
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
