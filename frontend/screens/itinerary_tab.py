from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.button import Button as MDRaisedButton
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.clock import Clock
from datetime import datetime, timedelta

class ActivityCard(MDCard):
    def __init__(self, activity, on_edit_callback=None, on_delete_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.activity = activity
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback
        self.size_hint = (0.9, None)
        self.height = 100
        self.elevation = 2
        self.pos_hint = {'center_x': 0.5}
        self.build_card()
    
    def build_card(self):
        layout = MDBoxLayout(
            orientation='horizontal',
            padding=[10, 10, 10, 10],
            spacing=10
        )
        
        # Activity info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=5
        )
        
        # Title
        title = MDLabel(
            text=self.activity['title'],
            theme_text_color="Primary",
            size_hint_y=None,
            height=25,
            font_style="H6"
        )
        info_layout.add_widget(title)
        
        # Time and location
        time_location = f"🕐 {self.activity['time']} | 📍 {self.activity['location']}"
        time_location_label = MDLabel(
            text=time_location,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=20,
            font_style="Body2"
        )
        info_layout.add_widget(time_location_label)
        
        # Type and cost
        type_cost = f"🏷️ {self.activity['activity_type'].title()}"
        if self.activity.get('cost', 0) > 0:
            type_cost += f" | 💰 ${self.activity['cost']:.2f}"
        
        type_cost_label = MDLabel(
            text=type_cost,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=20,
            font_style="Caption"
        )
        info_layout.add_widget(type_cost_label)
        
        layout.add_widget(info_layout)
        
        # Action buttons
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint_x=None,
            width=80
        )
        
        if self.on_edit_callback:
            edit_btn = MDRaisedButton(
                text="Edit",
                size_hint_y=None,
                height=30,
                on_release=lambda x: self.on_edit_callback(self.activity)
            )
            actions_layout.add_widget(edit_btn)
        
        if self.on_delete_callback:
            delete_btn = MDRaisedButton(
                text="Delete",
                size_hint_y=None,
                height=30,
                on_release=lambda x: self.on_delete_callback(self.activity)
            )
            actions_layout.add_widget(delete_btn)
        
        layout.add_widget(actions_layout)
        
        self.add_widget(layout)

class ItineraryTab(MDBoxLayout):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            kwargs.pop('name')
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [20, 20, 20, 20]
        self.trip = None
        self.activities = []
        self.build_ui()
    
    def build_ui(self):
        # Scroll view
        self.scroll_view = MDScrollView()
        
        # Content container
        self.content_container = MDBoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint_y=None
        )
        self.content_container.bind(minimum_height=self.content_container.setter('height'))
        
        self.scroll_view.add_widget(self.content_container)
        self.add_widget(self.scroll_view)
        
        # Floating action button
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={'right': 0.95, 'bottom': 0.05},
            on_release=self.add_activity
        )
        self.add_widget(self.fab)
    
    def load_trip(self, trip):
        """Load trip data"""
        self.trip = trip
        self.activities = trip.get('activities', [])
        self.update_activities_display()
    
    def update_activities_display(self):
        """Update the activities display"""
        self.content_container.clear_widgets()

        if not self.trip:
            return

        # Generate day headers based on trip dates
        from datetime import datetime, timedelta
        start_date = datetime.fromisoformat(self.trip['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(self.trip['end_date'].replace('Z', '+00:00'))
        num_days = (end_date - start_date).days + 1

        # Group activities by day
        activities_by_day = {}
        for activity in self.activities:
            day = activity.get('day', 1)
            if day not in activities_by_day:
                activities_by_day[day] = []
            activities_by_day[day].append(activity)

        # Display activities by day
        for day in range(1, num_days + 1):
            # Calculate date for this day
            current_date = start_date + timedelta(days=day - 1)
            date_str = current_date.strftime("%b %d, %Y")

            # Day header
            day_label = MDLabel(
                text=f"Day {day} – {date_str}",
                theme_text_color="Primary",
                size_hint_y=None,
                height=40,
                font_style="H5"
            )
            self.content_container.add_widget(day_label)

            # Activities for this day
            day_activities = activities_by_day.get(day, [])
            if day_activities:
                day_activities = sorted(day_activities, key=lambda x: x.get('order', 0))
                for activity in day_activities:
                    card = ActivityCard(
                        activity=activity,
                        on_edit_callback=self.edit_activity,
                        on_delete_callback=self.delete_activity,
                        size_hint_y=None
                    )
                    self.content_container.add_widget(card)
            else:
                # Show add activity prompt
                add_label = MDLabel(
                    text="[+ Add Activity]",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=30,
                    font_style="Body2",
                    halign="center"
                )
                self.content_container.add_widget(add_label)
    
    def add_activity(self, instance):
        """Show add activity dialog"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=400
        )
        
        self.activity_title_field = MDTextField(
            hint_text="Activity Title",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_title_field)
        
        self.activity_time_field = MDTextField(
            hint_text="Time (e.g., 9:00 AM)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_time_field)
        
        self.activity_location_field = MDTextField(
            hint_text="Location",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_location_field)
        
        self.activity_type_field = MDTextField(
            hint_text="Type (food, transport, activity, lodging)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_type_field)
        
        self.activity_cost_field = MDTextField(
            hint_text="Cost ($)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_cost_field)
        
        self.activity_day_field = MDTextField(
            hint_text="Day (1, 2, 3, etc.)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_day_field)
        
        self.activity_notes_field = MDTextField(
            hint_text="Notes (optional)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.activity_notes_field)
        
        self.add_activity_dialog = MDDialog(
            title="Add Activity",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.add_activity_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Add",
                    on_release=self.create_activity
                )
            ]
        )
        self.add_activity_dialog.open()
    
    def create_activity(self, instance):
        """Create new activity"""
        # Get form data
        title = self.activity_title_field.text.strip()
        time = self.activity_time_field.text.strip()
        location = self.activity_location_field.text.strip()
        activity_type = self.activity_type_field.text.strip()
        cost_str = self.activity_cost_field.text.strip()
        day_str = self.activity_day_field.text.strip()
        notes = self.activity_notes_field.text.strip()
        
        # Validate inputs
        if not all([title, time, location, activity_type, day_str]):
            self.show_error("Please fill in all required fields")
            return
        
        try:
            cost = float(cost_str) if cost_str else 0.0
            day = int(day_str)
        except ValueError:
            self.show_error("Invalid cost or day value")
            return
        
        # Prepare activity data
        activity_data = {
            "title": title,
            "time": time,
            "location": location,
            "activity_type": activity_type,
            "cost": cost,
            "day": day,
            "notes": notes,
            "order": len(self.activities)
        }
        
        # Get app instance
        app = MDApp.get_running_app()
        
        # Show loading
        self.show_loading("Adding activity...")
        
        # Make API call
        def do_create(dt):
            trip_id = getattr(self.trip, 'id', None)
            if trip_id is None:
                trip_id = self.trip.get('_id') if isinstance(self.trip, dict) else None
                if trip_id is None:
                    trip_id = self.trip.get('id') if isinstance(self.trip, dict) else None
            if trip_id is None:
                self.hide_loading()
                self.show_error("Trip ID not found")
                return

            result, error = app.api_client.create_activity(str(trip_id), activity_data)
            if result:
                self.hide_loading()
                self.add_activity_dialog.dismiss()
                self.activities.append(result)
                self.update_activities_display()
                app.show_success_dialog("Success", "Activity added successfully!")
            else:
                self.hide_loading()
                self.show_error(f"Failed to add activity: {error}")

        Clock.schedule_once(do_create, 0.1)
    
    def edit_activity(self, activity):
        """Edit activity (placeholder)"""
        dialog = MDDialog(
            title="Edit Activity",
            text="Edit functionality coming soon!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def delete_activity(self, activity):
        """Delete activity"""
        dialog = MDDialog(
            title="Delete Activity",
            text=f"Are you sure you want to delete '{activity['title']}'?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete_activity(activity, dialog)
                )
            ]
        )
        dialog.open()
    
    def confirm_delete_activity(self, activity, dialog):
        """Confirm activity deletion"""
        dialog.dismiss()
        
        app = MDApp.get_running_app()

        def do_delete(dt):
            trip_id = getattr(self.trip, 'id', None)
            if trip_id is None:
                trip_id = self.trip.get('_id') if isinstance(self.trip, dict) else None
                if trip_id is None:
                    trip_id = self.trip.get('id') if isinstance(self.trip, dict) else None
            if trip_id is None:
                app.show_error_dialog("Error", "Trip ID not found")
                return

            result, error = app.api_client.delete_activity(str(trip_id), activity['id'])
            if result:
                self.activities = [a for a in self.activities if a['id'] != activity['id']]
                self.update_activities_display()
                app.show_success_dialog("Success", "Activity deleted successfully!")
            else:
                app.show_error_dialog("Error", f"Failed to delete activity: {error}")

        Clock.schedule_once(do_delete, 0.1)
    
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
