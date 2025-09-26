from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button as MDFloatingActionButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.clock import Clock
from kivy.animation import Animation
from datetime import datetime, timedelta
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.uix.button import Button
import os

# Custom card with modern elevation and shadow
class ModernCard(MDCard, CommonElevationBehavior):
    pass

class TripCard(ModernCard):
    def __init__(self, trip, on_tap_callback, **kwargs):
        super().__init__(**kwargs)
        self.trip = trip
        self.on_tap_callback = on_tap_callback
        self.size_hint_y = None
        self.height = dp(140)  # Reduced height for better performance
        self.elevation = 2  # Reduced elevation
        self.radius = [12]  # Slightly smaller radius
        self.ripple_behavior = True
        self.padding = [12, 12, 12, 12]
        self.build_card()
    
    def build_card(self):
        layout = MDBoxLayout(orientation='horizontal', padding=[0, 0, 0, 0], spacing=10)
        
        # Trip icon instead of destination photo
        icon_box = MDBoxLayout(
            size_hint_x=None, 
            width=dp(100),
            orientation='vertical',
            padding=0,
            md_bg_color=(0.1, 0.1, 0.1, 0.05),
            radius=[12]
        )

        # Trip icon
        trip_icon = MDIconButton(
            icon="airplane",
            size_hint=(1, 1),
            theme_icon_color="Primary",
            icon_size=dp(48)
        )
        icon_box.add_widget(trip_icon)
        layout.add_widget(icon_box)
        
        # Text content
        content = MDBoxLayout(orientation='vertical', spacing=6, size_hint_x=0.7)
        
        # Trip title
        title = MDLabel(
            text=self.trip['title'],
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(28),
            font_style="Body1"
        )
        content.add_widget(title)
        
        # Destination with icon
        dest_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24), spacing=5)
        icon = MDIconButton(
            icon="map-marker-outline", 
            size_hint_x=None, 
            width=dp(24),
            theme_icon_color="Secondary",
            icon_size=dp(18)
        )
        dest_box.add_widget(icon)
        
        destination = MDLabel(
            text=self.trip['destination'],
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
            font_style="Body2"
        )
        dest_box.add_widget(destination)
        content.add_widget(dest_box)
        
        # Dates
        start_date = datetime.fromisoformat(self.trip['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(self.trip['end_date'].replace('Z', '+00:00'))
        date_text = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
        
        date_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(22), spacing=5)
        date_icon = MDIconButton(
            icon="calendar-range", 
            size_hint_x=None, 
            width=dp(24),
            theme_icon_color="Secondary",
            icon_size=dp(16)
        )
        date_box.add_widget(date_icon)
        
        dates = MDLabel(
            text=date_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(18),
            font_style="Caption"
        )
        date_box.add_widget(dates)
        content.add_widget(date_box)
        
        # Countdown or status chip
        now = datetime.now()
        if start_date > now:
            days_left = (start_date - now).days
            status_text = f"Starts in {days_left} days"
            chip_icon = "clock-outline"
            chip_color = (0.2, 0.6, 1, 1)  # Blue
        elif end_date > now:
            status_text = "Ongoing"
            chip_icon = "run"
            chip_color = (0.2, 0.8, 0.4, 1)  # Green
        else:
            status_text = "Completed"
            chip_icon = "check-circle-outline"
            chip_color = (0.6, 0.6, 0.6, 1)  # Gray

        # Status chip and share button
        status_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(28),
            spacing=dp(8)
        )

        chip = MDChip(
            text=status_text, 
            icon_left=chip_icon,
            md_bg_color=chip_color,
            text_color=(1, 1, 1, 1),
            icon_left_color=(1, 1, 1, 1),
            size_hint=(None, None),
            height=dp(28),
            padding=[8, 0, 8, 0]
        )
        status_row.add_widget(chip)
        
        content.add_widget(status_row)

        # Quick actions
        actions_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(32),
            spacing=5,
            padding=[0, 5, 0, 0]
        )

        edit_btn = MDIconButton(
            icon="pencil",
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            theme_icon_color="Secondary",
            on_release=lambda x: self.edit_trip(self.trip)
        )
        actions_box.add_widget(edit_btn)

        delete_btn = MDIconButton(
            icon="delete",
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            theme_icon_color="Error",
            on_release=lambda x: self.confirm_delete_trip(self.trip)
        )
        actions_box.add_widget(delete_btn)

        content.add_widget(actions_box)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_tap_callback(self.trip)
            return True
        return super().on_touch_down(touch)

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trips = []
        self.filtered_trips = []
        self.query = ""
        self.active_filter = "All"
        self.sort_order = "Recent"
        self.is_loading = False
        self.filter_chips = []
        self.build_ui()
    
    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=0
        )
        
        # Top app bar with modern styling
        app = MDApp.get_running_app()
        self.top_bar = MDTopAppBar(
            title="My Trips",
            elevation=2,
            md_bg_color=app.theme_cls.primary_color,
            left_action_items=[["menu", lambda x: self.show_menu(x)]],
            right_action_items=[
                ["magnify", lambda x: self.focus_search()],
                ["account-circle", lambda x: self.show_profile_menu(x)]
            ],
            specific_text_color=(1, 1, 1, 1)
        )
        
        main_layout.add_widget(self.top_bar)

        # Add spacer to separate from top bar
        spacer = MDBoxLayout(size_hint_y=None, height=dp(20))
        main_layout.add_widget(spacer)

        # Search and filter section with proper spacing
        search_filter_box = MDBoxLayout(
            orientation='vertical', 
            padding=[dp(16), dp(16), dp(16), dp(16)], 
            spacing=dp(12), 
            size_hint_y=None,
            height=dp(140),
            md_bg_color=(0.95, 0.95, 0.95, 1)
        )

        # Search field with modern styling
        self.search_field = MDTextField(
            hint_text='Search trips...',
            icon_left='magnify',
            mode="round",
            size_hint_x=1,
            height=dp(48),
            font_size=dp(16),
            line_color_normal=(0.7, 0.7, 0.7, 1),
            line_color_focus=app.theme_cls.primary_color
        )
        self.search_field.bind(text=lambda *_: self.apply_filters())
        search_filter_box.add_widget(self.search_field)

        # Filter chips with modern styling
        chips_box = MDBoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(36))
        
        filter_options = [
            {"label": "All", "icon": "view-grid-outline"},
            {"label": "Upcoming", "icon": "clock-outline"},
            {"label": "Ongoing", "icon": "run"},
            {"label": "Completed", "icon": "check-circle-outline"}
        ]
        
        for option in filter_options:
            chip = MDChip(
                text=option["label"],
                icon_left=option["icon"],
                text_color=app.theme_cls.primary_color if option["label"] == self.active_filter else (0.7, 0.7, 0.7, 1)
            )
            chip.bind(on_release=lambda x, label=option["label"]: self.set_filter(label))
            chips_box.add_widget(chip)
            self.filter_chips.append(chip)

        search_filter_box.add_widget(chips_box)

        # Sort toggle
        sort_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(36),
            pos_hint={'right': 1}
        )

        sort_label = MDLabel(
            text="Sort:",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=None,
            width=dp(40)
        )
        sort_box.add_widget(sort_label)

        self.sort_chip = MDChip(
            text="Recent",
            icon_left="sort-descending",
            size_hint_x=None,
            width=dp(90),
            on_release=self.on_sort_chip_release
        )
        sort_box.add_widget(self.sort_chip)

        search_filter_box.add_widget(sort_box)

        main_layout.add_widget(search_filter_box)

        # Scroll view for trips
        self.scroll_view = MDScrollView()
        
        # Trips container
        self.trips_container = MDGridLayout(
            cols=1,
            spacing=dp(15),
            padding=[dp(20), dp(15), dp(20), dp(80)],  # Extra bottom padding for FAB
            size_hint_y=None,
            adaptive_height=True
        )
        self.trips_container.bind(minimum_height=self.trips_container.setter('height'))
        
        self.scroll_view.add_widget(self.trips_container)
        main_layout.add_widget(self.scroll_view)
        
        # Custom bottom navigation with 5-tab layout
        self.bottom_nav_card = MDCard(
            size_hint_y=None,
            height=dp(80),
            md_bg_color=(1, 1, 1, 1),  # White background
            radius=[dp(20), dp(20), 0, 0],  # Rounded top corners
            elevation=4
        )

        self.bottom_nav_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            spacing=dp(0)
        )
        self.bottom_nav_card.add_widget(self.bottom_nav_layout)

        # Home tab
        self.home_tab = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            padding=[dp(4), dp(8), dp(4), dp(8)],
            spacing=dp(4)
        )
        home_icon = MDIconButton(
            icon='home',
            size_hint=(1, None),
            height=dp(24),
            theme_icon_color="Custom",
            icon_color=app.theme_cls.primary_color,  # Active color
            on_release=self.on_home_press
        )
        home_label = MDLabel(
            text="Home",
            size_hint=(1, None),
            height=dp(16),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=app.theme_cls.primary_color,
            halign="center"
        )
        self.home_tab.add_widget(home_icon)
        self.home_tab.add_widget(home_label)
        self.bottom_nav_layout.add_widget(self.home_tab)

        # Explore tab
        self.explore_tab = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            padding=[dp(4), dp(8), dp(4), dp(8)],
            spacing=dp(4)
        )
        explore_icon = MDIconButton(
            icon='compass-outline',
            size_hint=(1, None),
            height=dp(24),
            theme_icon_color="Custom",
            icon_color=(0.6, 0.6, 0.6, 1),  # Inactive color
            on_release=self.on_explore_press
        )
        explore_label = MDLabel(
            text="Explore",
            size_hint=(1, None),
            height=dp(16),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.6, 0.6, 0.6, 1),
            halign="center"
        )
        self.explore_tab.add_widget(explore_icon)
        self.explore_tab.add_widget(explore_label)
        self.bottom_nav_layout.add_widget(self.explore_tab)

        # Plus tab
        self.plus_tab = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            padding=[dp(4), dp(8), dp(4), dp(8)],
            spacing=dp(4)
        )
        plus_icon = MDIconButton(
            icon='plus',
            size_hint=(1, None),
            height=dp(24),
            theme_icon_color="Custom",
            icon_color=app.theme_cls.primary_color,  # Highlighted color
            on_release=self.show_new_trip_menu
        )
        plus_label = MDLabel(
            text="NEW",
            size_hint=(1, None),
            height=dp(16),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=app.theme_cls.primary_color,
            halign="center"
        )
        self.plus_tab.add_widget(plus_icon)
        self.plus_tab.add_widget(plus_label)
        self.bottom_nav_layout.add_widget(self.plus_tab)

        # Calendar tab
        self.calendar_tab = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            padding=[dp(4), dp(8), dp(4), dp(8)],
            spacing=dp(4)
        )
        calendar_icon = MDIconButton(
            icon='calendar-outline',
            size_hint=(1, None),
            height=dp(24),
            theme_icon_color="Custom",
            icon_color=(0.6, 0.6, 0.6, 1),  # Inactive color
            on_release=self.on_calendar_press
        )
        calendar_label = MDLabel(
            text="Calendar",
            size_hint=(1, None),
            height=dp(16),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.6, 0.6, 0.6, 1),
            halign="center"
        )
        self.calendar_tab.add_widget(calendar_icon)
        self.calendar_tab.add_widget(calendar_label)
        self.bottom_nav_layout.add_widget(self.calendar_tab)

        # Settings tab
        self.settings_tab = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            padding=[dp(4), dp(8), dp(4), dp(8)],
            spacing=dp(4)
        )
        settings_icon = MDIconButton(
            icon='cog-outline',
            size_hint=(1, None),
            height=dp(24),
            theme_icon_color="Custom",
            icon_color=(0.6, 0.6, 0.6, 1),  # Inactive color
            on_release=self.on_settings_press
        )
        settings_label = MDLabel(
            text="Settings",
            size_hint=(1, None),
            height=dp(16),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.6, 0.6, 0.6, 1),
            halign="center"
        )
        self.settings_tab.add_widget(settings_icon)
        self.settings_tab.add_widget(settings_label)
        self.bottom_nav_layout.add_widget(self.settings_tab)

        main_layout.add_widget(self.bottom_nav_card)
        
        self.add_widget(main_layout)
        
        # Load trips after UI is built
        Clock.schedule_once(lambda dt: self.load_trips(), 0.5)
    
        # Initialize active tab
        self.current_tab = 'home'
        self.update_tab_icons()

    def focus_search(self):
        """Focus on the search field"""
        self.search_field.focus = True
    
    def load_trips(self):
        """Load trips from API with smooth loading"""
        app = MDApp.get_running_app()
        
        def do_load(dt):
            self.is_loading = True
            self.show_loading_placeholders()
            
            # Check if user is authenticated
            if not app.store.exists('access_token'):
                self.trips = []
                self.is_loading = False
                self.update_trips_display()
                return
            
            trips, error = app.api_client.get_trips()
            
            if isinstance(trips, list):
                self.trips = trips
                self.is_loading = False
                # Use animation for smooth transition
                Clock.schedule_once(lambda dt: self.apply_filters(), 0.1)
            else:
                # Show error message to user
                self.trips = []
                self.is_loading = False
                self.update_trips_display()
                
                # Show error to user
                if error:
                    app.show_error_snackbar(f"Failed to load trips: {error}")
        
        Clock.schedule_once(do_load, 0.05)  # Reduced delay for faster response

    def set_filter(self, label):
        self.active_filter = label
        # Update chip colors
        app = MDApp.get_running_app()
        for chip in self.filter_chips:
            if hasattr(chip, 'text'):
                chip.text_color = app.theme_cls.primary_color if chip.text == label else (0.7, 0.7, 0.7, 1)
        self.apply_filters()

    def on_sort_chip_release(self, instance):
        """Toggle sort order"""
        if self.sort_order == "Recent":
            self.sort_order = "Alphabetical"
            self.sort_chip.text = "A-Z"
            self.sort_chip.icon_left = "sort-alphabetical-ascending"
        else:
            self.sort_order = "Recent"
            self.sort_chip.text = "Recent"
            self.sort_chip.icon_left = "sort-descending"
        self.apply_filters()

    def apply_filters(self):
        """Filter trips by search query and status."""
        q = (self.search_field.text or "").strip().lower()
        now = datetime.now()
        result = []
        for t in self.trips:
            title_match = q in t.get('title', '').lower() or q in t.get('destination', '').lower()
            if not title_match:
                continue
            start = datetime.fromisoformat(t['start_date'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(t['end_date'].replace('Z', '+00:00'))
            status = 'Upcoming' if start > now else ('Ongoing' if end > now else 'Completed')
            if self.active_filter != 'All' and status != self.active_filter:
                continue
            result.append(t)

        # Sort results
        if self.sort_order == "Recent":
            result.sort(key=lambda x: datetime.fromisoformat(x['start_date'].replace('Z', '+00:00')), reverse=True)
        else:  # Alphabetical
            result.sort(key=lambda x: x.get('title', '').lower())

        self.filtered_trips = result
        self.update_trips_display()
    
    def update_trips_display(self):
        """Update the trips display with smooth animations"""
        # Clear existing trips with fade out animation
        if hasattr(self, 'trips_container') and self.trips_container.children:
            for child in self.trips_container.children[:]:
                anim = Animation(opacity=0, duration=0.2)
                anim.bind(on_complete=lambda *args, widget=child: self.trips_container.remove_widget(widget))
                anim.start(child)
        
        # Schedule the new content to appear after clearing
        Clock.schedule_once(lambda dt: self._add_trip_cards(), 0.2)
    
    def _add_trip_cards(self):
        """Add trip cards with smooth animations"""
        self.trips_container.clear_widgets()
        
        if self.is_loading:
            # Loading placeholders with modern skeleton UI
            for _ in range(3):
                placeholder = ModernCard(
                    size_hint_y=None, 
                    height=dp(160), 
                    elevation=2,
                    padding=[10, 10, 10, 10]
                )
                box = MDBoxLayout(orientation='horizontal', spacing=10)
                
                # Image placeholder
                img_placeholder = MDBoxLayout(
                    size_hint_x=None, 
                    width=dp(100),
                    md_bg_color=(0.9, 0.9, 0.9, 1),
                    radius=[12]
                )
                box.add_widget(img_placeholder)
                
                # Content placeholder
                content = MDBoxLayout(orientation='vertical', spacing=6)
                for i in range(4):
                    line = MDBoxLayout(
                        size_hint_y=None, 
                        height=dp(20 if i == 0 else 15),
                        md_bg_color=(0.9, 0.9, 0.9, 1),
                        radius=[4]
                    )
                    content.add_widget(line)
                
                box.add_widget(content)
                placeholder.add_widget(box)
                self.trips_container.add_widget(placeholder)
            return

        visible = self.filtered_trips if self.search_field.text or self.active_filter != 'All' else self.trips

        if not visible:
            # Modern empty state
            # Remove padding for empty state to fill the space
            original_padding = self.trips_container.padding
            self.trips_container.padding = [0, 0, 0, 0]

            empty_box = MDBoxLayout(size_hint_y=1)

            from kivy.uix.floatlayout import FloatLayout
            content_layout = FloatLayout(size_hint=(1, 1))

            # Centered content
            content_box = MDBoxLayout(
                orientation='vertical',
                spacing=dp(20),
                size_hint=(None, None),
                size=(dp(300), dp(200)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            
            # Illustration icon - use plane icon
            icon = MDIconButton(
                icon="airplane",
                icon_size=dp(80),
                theme_icon_color="Secondary",
                size_hint=(1, None),
                height=dp(80),
                disabled=True
            )
            content_box.add_widget(icon)
            
            # Title
            title = MDLabel(
                text="No trips planned yet",
                theme_text_color="Primary",
                size_hint=(1, None),
                height=dp(36),
                font_style="H5",
                bold=True,
                halign="center"
            )
            content_box.add_widget(title)
            
            # Description
            desc = MDLabel(
                text="Tap + NEW to start your adventure!",
                theme_text_color="Secondary",
                size_hint=(1, None),
                height=dp(24),
                font_style="Body1",
                halign="center"
            )
            content_box.add_widget(desc)
            
            # Action button
            create_btn = MDRaisedButton(
                text="Create your first trip",
                size_hint=(None, None),
                size=(dp(200), dp(48)),
                pos_hint={'center_x': 0.5},
                on_release=self.create_trip
            )
            content_box.add_widget(create_btn)

            content_layout.add_widget(content_box)
            empty_box.add_widget(content_layout)
            
            self.trips_container.add_widget(empty_box)
        else:
            # Add trip cards with animation
            for i, trip in enumerate(visible):
                card = TripCard(
                    trip=trip,
                    on_tap_callback=self.open_trip,
                    size_hint_y=None
                )
                card.opacity = 0
                self.trips_container.add_widget(card)
                # Staggered animation
                anim = Animation(opacity=1, duration=0.3, t='out_quad')
                Clock.schedule_once(lambda dt, c=card, a=anim: a.start(c), i * 0.1)

    def show_loading_placeholders(self):
        self.update_trips_display()  # Reuse the loading state from update_trips_display
    
    def open_trip(self, trip):
        """Open trip detail screen"""
        app = MDApp.get_running_app()
        app.open_trip_detail(trip)
    
    def create_trip(self, instance):
        """Open create trip screen"""
        app = MDApp.get_running_app()
        app.open_create_trip()
    
    def join_trip(self, instance):
        """Open join trip screen"""
        app = MDApp.get_running_app()
        app.open_join_trip()
    

    def edit_trip(self, trip):
        """Open create trip screen with trip data for editing"""
        app = MDApp.get_running_app()
        app.create_trip_screen.title_field.text = trip.get('title', '')
        app.create_trip_screen.destination_field.text = trip.get('destination', '')
        app.create_trip_screen.start_date_field.text = trip.get('start_date', '')[:10]
        app.create_trip_screen.end_date_field.text = trip.get('end_date', '')[:10]
        app.create_trip_screen.budget_field.text = str(trip.get('budget', ''))
        app.screen_manager.current = 'create_trip'
        app.create_trip_screen.editing_trip = trip

    def confirm_delete_trip(self, trip):
        """Show confirmation dialog before deleting trip"""
        app = MDApp.get_running_app()
        from kivymd.uix.dialog import MDDialog
        if hasattr(self, 'delete_dialog') and self.delete_dialog:
            self.delete_dialog.dismiss()
        self.delete_dialog = MDDialog(
            title="Delete Trip",
            text=f"Are you sure you want to delete the trip '{trip.get('title', '')}'?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.delete_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.delete_trip(trip)
                )
            ]
        )
        self.delete_dialog.open()

    def delete_trip(self, trip):
        """Delete trip and refresh list"""
        app = MDApp.get_running_app()
        self.delete_dialog.dismiss()
        def do_delete(dt):
            success, error = app.api_client.delete_trip(trip.get('id'))
            if success:
                app.show_success_snackbar("Trip deleted successfully")
                self.load_trips()
            else:
                app.show_error_snackbar(f"Failed to delete trip: {error}")
        from kivy.clock import Clock
        Clock.schedule_once(do_delete, 0.1)


    def open_nav_drawer(self):
        """Open the navigation drawer"""
        app = MDApp.get_running_app()
        app.nav_drawer.set_state("open")
    
    def open_calendar(self):
        """Open calendar screen"""
        app = MDApp.get_running_app()
        app.screen_manager.current = 'calendar'
    
    def show_settings(self):
        """Show settings dialog"""
        app = MDApp.get_running_app()
        content = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=[dp(0), dp(8), dp(0), dp(8)], size_hint_y=None)
        content.height = dp(120)
        
        
        # Notifications setting
        notif_box = MDBoxLayout(orientation='horizontal', spacing=dp(12), size_hint_y=None, height=dp(48))
        notif_label = MDLabel(text="Notifications", size_hint_x=None, width=dp(120), theme_text_color="Primary")
        notif_switch = MDSwitch(active=True, pos_hint={'center_y': 0.5})
        notif_box.add_widget(notif_label)
        notif_box.add_widget(notif_switch)
        content.add_widget(notif_box)

        dialog = MDDialog(
            title="[size=20]Settings[/size]",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SAVE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_profile(self):
        """Show profile dialog"""
        app = MDApp.get_running_app()
        user = app.current_user or {}
        content = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=[dp(0), dp(8), dp(0), dp(8)], size_hint_y=None)
        content.height = dp(100)

        # User info
        name_label = MDLabel(text=f"Name: {user.get('name', 'N/A')}", theme_text_color="Primary")
        email_label = MDLabel(text=f"Email: {user.get('email', 'N/A')}", theme_text_color="Secondary")
        content.add_widget(name_label)
        content.add_widget(email_label)

        dialog = MDDialog(
            title="[size=20]Profile[/size]",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="LOGOUT",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.error_color,
                    on_release=lambda x: self.logout(x)
                ),
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_help(self):
        """Show help dialog"""
        app = MDApp.get_running_app()
        content = MDLabel(
            text="TravelMate helps you plan and organize your trips.\n\nCreate trips, add itinerary items, track your budget, and build packing lists all in one place.",
            size_hint_y=None,
            valign="top"
        )
        content.bind(texture_size=content.setter('size'))
        
        dialog = MDDialog(
            title="[size=20]Help & Feedback[/size]",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="GOT IT",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def update_tab_icons(self):
        """Update tab icons and labels based on current tab"""
        app = MDApp.get_running_app()
        active_color = app.theme_cls.primary_color
        inactive_color = (0.6, 0.6, 0.6, 1)

        # Home tab
        home_icon = self.home_tab.children[1]  # Icon is second child (added last)
        home_label = self.home_tab.children[0]  # Label is first child
        if self.current_tab == 'home':
            home_icon.icon = 'home'
            home_icon.icon_color = active_color
            home_label.text_color = active_color
        else:
            home_icon.icon = 'home-outline'
            home_icon.icon_color = inactive_color
            home_label.text_color = inactive_color

        # Explore tab
        explore_icon = self.explore_tab.children[1]
        explore_label = self.explore_tab.children[0]
        if self.current_tab == 'explore':
            explore_icon.icon = 'compass'
            explore_icon.icon_color = active_color
            explore_label.text_color = active_color
        else:
            explore_icon.icon = 'compass-outline'
            explore_icon.icon_color = inactive_color
            explore_label.text_color = inactive_color

        # Calendar tab
        calendar_icon = self.calendar_tab.children[1]
        calendar_label = self.calendar_tab.children[0]
        if self.current_tab == 'calendar':
            calendar_icon.icon = 'calendar'
            calendar_icon.icon_color = active_color
            calendar_label.text_color = active_color
        else:
            calendar_icon.icon = 'calendar-outline'
            calendar_icon.icon_color = inactive_color
            calendar_label.text_color = inactive_color

        # Settings tab
        settings_icon = self.settings_tab.children[1]
        settings_label = self.settings_tab.children[0]
        if self.current_tab == 'settings':
            settings_icon.icon = 'cog'
            settings_icon.icon_color = active_color
            settings_label.text_color = active_color
        else:
            settings_icon.icon = 'cog-outline'
            settings_icon.icon_color = inactive_color
            settings_label.text_color = inactive_color

    def on_home_press(self, instance):
        """Handle home tab press"""
        self.current_tab = 'home'
        self.update_tab_icons()
        self.load_trips()

    def on_calendar_press(self, instance):
        """Handle calendar tab press"""
        self.current_tab = 'calendar'
        self.update_tab_icons()
        self.open_calendar()

    def on_explore_press(self, instance):
        """Handle explore tab press"""
        self.current_tab = 'explore'
        self.update_tab_icons()
        # Show explore dialog
        app = MDApp.get_running_app()
        dialog = MDDialog(
            title="Explore",
            text="Discover new destinations and get travel inspiration!",
            buttons=[
                MDRaisedButton(
                    text="Browse Destinations",
                    on_release=lambda x: self.browse_destinations()
                ),
                MDFlatButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def on_settings_press(self, instance):
        """Handle settings tab press"""
        self.current_tab = 'settings'
        self.update_tab_icons()
        self.show_settings()



    def get_responsive_sizes(self):
        """Get responsive sizes based on screen width"""
        screen_width = Window.size[0]
        screen_height = Window.size[1]

        # Responsive scaling factor
        if screen_width < 400:  # Small phones
            scale = 0.8
            dialog_width_hint = 0.98
            dialog_height = dp(280)
            content_padding = dp(6)
            button_spacing = dp(12)
            button_padding = [dp(6), 0, dp(6), 0]
        elif screen_width < 600:  # Medium phones/tablets
            scale = 0.9
            dialog_width_hint = 0.95
            dialog_height = dp(320)
            content_padding = dp(8)
            button_spacing = dp(16)
            button_padding = [dp(8), 0, dp(8), 0]
        else:  # Large tablets/desktops
            scale = 1.0
            dialog_width_hint = 0.9
            dialog_height = dp(360)
            content_padding = dp(12)
            button_spacing = dp(20)
            button_padding = [dp(12), 0, dp(12), 0]

        return {
            'scale': scale,
            'dialog_width_hint': dialog_width_hint,
            'dialog_height': dialog_height,
            'content_padding': content_padding,
            'button_spacing': button_spacing,
            'button_padding': button_padding
        }

    def show_new_trip_menu(self, instance):
        """Show menu for new trip options"""
        app = MDApp.get_running_app()

        # Get responsive sizes
        sizes = self.get_responsive_sizes()

        # Create dialog content with improved layout
        content = MDBoxLayout(
            orientation='vertical',
            spacing=sizes['content_padding'],
            padding=[sizes['content_padding'], sizes['content_padding'], sizes['content_padding'], sizes['content_padding']],
            size_hint_y=None,
            height=dp(280)
        )

        # Top bar with close button on left
        top_bar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20) * sizes['scale']
        )

        # Close button on left
        close_btn = MDIconButton(
            icon="close",
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            theme_icon_color="Secondary",
            on_release=lambda x: self.new_trip_dialog.dismiss()
        )
        top_bar.add_widget(close_btn)

        # Spacer
        top_bar.add_widget(MDBoxLayout(size_hint_x=1))

        content.add_widget(top_bar)

        # Title
        title = MDLabel(
            text="Let's Get Started!",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(40) * sizes['scale'],
            halign="center",
            bold=True,
            font_size=dp(20) * sizes['scale']
        )
        content.add_widget(title)

        # Subtitle
        subtitle = MDLabel(
            text="Would you like to create a new trip or join an existing one?",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(40) * sizes['scale'],
            halign="center",
            font_size=dp(14) * sizes['scale']
        )
        content.add_widget(subtitle)

        # Buttons box with create and join buttons aligned horizontally
        buttons_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48) * sizes['scale'],
            spacing=sizes['button_spacing'],
            padding=sizes['button_padding']
        )

        # Create Trip button with icon inside
        create_btn = MDFillRoundFlatIconButton(
            text="Create Trip",
            size_hint=(0.5, 1),
            icon="airplane",
            on_release=self.on_create_trip_option,
            md_bg_color=app.theme_cls.primary_color,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size=dp(14) * sizes['scale']
        )
        buttons_box.add_widget(create_btn)

        # Join Trip button with icon inside
        join_btn = MDFillRoundFlatIconButton(
            text="Join Trip",
            size_hint=(0.5, 1),
            icon="account-plus",
            on_release=self.on_join_trip_option,
            md_bg_color=(0.3, 0.5, 0.8, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size=dp(14) * sizes['scale']
        )
        buttons_box.add_widget(join_btn)

        content.add_widget(buttons_box)

        # Dialog
        self.new_trip_dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            size_hint=(sizes['dialog_width_hint'], None),
            height=sizes['dialog_height'],
            radius=[dp(20), dp(20), dp(20), dp(20)],
            auto_dismiss=False
        )

        # Add fade-in animation
        self.new_trip_dialog.opacity = 0
        anim = Animation(opacity=1, duration=0.3, t='out_quad')
        self.new_trip_dialog.open()
        anim.start(self.new_trip_dialog)

    def on_create_trip_option(self, instance):
        """Handle create trip from menu"""
        if hasattr(self, 'new_trip_dialog'):
            self.new_trip_dialog.dismiss()
        self.create_trip(None)

    def on_join_trip_option(self, instance):
        """Handle join trip from menu"""
        if hasattr(self, 'new_trip_dialog'):
            self.new_trip_dialog.dismiss()
        self.show_join_trip_dialog()

    def show_join_trip_dialog(self):
        """Show join trip dialog with options"""
        app = MDApp.get_running_app()

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(8), dp(20), dp(8)],
            size_hint_y=None,
            height=dp(200)
        )

        # Trip Key input
        self.trip_key_field = MDTextField(
            hint_text="Enter Trip Key",
            helper_text="Enter the trip key to join",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(60)
        )
        content.add_widget(self.trip_key_field)

        # Buttons
        buttons_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(48)
        )

        join_key_btn = MDRaisedButton(
            text="Join by Key",
            size_hint_x=0.5,
            on_release=self.join_trip_by_key
        )
        buttons_box.add_widget(join_key_btn)

        scan_qr_btn = MDRaisedButton(
            text="Scan QR",
            size_hint_x=0.5,
            on_release=self.scan_qr_code
        )
        buttons_box.add_widget(scan_qr_btn)

        content.add_widget(buttons_box)

        self.join_trip_dialog = MDDialog(
            title="Join Trip",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.join_trip_dialog.dismiss()
                )
            ]
        )
        self.join_trip_dialog.open()

    def join_trip_by_key(self, instance):
        """Join trip using entered key"""
        trip_key = self.trip_key_field.text.strip()
        if not trip_key:
            app = MDApp.get_running_app()
            app.show_error_snackbar("Please enter a trip key")
            return

        app = MDApp.get_running_app()
        app.show_success_snackbar("Joining trip...")
        
        def do_join(dt):
            trip_data, error = app.api_client.join_trip(trip_key)
            
            if trip_data:
                app.show_success_snackbar(f"Successfully joined trip: {trip_data.get('title', 'Unknown Trip')}")
                # Refresh trips in dashboard
                self.load_trips()
            else:
                app.show_error_snackbar(f"Failed to join trip: {error}")
            
            self.join_trip_dialog.dismiss()
        
        Clock.schedule_once(do_join, 0.5)

    def scan_qr_code(self, instance):
        """Scan QR code to join trip"""
        app = MDApp.get_running_app()
        # For now, show a dialog to enter trip ID manually
        # In a real implementation, you'd use a camera scanner
        app.show_success_snackbar("QR scanning will be available soon. Please use Trip ID for now.")
        self.join_trip_dialog.dismiss()

    def browse_destinations(self):
        """Browse popular destinations"""
        app = MDApp.get_running_app()
        app.show_success_snackbar("Browse destinations feature coming soon!")

    def show_profile_menu(self, instance):
        """Show profile dropdown menu"""
        app = MDApp.get_running_app()
        
        menu_items = [
            {
                "text": "Profile",
                "viewclass": "Button",
                "on_release": lambda: self.open_profile()
            },
            {
                "text": "Logout",
                "viewclass": "Button",
                "on_release": lambda: self.logout()
            }
        ]
        
        self.profile_menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        self.profile_menu.open()
    
    def open_profile(self):
        """Open profile screen"""
        app = MDApp.get_running_app()
        app.open_profile()
        if hasattr(self, 'profile_menu'):
            self.profile_menu.dismiss()

    def logout(self):
        """Logout user"""
        app = MDApp.get_running_app()
        app.logout_user()
        if hasattr(self, 'profile_menu'):
            self.profile_menu.dismiss()

    def show_saved_places(self):
        """Show saved places placeholder dialog"""
        app = MDApp.get_running_app()
        from kivymd.uix.dialog import MDDialog
        content = MDLabel(
            text="Saved Places feature coming soon!",
            size_hint_y=None,
            valign="top"
        )
        content.bind(texture_size=content.setter('size'))
        self.saved_places_dialog = MDDialog(
            title="Saved Places",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.saved_places_dialog.dismiss()
                )
            ]
        )
        self.saved_places_dialog.open()

    def show_travel_tips(self):
        """Show travel tips placeholder dialog"""
        app = MDApp.get_running_app()
        from kivymd.uix.dialog import MDDialog
        content = MDLabel(
            text="Travel Tips feature coming soon!",
            size_hint_y=None,
            valign="top"
        )
        content.bind(texture_size=content.setter('size'))
        self.travel_tips_dialog = MDDialog(
            title="Travel Tips",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.travel_tips_dialog.dismiss()
                )
            ]
        )
        self.travel_tips_dialog.open()

    def show_menu(self, instance):
        """Show hamburger menu"""
        menu_items = [
            {
                "text": "My Trips",
                "icon": "briefcase-outline",
                "viewclass": "Button",
                "on_release": lambda: self.load_trips()
            },
            {
                "text": "New Trip",
                "icon": "plus",
                "viewclass": "Button",
                "on_release": lambda: self.create_trip(None)
            },
            {
                "text": "Saved Places",
                "icon": "heart-outline",
                "viewclass": "Button",
                "on_release": lambda: self.show_saved_places()
            },
            {
                "text": "Travel Tips",
                "icon": "earth",
                "viewclass": "Button",
                "on_release": lambda: self.show_travel_tips()
            },
            {
                "text": "Settings",
                "icon": "cog-outline",
                "viewclass": "Button",
                "on_release": lambda: self.show_settings()
            },
            {
                "text": "Help & Feedback",
                "icon": "help-circle-outline",
                "viewclass": "Button",
                "on_release": lambda: self.show_help()
            },
            {
                "text": "Profile / Sign Out",
                "icon": "account-outline",
                "viewclass": "Button",
                "on_release": lambda: self.show_profile()
            }
        ]

        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            elevation=4,
            border_margin=dp(10)
        )
        self.menu.open()
        