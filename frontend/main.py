from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.list import MDList
from kivy.uix.button import Button
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button as MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import requests
import json
import websocket as websocket
import threading
from datetime import datetime, timedelta
import os

from screens.splash_screen import SplashScreen
from screens.auth_screen import AuthScreen
from screens.dashboard_screen import DashboardScreen
from screens.trip_detail_screen import TripDetailScreen
from screens.create_trip_screen import CreateTripScreen
from screens.join_trip_screen import JoinTripScreen
from screens.trip_sharing_screen import TripSharingScreen
from screens.calendar_screen import CalendarScreen
from screens.profile_screen import ProfileScreen
from utils.api_client import APIClient
from utils.websocket_client import WebSocketClient

class TravelMateApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "TravelMate"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        
        # Set app icon
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "Logo for Travel Mate App - Iconographic Style.png")
        logo_path = os.path.abspath(logo_path)
        if os.path.exists(logo_path):
            self.icon = logo_path
        
        # Initialize storage
        self.store = JsonStore('user_data.json')
        
        # Initialize API client
        self.api_client = APIClient()
        
        # Initialize WebSocket client
        self.ws_client = WebSocketClient()
        
        # Current user data
        self.current_user = None
        self.current_trip = None
        
        # Screen manager with smooth transitions
        self.screen_manager = MDScreenManager()
        self.screen_manager.transition = SlideTransition(duration=0.3)
        
    def build(self):
        # Create navigation layout
        self.nav_layout = MDNavigationLayout()

        # Add screen manager to nav layout
        self.nav_layout.add_widget(self.screen_manager)

        # Create navigation drawer
        self.nav_drawer = MDNavigationDrawer()

        # Create drawer content
        drawer_scroll = MDScrollView()
        drawer_list = MDList()

        # Add menu items to drawer
        menu_items = [
            ("My Trips", "briefcase", self.load_trips),
            ("New Trip", "plus", self.show_new_trip_menu),
            ("Saved Places", "heart", self.show_saved_places),
            ("Travel Tips", "earth", self.show_travel_tips),
            ("Settings", "cog", self.show_settings),
            ("Help & Feedback", "help-circle", self.show_help),
            ("Profile / Sign Out", "account", self.show_profile)
        ]

        for text, icon, callback in menu_items:
            item = Button(text=text, on_release=lambda cb=callback: self.call_menu_callback(cb))
            # Note: Icon functionality will need to be implemented differently in KivyMD 2.0
            drawer_list.add_widget(item)

        drawer_scroll.add_widget(drawer_list)
        self.nav_drawer.add_widget(drawer_scroll)

        # Add drawer to nav layout
        self.nav_layout.add_widget(self.nav_drawer)

        # Add screens
        self.splash_screen = SplashScreen(name='splash')
        self.auth_screen = AuthScreen(name='auth')
        self.dashboard_screen = DashboardScreen(name='dashboard')
        self.trip_detail_screen = TripDetailScreen(name='trip_detail')
        self.create_trip_screen = CreateTripScreen(name='create_trip')
        self.join_trip_screen = JoinTripScreen(name='join_trip')
        self.trip_sharing_screen = TripSharingScreen(name='trip_sharing')
        self.calendar_screen = CalendarScreen(name='calendar')
        self.profile_screen = ProfileScreen(name='profile')

        self.screen_manager.add_widget(self.splash_screen)
        self.screen_manager.add_widget(self.auth_screen)
        self.screen_manager.add_widget(self.dashboard_screen)
        self.screen_manager.add_widget(self.trip_detail_screen)
        self.screen_manager.add_widget(self.create_trip_screen)
        self.screen_manager.add_widget(self.join_trip_screen)
        self.screen_manager.add_widget(self.trip_sharing_screen)
        self.screen_manager.add_widget(self.calendar_screen)
        self.screen_manager.add_widget(self.profile_screen)

        # Start with splash screen - authentication will be handled there
        self.screen_manager.current = 'splash'

        # Close drawer on screen change
        self.screen_manager.bind(current=self.close_nav_drawer)

        return self.nav_layout

    def call_menu_callback(self, callback):
        """Call the menu callback and close the drawer"""
        callback()
        self.nav_drawer.set_state("close")

    def close_nav_drawer(self, instance, value):
        """Close the navigation drawer"""
        if self.nav_drawer.state == "open":
            self.nav_drawer.set_state("close")

    def load_trips(self):
        """Load trips in dashboard"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.load_trips()

    def show_new_trip_menu(self):
        """Show new trip menu"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_new_trip_menu(None)

    def show_saved_places(self):
        """Show saved places"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_saved_places()

    def show_travel_tips(self):
        """Show travel tips"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_travel_tips()

    def show_settings(self):
        """Show settings"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_settings()

    def show_help(self):
        """Show help"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_help()

    def show_profile(self):
        """Show profile"""
        if hasattr(self, 'dashboard_screen'):
            self.dashboard_screen.show_profile()
    
    
    def login_user(self, user_data, access_token):
        """Handle successful login"""
        self.current_user = user_data
        self.store.put('access_token', token=access_token)
        self.store.put('user', **user_data)
        self.screen_manager.current = 'dashboard'
        self.dashboard_screen.load_trips()
    
    def logout_user(self):
        """Handle logout"""
        self.current_user = None
        self.store.delete('access_token')
        self.store.delete('user')
        self.screen_manager.current = 'auth'
        self.ws_client.disconnect()
    
    def open_trip_detail(self, trip):
        """Open trip detail screen"""
        self.current_trip = trip
        self.trip_detail_screen.load_trip(trip)
        self.screen_manager.current = 'trip_detail'
    
    def open_create_trip(self):
        """Open create trip screen"""
        self.screen_manager.current = 'create_trip'
    
    def open_join_trip(self):
        """Open join trip screen"""
        self.screen_manager.current = 'join_trip'
    
    def open_trip_sharing(self, trip):
        """Open trip sharing screen"""
        self.trip_sharing_screen.trip = trip
        self.screen_manager.current = 'trip_sharing'
    
    def open_profile(self):
        """Open profile screen"""
        self.screen_manager.current = 'profile'
    
    def go_back_to_dashboard(self):
        """Go back to dashboard"""
        self.screen_manager.current = 'dashboard'
        self.dashboard_screen.load_trips()
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_success_dialog(self, title, message):
        """Show success dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    # Non-blocking feedback via snackbars
    def show_success_snackbar(self, message):
        from kivymd.uix.snackbar import Snackbar
        try:
            Snackbar(text=message, duration=2).open()
        except Exception:
            self.show_success_dialog("Success", message)

    def show_error_snackbar(self, message):
        from kivymd.uix.snackbar import Snackbar
        try:
            Snackbar(text=message, duration=2).open()
        except Exception:
            self.show_error_dialog("Error", message)

if __name__ == '__main__':
    TravelMateApp().run()
