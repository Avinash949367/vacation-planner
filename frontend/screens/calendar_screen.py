from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.button import Button as MDRaisedButton, Button as MDFlatButton
from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime, timedelta
from kivy.uix.button import Button
import calendar

class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
        self.trips = []
        self.build_ui()
    
    def on_enter(self):
        """Called when the screen is entered"""
        super().on_enter()
        # Refresh calendar data when entering the screen with smooth loading
        Clock.schedule_once(lambda dt: self.load_trips(), 0.05)

    def build_ui(self):
        app = MDApp.get_running_app()
        main_layout = MDBoxLayout(orientation='vertical')

        # Top app bar with navigation
        self.top_bar = MDTopAppBar(
            title="Calendar View",
            elevation=4,
            md_bg_color=app.theme_cls.primary_color,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["chevron-left", lambda x: self.previous_month()],
                ["chevron-right", lambda x: self.next_month()],
                ["refresh", lambda x: self.refresh_calendar()]
            ]
        )
        main_layout.add_widget(self.top_bar)

        # Month/Year display with picker
        month_year_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=[dp(20), dp(10), dp(20), dp(10)]
        )
        
        self.month_label = MDLabel(
            text="",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
            size_hint_x=0.8
        )
        month_year_layout.add_widget(self.month_label)
        
        # Month/Year picker button
        picker_btn = MDIconButton(
            icon="calendar-month",
            size_hint_x=0.2,
            on_release=self.show_month_year_picker
        )
        month_year_layout.add_widget(picker_btn)
        
        main_layout.add_widget(month_year_layout)

        # Calendar container
        self.calendar_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        main_layout.add_widget(self.calendar_container)

        self.add_widget(main_layout)

        # Add floating action button for creating new trips
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            on_release=self.create_new_trip
        )
        self.add_widget(self.fab)

        # Load trips and populate calendar
        Clock.schedule_once(lambda dt: self.load_trips(), 0.1)

    def load_trips(self):
        """Load trips from the dashboard screen"""
        app = MDApp.get_running_app()
        
        # Try to get trips from dashboard screen
        if hasattr(app, 'dashboard_screen') and hasattr(app.dashboard_screen, 'trips'):
            self.trips = app.dashboard_screen.trips
            print(f"DEBUG: Loaded {len(self.trips)} trips from dashboard")
        else:
            # Fallback: try to load trips directly from API
            print("DEBUG: Dashboard trips not available, loading from API")
            trips, error = app.api_client.get_trips()
            if isinstance(trips, list):
                self.trips = trips
                print(f"DEBUG: Loaded {len(self.trips)} trips from API")
            else:
                self.trips = []
                print(f"DEBUG: Failed to load trips: {error}")
        
        self.update_calendar()

    def update_calendar(self):
        """Update the calendar display"""
        self.calendar_container.clear_widgets()
        
        # Update month label
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        self.month_label.text = f"{month_names[self.current_date.month - 1]} {self.current_date.year}"
        
        # Create calendar grid
        self.create_calendar_grid()

    def create_calendar_grid(self):
        """Create the calendar grid"""
        year = self.current_date.year
        month = self.current_date.month
        
        # Day headers
        days_header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(2)
        )
        
        day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for day_name in day_names:
            day_label = MDLabel(
                text=day_name,
                theme_text_color="Primary",
                font_style="Body2",
                halign="center",
                size_hint_x=1/7
            )
            days_header.add_widget(day_label)
        
        self.calendar_container.add_widget(days_header)
        
        # Calendar grid
        self.calendar_grid = GridLayout(
            cols=7,
            spacing=dp(2),
            size_hint_y=None
        )
        self.calendar_grid.bind(minimum_height=self.calendar_grid.setter('height'))
        
        # Get calendar data
        first_day = datetime(year, month, 1)
        start_weekday = first_day.weekday()  # Monday=0
        start_weekday = (start_weekday + 1) % 7  # Convert to Sunday=0
        days_in_month = calendar.monthrange(year, month)[1]
        
        # Fill empty cells before first day
        for _ in range(start_weekday):
            empty_cell = MDLabel(text="")
            self.calendar_grid.add_widget(empty_cell)
        
        # Add day cells
        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            day_cell = self.create_day_cell(day, date_str)
            self.calendar_grid.add_widget(day_cell)
        
        self.calendar_container.add_widget(self.calendar_grid)

    def create_day_cell(self, day, date_str):
        """Create a day cell with trip indicators"""
        app = MDApp.get_running_app()
        
        # Check if there are trips on this date
        trips_on_date = self.get_trips_on_date(date_str)
        has_trips = len(trips_on_date) > 0
        
        # Create day card
        day_card = MDCard(
            size_hint_y=None,
            height=dp(60),
            elevation=2 if has_trips else 1,
            radius=[8],
            md_bg_color=app.theme_cls.primary_color if has_trips else (0.95, 0.95, 0.95, 1),
            on_release=lambda x, d=date_str: self.show_trips_for_date(d)
        )
        
        # Day content
        day_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            padding=[dp(4), dp(4), dp(4), dp(4)]
        )
        
        # Day number
        day_label = MDLabel(
            text=str(day),
            theme_text_color="Primary" if has_trips else "Secondary",
            font_style="Body1",
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        day_content.add_widget(day_label)
        
        # Trip indicators
        if has_trips:
            trip_count = len(trips_on_date)
            if trip_count == 1:
                trip_text = trips_on_date[0].get('title', 'Trip')[:8]
            else:
                trip_text = f"{trip_count} trips"
            
            trip_label = MDLabel(
                text=trip_text,
                theme_text_color="Primary",
                font_style="Caption",
                halign="center",
                size_hint_y=None,
                height=dp(15)
            )
            day_content.add_widget(trip_label)
        
        day_card.add_widget(day_content)
        return day_card

    def get_trips_on_date(self, date_str):
        """Get trips that occur on a specific date"""
        trips_on_date = []
        for trip in self.trips:
            start_date = trip.get('start_date', '')[:10]
            end_date = trip.get('end_date', '')[:10]
            if start_date <= date_str <= end_date:
                trips_on_date.append(trip)
        return trips_on_date

    def show_trips_for_date(self, date_str):
        """Show detailed trip information for a specific date"""
        trips_on_date = self.get_trips_on_date(date_str)
        
        if not trips_on_date:
            # No trips dialog
            dialog = MDDialog(
                title=f"No trips on {date_str}",
                text="You don't have any trips scheduled for this date.",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return
        
        # Create detailed trip dialog
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Date header
        date_label = MDLabel(
            text=f"Trips on {date_str}",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(date_label)
        
        # Trip cards
        for trip in trips_on_date:
            trip_card = self.create_trip_card(trip)
            content.add_widget(trip_card)
        
        content.height = dp(200 + len(trips_on_date) * 100)
        
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

    def create_trip_card(self, trip):
        """Create a trip card for the dialog"""
        app = MDApp.get_running_app()
        
        trip_card = MDCard(
            size_hint_y=None,
            height=dp(80),
            elevation=2,
            radius=[8],
            padding=[dp(12), dp(12), dp(12), dp(12)]
        )
        
        trip_content = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(12)
        )
        
        # Trip icon
        icon = MDIconButton(
            icon="airplane",
            size_hint_x=None,
            width=dp(40),
            theme_icon_color="Primary"
        )
        trip_content.add_widget(icon)
        
        # Trip details
        details = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4)
        )
        
        # Title
        title = MDLabel(
            text=trip.get('title', 'Unknown Trip'),
            theme_text_color="Primary",
            font_style="Body1"
        )
        details.add_widget(title)
        
        # Destination and dates
        destination = MDLabel(
            text=f"📍 {trip.get('destination', 'Unknown Destination')}",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        details.add_widget(destination)
        
        # Duration
        start_date = trip.get('start_date', '')[:10]
        end_date = trip.get('end_date', '')[:10]
        duration = MDLabel(
            text=f"📅 {start_date} to {end_date}",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        details.add_widget(duration)
        
        trip_content.add_widget(details)
        trip_card.add_widget(trip_content)
        
        return trip_card

    def previous_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def show_month_year_picker(self, instance):
        """Show month and year picker dialog"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
            size_hint_y=None
        )
        
        # Title
        title = MDLabel(
            text="Select Month & Year",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        content.add_widget(title)
        
        # Month selection
        month_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        month_label = MDLabel(
            text="Month:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        month_layout.add_widget(month_label)
        
        # Month dropdown
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        self.month_spinner = MDBoxLayout(
            orientation='horizontal',
            size_hint_x=0.7,
            spacing=dp(5)
        )
        
        # Previous month button
        prev_month_btn = MDIconButton(
            icon="chevron-left",
            size_hint_x=None,
            width=dp(40),
            on_release=lambda x: self.change_month(-1)
        )
        self.month_spinner.add_widget(prev_month_btn)
        
        # Current month display
        self.current_month_label = MDLabel(
            text=month_names[self.current_date.month - 1],
            theme_text_color="Primary",
            font_style="Body1",
            halign="center",
            size_hint_x=1
        )
        self.month_spinner.add_widget(self.current_month_label)
        
        # Next month button
        next_month_btn = MDIconButton(
            icon="chevron-right",
            size_hint_x=None,
            width=dp(40),
            on_release=lambda x: self.change_month(1)
        )
        self.month_spinner.add_widget(next_month_btn)
        
        month_layout.add_widget(self.month_spinner)
        content.add_widget(month_layout)
        
        # Year selection
        year_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        year_label = MDLabel(
            text="Year:",
            theme_text_color="Primary",
            size_hint_x=0.3
        )
        year_layout.add_widget(year_label)
        
        # Year input
        from kivymd.uix.textfield import MDTextField
        self.year_field = MDTextField(
            text=str(self.current_date.year),
            hint_text="Year",
            mode="rectangle",
            size_hint_x=0.7,
            input_filter="int"
        )
        year_layout.add_widget(self.year_field)
        
        content.add_widget(year_layout)
        
        content.height = dp(200)
        
        # Create dialog
        self.picker_dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: self.picker_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Apply",
                    on_release=self.apply_date_selection
                )
            ]
        )
        self.picker_dialog.open()

    def change_month(self, direction):
        """Change month in the picker"""
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        new_month = self.current_date.month + direction
        if new_month < 1:
            new_month = 12
        elif new_month > 12:
            new_month = 1
        
        self.current_date = self.current_date.replace(month=new_month)
        self.current_month_label.text = month_names[new_month - 1]

    def apply_date_selection(self, instance):
        """Apply the selected month and year"""
        try:
            year = int(self.year_field.text)
            if 2020 <= year <= 2030:  # Reasonable year range
                self.current_date = self.current_date.replace(year=year)
                self.picker_dialog.dismiss()
                self.update_calendar()
            else:
                app = MDApp.get_running_app()
                app.show_error_snackbar("Please enter a year between 2020 and 2030")
        except ValueError:
            app = MDApp.get_running_app()
            app.show_error_snackbar("Please enter a valid year")

    def refresh_calendar(self):
        """Refresh the calendar with latest trip data"""
        self.load_trips()

    def create_new_trip(self, instance):
        """Navigate to create trip screen"""
        app = MDApp.get_running_app()
        app.open_create_trip()

    def go_back(self):
        """Go back to dashboard"""
        app = MDApp.get_running_app()
        app.screen_manager.current = 'dashboard'
