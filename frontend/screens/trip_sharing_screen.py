from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton as MDRaisedButton, MDTextButton as MDFlatButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image as KivyImage
import qrcode
import io
from kivy.core.image import Image as CoreImage

class TripSharingScreen(MDScreen):
    def __init__(self, trip=None, **kwargs):
        super().__init__(**kwargs)
        self.trip = trip
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
            title="Share Trip",
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
        
        # Trip info card
        if self.trip:
            self.add_trip_info_card()
        
        # QR Code section
        self.add_qr_code_section()
        
        # Trip ID section
        self.add_trip_id_section()
        
        # Share options
        self.add_share_options()
        
        self.scroll_view.add_widget(self.content_container)
        main_layout.add_widget(self.scroll_view)
        
        self.add_widget(main_layout)
    
    def add_trip_info_card(self):
        """Add trip information card"""
        trip_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        trip_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        # Trip title
        title = MDLabel(
            text=self.trip.get('title', 'Unknown Trip'),
            theme_text_color="Primary",
            font_style="H6"
        )
        trip_content.add_widget(title)
        
        # Destination
        destination = MDLabel(
            text=f"📍 {self.trip.get('destination', 'Unknown Destination')}",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        trip_content.add_widget(destination)
        
        # Dates
        start_date = self.trip.get('start_date', '')
        end_date = self.trip.get('end_date', '')
        if start_date and end_date:
            dates = MDLabel(
                text=f"📅 {start_date[:10]} to {end_date[:10]}",
                theme_text_color="Secondary",
                font_style="Body2"
            )
            trip_content.add_widget(dates)
        
        trip_card.add_widget(trip_content)
        self.content_container.add_widget(trip_card)
    
    def add_qr_code_section(self):
        """Add QR code section"""
        qr_card = MDCard(
            size_hint_y=None,
            height=dp(250),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        qr_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # Title
        title = MDLabel(
            text="QR Code",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        qr_content.add_widget(title)
        
        # QR Code container
        self.qr_container = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=1,
            radius=[8],
            md_bg_color=(0.95, 0.95, 0.95, 1)
        )
        
        # Generate QR code immediately
        self.generate_qr_code_display()
        
        qr_content.add_widget(self.qr_container)
        
        # Instructions
        instructions = MDLabel(
            text="Share this QR code with friends to let them join your trip",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        qr_content.add_widget(instructions)
        
        qr_card.add_widget(qr_content)
        self.content_container.add_widget(qr_card)
    
    def add_trip_id_section(self):
        """Add trip ID section"""
        id_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        id_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )
        
        # Title
        title = MDLabel(
            text="Trip ID",
            theme_text_color="Primary",
            font_style="H6"
        )
        id_content.add_widget(title)
        
        # Trip ID display
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown')) if self.trip else 'Unknown'
        id_display = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(8)
        )
        
        self.id_field = MDTextField(
            text=trip_id,
            hint_text="Trip ID",
            readonly=True,
            size_hint_x=0.7,
            mode="rectangle"
        )
        id_display.add_widget(self.id_field)
        
        copy_btn = MDIconButton(
            icon="content-copy",
            size_hint_x=0.3,
            on_release=self.copy_trip_id
        )
        id_display.add_widget(copy_btn)
        
        id_content.add_widget(id_display)
        
        # Instructions
        instructions = MDLabel(
            text="Share this Trip ID with friends",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        id_content.add_widget(instructions)
        
        id_card.add_widget(id_content)
        self.content_container.add_widget(id_card)
    
    def add_share_options(self):
        """Add share options"""
        share_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            radius=[12],
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        share_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )
        
        # Title
        title = MDLabel(
            text="Share Options",
            theme_text_color="Primary",
            font_style="H6"
        )
        share_content.add_widget(title)
        
        # Share buttons
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(12)
        )
        
        # Share via message
        message_btn = MDRaisedButton(
            text="Share via Message",
            size_hint_x=0.5,
            icon="message",
            on_release=self.share_via_message
        )
        buttons_layout.add_widget(message_btn)
        
        # Share via email
        email_btn = MDRaisedButton(
            text="Share via Email",
            size_hint_x=0.5,
            icon="email",
            on_release=self.share_via_email
        )
        buttons_layout.add_widget(email_btn)
        
        share_content.add_widget(buttons_layout)
        share_card.add_widget(share_content)
        self.content_container.add_widget(share_card)
    
    def generate_qr_code_display(self):
        """Generate and display QR code in the container"""
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown')) if self.trip else 'Unknown'
        qr_data = f"travelmate://join/{trip_id}"
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=6, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Create Kivy image
            core_img = CoreImage(img_buffer, ext='png')
            qr_image = KivyImage(
                texture=core_img.texture,
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=True
            )
            
            # Clear container and add QR code
            self.qr_container.clear_widgets()
            self.qr_container.add_widget(qr_image)
            
        except Exception as e:
            # Fallback to text if QR generation fails
            self.qr_container.clear_widgets()
            qr_text = MDLabel(
                text=f"QR Code\nTrip ID: {trip_id}",
                theme_text_color="Secondary",
                font_style="Body2",
                halign="center",
                valign="center"
            )
            self.qr_container.add_widget(qr_text)
    
    def generate_qr_code(self, instance, touch):
        """Generate QR code for trip sharing"""
        if not instance.collide_point(*touch.pos):
            return
        
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown')) if self.trip else 'Unknown'
        qr_data = f"travelmate://join/{trip_id}"
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Show QR code in dialog
            self.show_qr_code_dialog(img_buffer.getvalue())
            
        except Exception as e:
            app = MDApp.get_running_app()
            app.show_error_snackbar(f"Failed to generate QR code: {str(e)}")
    
    def show_qr_code_dialog(self, qr_data):
        """Show QR code in a dialog"""
        app = MDApp.get_running_app()
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Trip QR Code",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # QR Code image
        try:
            core_img = CoreImage(io.BytesIO(qr_data), ext='png')
            qr_image = KivyImage(
                texture=core_img.texture,
                size_hint=(1, None),
                height=dp(200),
                allow_stretch=True,
                keep_ratio=True
            )
            content.add_widget(qr_image)
        except Exception as e:
            qr_label = MDLabel(
                text=f"QR Code Generated!\nTrip ID: {self.trip.get('_id', 'Unknown') if self.trip else 'Unknown'}",
                theme_text_color="Secondary",
                font_style="Body2",
                halign="center"
            )
            content.add_widget(qr_label)
        
        content.height = dp(280)
        
        dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def copy_trip_id(self, instance):
        """Copy trip ID to clipboard"""
        trip_id = self.id_field.text
        # In a real app, you'd copy to clipboard
        app = MDApp.get_running_app()
        app.show_success_snackbar(f"Trip ID copied: {trip_id}")
    
    def share_via_message(self, instance):
        """Share trip via message"""
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown')) if self.trip else 'Unknown'
        message = f"Join my trip! Use Trip ID: {trip_id} or scan the QR code in TravelMate app."
        # In a real app, you'd open the messaging app
        app = MDApp.get_running_app()
        app.show_success_snackbar("Message sharing not implemented in demo")
    
    def share_via_email(self, instance):
        """Share trip via email"""
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown')) if self.trip else 'Unknown'
        subject = "Join my trip on TravelMate!"
        body = f"Hi!\n\nI'd like to invite you to join my trip on TravelMate.\n\nTrip ID: {trip_id}\n\nDownload TravelMate and use this ID to join my trip!\n\nBest regards"
        # In a real app, you'd open the email app
        app = MDApp.get_running_app()
        app.show_success_snackbar("Email sharing not implemented in demo")
    
    def go_back(self):
        """Go back to previous screen"""
        app = MDApp.get_running_app()
        app.go_back_to_dashboard()
