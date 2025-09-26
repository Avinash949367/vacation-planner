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
from kivy.clock import Clock
from kivy.metrics import dp
from datetime import datetime
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.card import MDCard
import qrcode
import io
from kivy.core.image import Image as CoreImage

class CreateTripScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editing_trip = None
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
            title="Create Trip",
            elevation=2,
            md_bg_color=app.theme_cls.primary_color
        )

        # Back button
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )
        self.top_bar.add_widget(back_btn)

        main_layout.add_widget(self.top_bar)

        # Scroll view for form
        self.scroll_view = MDScrollView()

        # Form container
        self.form_container = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[20, 20, 20, 20],
            size_hint_y=None
        )
        self.form_container.bind(minimum_height=self.form_container.setter('height'))

        # Trip title
        self.title_field = MDTextField(
            hint_text="Trip Title",
            helper_text="e.g., Goa Vacation",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60
        )
        self.form_container.add_widget(self.title_field)

        # Destination
        self.destination_field = MDTextField(
            hint_text="Destination",
            helper_text="e.g., Goa, India",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60
        )
        self.form_container.add_widget(self.destination_field)

        # Start date
        self.start_date_field = MDTextField(
            hint_text="Start Date",
            helper_text="Tap calendar to pick",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60,
            icon_left="calendar",
            icon_right="calendar"
        )
        self.start_date_field.bind(on_right_icon_release=lambda *_: self.open_start_date_picker())
        self.start_date_field.bind(focus=lambda instance, value: self.open_start_date_picker() if value else None)
        self.form_container.add_widget(self.start_date_field)

        # End date
        self.end_date_field = MDTextField(
            hint_text="End Date",
            helper_text="Tap calendar to pick",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60,
            icon_left="calendar",
            icon_right="calendar"
        )
        self.end_date_field.bind(on_right_icon_release=lambda *_: self.open_end_date_picker())
        self.end_date_field.bind(focus=lambda instance, value: self.open_end_date_picker() if value else None)
        self.form_container.add_widget(self.end_date_field)

        # Budget
        self.budget_field = MDTextField(
            hint_text="Budget (optional)",
            helper_text="Enter estimated budget",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=60,
            input_filter="float"
        )
        self.form_container.add_widget(self.budget_field)

        # Create Trip button
        self.create_btn = MDRaisedButton(
            text="Create Trip",
            size_hint_y=None,
            height=50,
            on_release=self.create_trip
        )
        self.form_container.add_widget(self.create_btn)

        self.scroll_view.add_widget(self.form_container)
        main_layout.add_widget(self.scroll_view)

        self.add_widget(main_layout)



    def open_start_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self._on_start_date)
        picker.open()

    def _on_start_date(self, instance, value, date_range):
        # value is datetime.date
        try:
            self.start_date_field.text = value.strftime("%Y-%m-%d")
        except Exception:
            pass

    def open_end_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self._on_end_date)
        picker.open()

    def _on_end_date(self, instance, value, date_range):
        try:
            self.end_date_field.text = value.strftime("%Y-%m-%d")
        except Exception:
            pass

    def create_trip(self, instance):
        """Create or update a trip"""
        # Get form data
        title = self.title_field.text.strip()
        destination = self.destination_field.text.strip()
        start_date_str = self.start_date_field.text.strip()
        end_date_str = self.end_date_field.text.strip()

        # Validate inputs
        has_error = False
        def set_error(field, msg):
            nonlocal has_error
            has_error = True
            field.error = True
            field.helper_text = msg
            field.helper_text_mode = "persistent"

        # Clear previous errors
        for f in [self.title_field, self.destination_field, self.start_date_field, self.end_date_field]:
            f.error = False
            f.helper_text_mode = "on_focus"

        if not title:
            set_error(self.title_field, "Title is required")
        if not destination:
            set_error(self.destination_field, "Destination is required")
        if not start_date_str:
            set_error(self.start_date_field, "Start date is required")
        if not end_date_str:
            set_error(self.end_date_field, "End date is required")
        if has_error:
            return

        try:
            # Parse dates
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if start_date >= end_date:
                self.show_error("End date must be after start date")
                return

        except ValueError as e:
            set_error(self.start_date_field, "Use the calendar to pick a date")
            set_error(self.end_date_field, "Use the calendar to pick a date")
            return

        # Prepare trip data with default budget
        trip_data = {
            "title": title,
            "destination": destination,
            "start_date": start_date.isoformat() + "Z",
            "end_date": end_date.isoformat() + "Z",
            "budget": float(self.budget_field.text) if self.budget_field.text else 0.0,
            "notes": "",
            "people": 1
        }

        # Get app instance
        app = MDApp.get_running_app()

        # Show loading
        action = "Updating" if self.editing_trip else "Creating"
        self.show_loading(f"{action} trip...")

        # Make API call
        def do_action(dt):
            if self.editing_trip:
                # Handle different ID field names
                trip_id = getattr(self.editing_trip, 'id', None)
                if trip_id is None:
                    trip_id = self.editing_trip.get('_id') if isinstance(self.editing_trip, dict) else None
                    if trip_id is None:
                        trip_id = self.editing_trip.get('id') if isinstance(self.editing_trip, dict) else None

                if trip_id is None:
                    self.hide_loading()
                    app.show_error_snackbar("Trip ID not found")
                    return

                result, error = app.api_client.update_trip(str(trip_id), trip_data)
                message = "Trip updated successfully!"
            else:
                result, error = app.api_client.create_trip(trip_data)
                message = "Trip created successfully!"
            if result:
                self.hide_loading()
                if not self.editing_trip:  # Only show QR for new trips
                    self.show_trip_created_success(result)
                else:
                    app.show_success_snackbar(message)
                self.clear_form()
                self.editing_trip = None
                if self.editing_trip:  # Go back immediately for edits
                    app.go_back_to_dashboard()
            else:
                self.hide_loading()
                app.show_error_snackbar(f"Failed to {action.lower()} trip: {error}")

        Clock.schedule_once(do_action, 0.1)
    
    def clear_form(self):
        """Clear the form"""
        self.title_field.text = ""
        self.destination_field.text = ""
        self.start_date_field.text = ""
        self.end_date_field.text = ""
        self.budget_field.text = ""
    
    def go_back(self, instance):
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
    
    def generate_qr_code(self, trip_id):
        """Generate QR code for trip sharing"""
        try:
            # Create QR code with trip join URL
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"travelmate://join/{trip_id}")
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            return img_buffer.getvalue()
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    def show_trip_created_success(self, trip_data):
        """Show success dialog with QR code and trip ID"""
        app = MDApp.get_running_app()
        trip_id = trip_data.get('id', 'Unknown')
        
        # Create content with QR code and trip ID
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Success message
        success_label = MDLabel(
            text="Trip created successfully!",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(success_label)
        
        # Trip ID
        trip_id_label = MDLabel(
            text=f"Trip ID: {trip_id}",
            theme_text_color="Secondary",
            font_style="Body1",
            halign="center"
        )
        content.add_widget(trip_id_label)
        
        # QR Code (if available)
        qr_data = self.generate_qr_code(trip_id)
        if qr_data:
            try:
                # Create texture from QR code data
                texture = CoreImage(io.BytesIO(qr_data), ext='png').texture
                
                # Add QR code label
                qr_label = MDLabel(
                    text="Share this QR code to invite others:",
                    theme_text_color="Secondary",
                    font_style="Body2",
                    halign="center"
                )
                content.add_widget(qr_label)
                
                # Note: In a real implementation, you'd display the QR code image here
                # For now, we'll just show the trip ID
                
            except Exception as e:
                print(f"Error displaying QR code: {e}")
        
        # Instructions
        instructions = MDLabel(
            text="Share the Trip ID with friends to let them join your trip!",
            theme_text_color="Secondary",
            font_style="Body2",
            halign="center"
        )
        content.add_widget(instructions)
        
        content.height = dp(200)
        
        dialog = MDDialog(
            title="Trip Created!",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Share Trip ID",
                    on_release=lambda x: self.share_trip_id(trip_id, dialog)
                ),
                MDRaisedButton(
                    text="Done",
                    on_release=lambda x: [dialog.dismiss(), app.go_back_to_dashboard()]
                )
            ]
        )
        dialog.open()
    
    def share_trip_id(self, trip_id, dialog):
        """Share trip ID (placeholder for actual sharing functionality)"""
        # In a real app, this would use platform-specific sharing
        app = MDApp.get_running_app()
        app.show_success_snackbar(f"Trip ID copied: {trip_id}")
        dialog.dismiss()
        app.go_back_to_dashboard()
