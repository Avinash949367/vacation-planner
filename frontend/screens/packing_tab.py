from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.button import Button as MDRaisedButton
from kivymd.app import MDApp
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.clock import Clock
from datetime import datetime

class PackingItemCard(MDCard):
    def __init__(self, item, on_toggle_callback=None, on_edit_callback=None, on_delete_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.on_toggle_callback = on_toggle_callback
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback
        self.size_hint = (0.9, None)
        self.height = 80
        self.elevation = 2
        self.pos_hint = {'center_x': 0.5}
        self.build_card()
    
    def build_card(self):
        layout = MDBoxLayout(
            orientation='horizontal',
            padding=[10, 10, 10, 10],
            spacing=10
        )
        
        # Checkbox
        self.checkbox = MDCheckbox(
            active=self.item['packed'],
            on_release=lambda x: self.toggle_item()
        )
        layout.add_widget(self.checkbox)
        
        # Item info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=5
        )
        
        # Name
        name = MDLabel(
            text=self.item['name'],
            theme_text_color="Primary" if not self.item['packed'] else "Secondary",
            size_hint_y=None,
            height=25,
            font_style="H6"
        )
        info_layout.add_widget(name)
        
        # Category
        category = f"🏷️ {self.item['category'].title()}"
        category_label = MDLabel(
            text=category,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=20,
            font_style="Body2"
        )
        info_layout.add_widget(category_label)
        
        # Notes
        if self.item.get('notes'):
            notes_label = MDLabel(
                text=f"📝 {self.item['notes']}",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=20,
                font_style="Caption"
            )
            info_layout.add_widget(notes_label)
        
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
                on_release=lambda x: self.on_edit_callback(self.item)
            )
            actions_layout.add_widget(edit_btn)
        
        if self.on_delete_callback:
            delete_btn = MDRaisedButton(
                text="Delete",
                size_hint_y=None,
                height=30,
                on_release=lambda x: self.on_delete_callback(self.item)
            )
            actions_layout.add_widget(delete_btn)
        
        layout.add_widget(actions_layout)
        
        self.add_widget(layout)
    
    def toggle_item(self):
        """Toggle item packed status"""
        if self.on_toggle_callback:
            self.on_toggle_callback(self.item)

class PackingTab(MDBoxLayout):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            kwargs.pop('name')
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [20, 20, 20, 20]
        self.trip = None
        self.packing_items = []
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
        
        # Packing summary card
        self.packing_summary_card = MDCard(
            size_hint=(0.9, None),
            height=150,
            elevation=2,
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.packing_summary_card)
        
        # Packing items list
        self.items_label = MDLabel(
            text="Packing Items",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40,
            font_style="H5"
        )
        self.content_container.add_widget(self.items_label)
        
        self.scroll_view.add_widget(self.content_container)
        self.add_widget(self.scroll_view)
        
        # Floating action button
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={'right': 0.95, 'bottom': 0.05},
            on_release=self.add_item
        )
        self.add_widget(self.fab)
    
    def load_trip(self, trip):
        """Load trip data"""
        self.trip = trip
        self.packing_items = trip.get('packing_items', [])
        self.update_packing_summary()
        self.update_items_display()
    
    def update_packing_summary(self):
        """Update packing summary display"""
        self.packing_summary_card.clear_widgets()
        
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[15, 15, 15, 15],
            spacing=10
        )
        
        # Title
        title = MDLabel(
            text="🎒 Packing Progress",
            theme_text_color="Primary",
            size_hint_y=None,
            height=30,
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Progress info
        total_items = len(self.packing_items)
        packed_items = sum(1 for item in self.packing_items if item['packed'])
        
        if total_items > 0:
            progress_percent = (packed_items / total_items) * 100
            progress_text = f"{packed_items}/{total_items} items packed ({progress_percent:.0f}%)"
        else:
            progress_text = "No items added yet"
        
        progress_label = MDLabel(
            text=progress_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=25,
            font_style="Body1"
        )
        layout.add_widget(progress_label)
        
        # Category breakdown
        if self.packing_items:
            categories = {}
            for item in self.packing_items:
                category = item['category']
                if category not in categories:
                    categories[category] = {'total': 0, 'packed': 0}
                categories[category]['total'] += 1
                if item['packed']:
                    categories[category]['packed'] += 1
            
            category_text = "Categories:\n"
            for category, counts in categories.items():
                category_text += f"• {category.title()}: {counts['packed']}/{counts['total']}\n"
            
            category_label = MDLabel(
                text=category_text.strip(),
                theme_text_color="Secondary",
                size_hint_y=None,
                height=60,
                font_style="Body2"
            )
            layout.add_widget(category_label)
        
        self.packing_summary_card.add_widget(layout)
    
    def update_items_display(self):
        """Update the items display"""
        # Remove old items label
        if hasattr(self, 'items_label'):
            self.content_container.remove_widget(self.items_label)
        
        # Add new items label
        self.items_label = MDLabel(
            text=f"Packing Items ({len(self.packing_items)})",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40,
            font_style="H5"
        )
        self.content_container.add_widget(self.items_label)
        
        if not self.packing_items:
            # Show empty state
            empty_label = MDLabel(
                text="No packing items yet!\nTap the + button to add your first item.",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=100
            )
            self.content_container.add_widget(empty_label)
        else:
            # Group items by category
            items_by_category = {}
            for item in self.packing_items:
                category = item['category']
                if category not in items_by_category:
                    items_by_category[category] = []
                items_by_category[category].append(item)
            
            # Display items by category
            for category in sorted(items_by_category.keys()):
                # Category header
                category_label = MDLabel(
                    text=f"{category.title()} ({len(items_by_category[category])} items)",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=40,
                    font_style="H6"
                )
                self.content_container.add_widget(category_label)
                
                # Items for this category
                for item in items_by_category[category]:
                    card = PackingItemCard(
                        item=item,
                        on_toggle_callback=self.toggle_item,
                        on_edit_callback=self.edit_item,
                        on_delete_callback=self.delete_item,
                        size_hint_y=None
                    )
                    self.content_container.add_widget(card)
    
    def add_item(self, instance):
        """Show add item dialog"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=250
        )
        
        self.item_name_field = MDTextField(
            hint_text="Item Name",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.item_name_field)
        
        self.item_category_field = MDTextField(
            hint_text="Category (clothes, toiletries, electronics, documents)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.item_category_field)
        
        self.item_notes_field = MDTextField(
            hint_text="Notes (optional)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.item_notes_field)
        
        self.add_item_dialog = MDDialog(
            title="Add Packing Item",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.add_item_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Add",
                    on_release=self.create_item
                )
            ]
        )
        self.add_item_dialog.open()
    
    def create_item(self, instance):
        """Create new packing item"""
        # Get form data
        name = self.item_name_field.text.strip()
        category = self.item_category_field.text.strip()
        notes = self.item_notes_field.text.strip()
        
        # Validate inputs
        if not all([name, category]):
            self.show_error("Please fill in all required fields")
            return
        
        # Prepare item data
        item_data = {
            "name": name,
            "category": category,
            "notes": notes,
            "packed": False
        }
        
        # Get app instance
        app = MDApp.get_running_app()

        # Show loading
        self.show_loading("Adding item...")

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

            result, error = app.api_client.create_packing_item(str(trip_id), item_data)
            if result:
                self.hide_loading()
                self.add_item_dialog.dismiss()
                self.packing_items.append(result)
                self.update_packing_summary()
                self.update_items_display()
                app.show_success_dialog("Success", "Packing item added successfully!")
            else:
                self.hide_loading()
                self.show_error(f"Failed to add item: {error}")

        Clock.schedule_once(do_create, 0.1)
    
    def toggle_item(self, item):
        """Toggle item packed status"""
        app = MDApp.get_running_app()

        def do_toggle(dt):
            trip_id = getattr(self.trip, 'id', None)
            if trip_id is None:
                trip_id = self.trip.get('_id') if isinstance(self.trip, dict) else None
                if trip_id is None:
                    trip_id = self.trip.get('id') if isinstance(self.trip, dict) else None
            if trip_id is None:
                app.show_error_dialog("Error", "Trip ID not found")
                return

            # Get item ID from various possible fields
            item_id = item.get('id') or item.get('_id') or item.get('item_id')
            if not item_id:
                app.show_error_dialog("Error", "Item ID not found")
                return

            result, error = app.api_client.toggle_packing_item(str(trip_id), str(item_id))
            if result:
                # Update local item
                for i, packing_item in enumerate(self.packing_items):
                    packing_item_id = packing_item.get('id') or packing_item.get('_id') or packing_item.get('item_id')
                    if packing_item_id == item_id:
                        self.packing_items[i]['packed'] = result['packed']
                        break
                self.update_packing_summary()
                self.update_items_display()
            else:
                app.show_error_dialog("Error", f"Failed to toggle item: {error}")

        Clock.schedule_once(do_toggle, 0.1)
    
    def edit_item(self, item):
        """Edit item (placeholder)"""
        dialog = MDDialog(
            title="Edit Item",
            text="Edit functionality coming soon!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def delete_item(self, item):
        """Delete item"""
        dialog = MDDialog(
            title="Delete Item",
            text=f"Are you sure you want to delete '{item['name']}'?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete_item(item, dialog)
                )
            ]
        )
        dialog.open()
    
    def confirm_delete_item(self, item, dialog):
        """Confirm item deletion"""
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

            result, error = app.api_client.delete_packing_item(str(trip_id), item['id'])
            if result:
                self.packing_items = [i for i in self.packing_items if i['id'] != item['id']]
                self.update_packing_summary()
                self.update_items_display()
                app.show_success_dialog("Success", "Item deleted successfully!")
            else:
                app.show_error_dialog("Error", f"Failed to delete item: {error}")

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
