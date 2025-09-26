from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.button import Button as MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.chip import MDChip
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime

class OverviewTab(MDBoxLayout):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            kwargs.pop('name')
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = [20, 20, 20, 20]
        self.md_bg_color = [0.98, 0.98, 0.98, 1]  # Light grey background
        self.build_ui()

    def get_responsive_sizes(self):
        """Get responsive sizes based on screen width"""
        screen_width = Window.size[0]
        screen_height = Window.size[1]

        if screen_width < 400:  # Small phones
            card_height_cover = 180
            card_height_info = 200
            card_height_weather = 160
            card_height_stats = 220
            padding = [15, 15, 15, 15]
            spacing = 10
            stat_card_size = (140, 65)
        elif screen_width < 600:  # Medium phones/tablets
            card_height_cover = 200
            card_height_info = 220
            card_height_weather = 180
            card_height_stats = 250
            padding = [20, 20, 20, 20]
            spacing = 15
            stat_card_size = (150, 70)
        else:  # Large tablets/desktops
            card_height_cover = 250
            card_height_info = 280
            card_height_weather = 200
            card_height_stats = 300
            padding = [25, 25, 25, 25]
            spacing = 20
            stat_card_size = (180, 80)

        return {
            'card_height_cover': card_height_cover,
            'card_height_info': card_height_info,
            'card_height_weather': card_height_weather,
            'card_height_stats': card_height_stats,
            'padding': padding,
            'spacing': spacing,
            'stat_card_size': stat_card_size
        }
    
    def build_ui(self):
        # Get responsive sizes
        sizes = self.get_responsive_sizes()

        # Scroll view
        self.scroll_view = MDScrollView()

        # Content container
        self.content_container = MDBoxLayout(
            orientation='vertical',
            spacing=sizes['spacing'],
            size_hint_y=None
        )
        self.content_container.bind(minimum_height=self.content_container.setter('height'))

        # Cover image card
        self.cover_card = MDCard(
            size_hint=(0.9, None),
            height=sizes['card_height_cover'],
            elevation=4,
            radius=[20, 20, 20, 20],
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.cover_card)

        # Trip info card
        self.trip_info_card = MDCard(
            size_hint=(0.9, None),
            height=sizes['card_height_info'],
            elevation=4,
            radius=[20, 20, 20, 20],
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.trip_info_card)

        # Weather card
        self.weather_card = MDCard(
            size_hint=(0.9, None),
            height=sizes['card_height_weather'],
            elevation=4,
            radius=[20, 20, 20, 20],
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.weather_card)

        # Quick stats card
        self.stats_card = MDCard(
            size_hint=(0.9, None),
            height=sizes['card_height_stats'],
            elevation=4,
            radius=[20, 20, 20, 20],
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.stats_card)

        self.scroll_view.add_widget(self.content_container)
        self.add_widget(self.scroll_view)
    
    def load_trip(self, trip):
        """Load trip data into overview"""
        self.trip = trip
        self.update_cover_image()
        self.update_trip_info()
        self.update_weather()
        self.update_stats()
    
    def update_trip_info(self):
        """Update trip information card"""
        self.trip_info_card.clear_widgets()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=[20, 20, 20, 20],
            spacing=15,
            md_bg_color=[1, 1, 1, 1],
            radius=[20, 20, 20, 20]
        )

        # Title with icon from dashboard
        title = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=50
        )
        icon = MDIconButton(
            icon="airplane-takeoff",
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(48, 48)
        )
        title_label = MDLabel(
            text=self.trip['title'],
            theme_text_color="Primary",
            font_style="H4",
            bold=True,
            valign="middle"
        )
        title.add_widget(icon)
        title.add_widget(title_label)
        layout.add_widget(title)

        # Destination with icon
        dest_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=40
        )
        dest_icon = MDIconButton(
            icon="map-marker-outline",
            theme_icon_color="Secondary",
            size_hint=(None, None),
            size=(36, 36)
        )
        dest_label = MDLabel(
            text=self.trip['destination'],
            theme_text_color="Secondary",
            font_style="H5",
            valign="middle"
        )
        dest_box.add_widget(dest_icon)
        dest_box.add_widget(dest_label)
        layout.add_widget(dest_box)

        # Dates with pill-shaped background
        start_date = datetime.fromisoformat(self.trip['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(self.trip['end_date'].replace('Z', '+00:00'))
        date_text = f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"

        date_chip = MDChip(
            text=date_text,
            size_hint=(None, None),
            height=36,
            padding=[15, 0, 15, 0],
            md_bg_color=[0.1, 0.5, 0.5, 0.3],  # Darker teal translucent background
            text_color=[0, 0, 0, 1],
            radius=[18, 18, 18, 18]
        )
        layout.add_widget(date_chip)

        # Duration with icon
        duration = (end_date - start_date).days + 1
        duration_text = f"{duration} day{'s' if duration != 1 else ''}"

        duration_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=35
        )
        duration_icon = MDIconButton(
            icon="timer-outline",
            theme_icon_color="Secondary",
            size_hint=(None, None),
            size=(32, 32)
        )
        duration_label = MDLabel(
            text=duration_text,
            theme_text_color="Secondary",
            font_style="Body1",
            valign="middle"
        )
        duration_box.add_widget(duration_icon)
        duration_box.add_widget(duration_label)
        layout.add_widget(duration_box)

        self.trip_info_card.add_widget(layout)

    def update_cover_image(self):
        """Update cover image card"""
        self.cover_card.clear_widgets()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=[0, 0, 0, 0],
            spacing=0
        )

        # Cover image
        cover_image = AsyncImage(
            source="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False
        )
        layout.add_widget(cover_image)

        self.cover_card.add_widget(layout)

    def update_weather(self):
        """Update weather information"""
        self.weather_card.clear_widgets()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=[20, 20, 20, 20],
            spacing=15,
            md_bg_color=[1, 1, 1, 1],
            radius=[20, 20, 20, 20]
        )

        # Weather title with icon
        title_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=40
        )
        weather_icon = MDIconButton(
            icon="weather-cloudy",
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(36, 36)
        )
        title = MDLabel(
            text="Weather Forecast",
            theme_text_color="Primary",
            font_style="H5",
            bold=True,
            valign="middle"
        )
        title_box.add_widget(weather_icon)
        title_box.add_widget(title)
        layout.add_widget(title_box)

        # Load weather data
        self.load_weather_data()

        # Weather info (placeholder)
        weather_info = MDLabel(
            text="Loading weather data...",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=70,
            font_style="Body1"
        )
        layout.add_widget(weather_info)

        self.weather_card.add_widget(layout)
    
    def load_weather_data(self):
        """Load weather data from API"""
        app = MDApp.get_running_app()
        
        def do_load(dt):
            forecast, error = app.api_client.get_weather_forecast(
                self.trip['destination'],
                self.trip['start_date'],
                self.trip['end_date']
            )
            if forecast:
                self.update_weather_display(forecast)
            else:
                self.update_weather_error(error)
        
        Clock.schedule_once(do_load, 0.1)
    
    def update_weather_display(self, forecast):
        """Update weather display with actual data"""
        self.weather_card.clear_widgets()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=[20, 20, 20, 20],
            spacing=15,
            md_bg_color=[1, 1, 1, 1],
            radius=[20, 20, 20, 20]
        )

        # Weather title with icon
        title_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint_y=None,
            height=40
        )
        weather_icon = MDIconButton(
            icon="weather-cloudy",
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(36, 36)
        )
        title = MDLabel(
            text="Weather Forecast",
            theme_text_color="Primary",
            font_style="H5",
            bold=True,
            valign="middle"
        )
        title_box.add_widget(weather_icon)
        title_box.add_widget(title)
        layout.add_widget(title_box)

        # Weather summary
        summary = forecast.get('summary', {})
        if summary:
            avg_temp = summary.get('average_temperature', 0)
            min_temp = summary.get('min_temperature', 0)
            max_temp = summary.get('max_temperature', 0)

            weather_text = f"Average: {avg_temp}°C\nRange: {min_temp}°C - {max_temp}°C"
        else:
            weather_text = "Weather data not available"

        weather_info = MDLabel(
            text=weather_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=70,
            font_style="Body1"
        )
        layout.add_widget(weather_info)

        self.weather_card.add_widget(layout)
    
    def update_weather_error(self, error):
        """Update weather display with error message"""
        self.weather_card.clear_widgets()
        
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[15, 15, 15, 15],
            spacing=10
        )
        
        # Weather title
        title = MDLabel(
            text="🌤️ Weather Forecast",
            theme_text_color="Primary",
            size_hint_y=None,
            height=30,
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Error message
        weather_info = MDLabel(
            text=f"Weather data unavailable\n{error or 'Please check your internet connection'}",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=60,
            font_style="Body2"
        )
        layout.add_widget(weather_info)
        
        self.weather_card.add_widget(layout)
    
    def update_stats(self):
        """Update quick statistics"""
        self.stats_card.clear_widgets()

        # Get responsive sizes
        sizes = self.get_responsive_sizes()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=sizes['padding'],
            spacing=10
        )

        # Stats title
        title = MDLabel(
            text="📊 Quick Stats",
            theme_text_color="Primary",
            size_hint_y=None,
            height=30,
            font_style="H6"
        )
        layout.add_widget(title)

        # Stats grid with mini cards
        stats_grid = MDGridLayout(
            cols=2,
            spacing=sizes['spacing'],
            size_hint_y=None,
            height=sizes['stat_card_size'][1] * 2 + sizes['spacing']  # 2 rows
        )

        def create_stat_card(icon, label, value):
            card = MDCard(
                size_hint=(None, None),
                size=sizes['stat_card_size'],
                elevation=4,
                radius=[15, 15, 15, 15],
                padding=[10, 10, 10, 10]
            )
            card_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=10
            )
            icon_button = MDIconButton(
                icon=icon,
                size_hint=(None, None),
                size=(40, 40),
                theme_icon_color="Primary"
            )
            card_layout.add_widget(icon_button)

            text_layout = MDBoxLayout(
                orientation='vertical',
                spacing=5
            )
            value_label = MDLabel(
                text=str(value),
                font_style="H6",
                bold=True,
                halign="left"
            )
            text_layout.add_widget(value_label)
            label_label = MDLabel(
                text=label,
                font_style="Body2",
                halign="left"
            )
            text_layout.add_widget(label_label)

            card_layout.add_widget(text_layout)
            card.add_widget(card_layout)
            return card

        budget_card = create_stat_card("cash", "Budget", f"${self.trip['budget']:,.2f}")
        activities_card = create_stat_card("party-popper", "Activities", len(self.trip.get('activities', [])))
        expenses_card = create_stat_card("chart-bar", "Expenses", len(self.trip.get('expenses', [])))
        packing_card = create_stat_card("bag-personal", "Packing", f"{len(self.trip.get('packing_items', []))} items")

        stats_grid.add_widget(budget_card)
        stats_grid.add_widget(activities_card)
        stats_grid.add_widget(expenses_card)
        stats_grid.add_widget(packing_card)

        layout.add_widget(stats_grid)
        self.stats_card.add_widget(layout)
