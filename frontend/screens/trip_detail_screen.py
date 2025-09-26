from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button as MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.metrics import dp
from datetime import datetime

from screens.overview_tab import OverviewTab
from screens.itinerary_tab import ItineraryTab
from screens.budget_tab import BudgetTab
from screens.packing_tab import PackingTab

class TripDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trip = None
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
            title="Trip Details",
            elevation=2,
            md_bg_color=app.theme_cls.primary_color,
            left_action_items=[["arrow-left", self.go_back]],
            right_action_items=[["dots-vertical", self.show_menu]]
        )
        
        main_layout.add_widget(self.top_bar)
        
        # Bottom navigation
        self.bottom_nav = MDBottomNavigation(
            panel_color=app.theme_cls.primary_color,
            selected_color_background=app.theme_cls.primary_color,
            text_color_active=[1, 1, 1, 1],  # White color for active text and icon
            md_bg_color=[1, 1, 1, 0.9],  # Semi-transparent background for floating effect
            radius=[20, 20, 20, 20],  # Rounded corners
            padding=[10, 10, 10, 10]
        )
        
        # Overview tab
        self.overview_tab = OverviewTab(name='overview')
        self.overview_item = MDBottomNavigationItem(
            name='overview',
            text='Overview',
            icon='home'
        )
        self.overview_item.add_widget(self.overview_tab)
        self.bottom_nav.add_widget(self.overview_item)
        
        # Itinerary tab
        self.itinerary_tab = ItineraryTab(name='itinerary')
        self.itinerary_item = MDBottomNavigationItem(
            name='itinerary',
            text='Itinerary',
            icon='calendar'
        )
        self.itinerary_item.add_widget(self.itinerary_tab)
        self.bottom_nav.add_widget(self.itinerary_item)
        
        # Budget tab
        self.budget_tab = BudgetTab(name='budget')
        self.budget_item = MDBottomNavigationItem(
            name='budget',
            text='Budget',
            icon='currency-usd'
        )
        self.budget_item.add_widget(self.budget_tab)
        self.bottom_nav.add_widget(self.budget_item)
        
        # Packing tab
        self.packing_tab = PackingTab(name='packing')
        self.packing_item = MDBottomNavigationItem(
            name='packing',
            text='Packing',
            icon='bag-personal'
        )
        self.packing_item.add_widget(self.packing_tab)
        self.bottom_nav.add_widget(self.packing_item)
        
        main_layout.add_widget(self.bottom_nav)
        
        self.add_widget(main_layout)
    
    def load_trip(self, trip):
        """Load trip data"""
        self.trip = trip
        self.top_bar.title = trip['title']
        
        # Load data in all tabs
        self.overview_tab.load_trip(trip)
        self.itinerary_tab.load_trip(trip)
        self.budget_tab.load_trip(trip)
        self.packing_tab.load_trip(trip)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        app = MDApp.get_running_app()
        app.go_back_to_dashboard()

    def go_home(self, instance):
        """Go to home/landing page"""
        app = MDApp.get_running_app()
        app.go_back_to_dashboard()
    
    def show_menu(self, instance):
        """Show trip menu"""
        menu_items = [
            {
                "text": "Edit Trip",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.edit_trip()
            },
            {
                "text": "Share Trip",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.share_trip()
            },
            {
                "text": "Delete Trip",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.delete_trip()
            }
        ]
        
        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4
        )
        self.menu.open()
    
    def edit_trip(self):
        """Edit trip details"""
        app = MDApp.get_running_app()
        # Pre-fill the create trip form with current trip data
        app.create_trip_screen.title_field.text = self.trip.get('title', '')
        app.create_trip_screen.destination_field.text = self.trip.get('destination', '')
        app.create_trip_screen.start_date_field.text = self.trip.get('start_date', '')[:10] if self.trip.get('start_date') else ''
        app.create_trip_screen.end_date_field.text = self.trip.get('end_date', '')[:10] if self.trip.get('end_date') else ''
        app.create_trip_screen.budget_field.text = str(self.trip.get('budget', ''))
        # Set editing flag and trip data
        app.create_trip_screen.editing_trip = self.trip
        # Navigate to create trip screen
        app.screen_manager.current = 'create_trip'
    
    def share_trip(self):
        """Share trip with others"""
        if not self.trip:
            return
            
        app = MDApp.get_running_app()
        
        # Create dialog content
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Share Trip",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # Trip info
        trip_info = MDLabel(
            text=f"{self.trip.get('title', 'Unknown Trip')}\n📍 {self.trip.get('destination', 'Unknown Destination')}",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(trip_info)
        
        # Share options
        options_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            height=dp(120)
        )
        
        # Key option
        key_btn = MDRaisedButton(
            text="Share Trip Key",
            icon="key",
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.share_trip_key()
        )
        options_layout.add_widget(key_btn)
        
        # QR option
        qr_btn = MDRaisedButton(
            text="Share QR Code",
            icon="qrcode",
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.share_trip_qr()
        )
        options_layout.add_widget(qr_btn)
        
        content.add_widget(options_layout)
        content.height = dp(200)
        
        # Create dialog
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
    
    def share_trip_key(self):
        """Share trip key"""
        if not self.trip:
            return
            
        app = MDApp.get_running_app()
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown'))
        
        # Create dialog to show trip key
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Trip Key",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # Trip key display
        key_display = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )
        
        key_field = MDTextField(
            text=trip_id,
            hint_text="Trip Key",
            readonly=True,
            size_hint_x=0.7,
            mode="rectangle"
        )
        key_display.add_widget(key_field)
        
        copy_btn = MDIconButton(
            icon="content-copy",
            size_hint_x=0.3,
            on_release=lambda x: self.copy_trip_key(trip_id)
        )
        key_display.add_widget(copy_btn)
        
        content.add_widget(key_display)
        
        # Instructions
        instructions = MDLabel(
            text="Share this key with friends to let them join your trip",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(instructions)
        
        content.height = dp(150)
        
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
    
    def share_trip_qr(self):
        """Share trip QR code"""
        if not self.trip:
            return
            
        app = MDApp.get_running_app()
        trip_id = self.trip.get('_id', self.trip.get('id', 'Unknown'))
        
        # Create dialog to show QR code
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
        
        # Generate and show QR code
        try:
            import qrcode
            import io
            from kivy.core.image import Image as CoreImage
            from kivy.uix.image import Image as KivyImage
            
            qr_data = f"travelmate://join/{trip_id}"
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            core_img = CoreImage(img_buffer, ext='png')
            qr_image = KivyImage(
                texture=core_img.texture,
                size_hint=(1, None),
                height=dp(200),
                allow_stretch=True,
                keep_ratio=True
            )
            content.add_widget(qr_image)
            
        except Exception as e:
            # Fallback to text
            qr_text = MDLabel(
                text=f"QR Code\nTrip ID: {trip_id}",
                theme_text_color="Secondary",
                font_style="Body2",
                halign="center"
            )
            content.add_widget(qr_text)
        
        # Instructions
        instructions = MDLabel(
            text="Share this QR code with friends to let them join your trip",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(instructions)
        
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
    
    def copy_trip_key(self, trip_id):
        """Copy trip key to clipboard"""
        app = MDApp.get_running_app()
        app.show_success_snackbar(f"Trip key copied: {trip_id}")
    
    def delete_trip(self):
        """Delete trip"""
        dialog = MDDialog(
            title="Delete Trip",
            text="Are you sure you want to delete this trip? This action cannot be undone.",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete(dialog)
                )
            ]
        )
        dialog.open()
    
    def confirm_delete(self, dialog):
        """Confirm trip deletion"""
        dialog.dismiss()

        app = MDApp.get_running_app()

        def do_delete(dt):
            trip_id = getattr(self.trip, 'id', None)
            if trip_id is None:
                trip_id = self.trip.get('_id') if isinstance(self.trip, dict) else None
                if trip_id is None:
                    trip_id = self.trip.get('id') if isinstance(self.trip, dict) else None
            if trip_id is None:
                app.show_error_snackbar("Trip ID not found")
                return

            result, error = app.api_client.delete_trip(str(trip_id))
            if result:
                app.show_success_snackbar("Trip deleted successfully!")
                app.go_back_to_dashboard()
            else:
                app.show_error_snackbar(f"Failed to delete trip: {error}")

        Clock.schedule_once(do_delete, 0.1)
