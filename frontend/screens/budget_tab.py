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
from datetime import datetime

class ExpenseCard(MDCard):
    def __init__(self, expense, on_edit_callback=None, on_delete_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.expense = expense
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
        
        # Expense info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=5
        )
        
        # Title and amount
        title_amount = f"{self.expense['title']} - ${self.expense['amount']:.2f}"
        title = MDLabel(
            text=title_amount,
            theme_text_color="Primary",
            size_hint_y=None,
            height=25,
            font_style="H6"
        )
        info_layout.add_widget(title)
        
        # Category and date
        expense_date = datetime.fromisoformat(self.expense['date'].replace('Z', '+00:00'))
        category_date = f"🏷️ {self.expense['category'].title()} | 📅 {expense_date.strftime('%b %d, %Y')}"
        
        category_date_label = MDLabel(
            text=category_date,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=20,
            font_style="Body2"
        )
        info_layout.add_widget(category_date_label)
        
        # Notes
        if self.expense.get('notes'):
            notes_label = MDLabel(
                text=f"📝 {self.expense['notes']}",
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
                on_release=lambda x: self.on_edit_callback(self.expense)
            )
            actions_layout.add_widget(edit_btn)
        
        if self.on_delete_callback:
            delete_btn = MDRaisedButton(
                text="Delete",
                size_hint_y=None,
                height=30,
                on_release=lambda x: self.on_delete_callback(self.expense)
            )
            actions_layout.add_widget(delete_btn)
        
        layout.add_widget(actions_layout)
        
        self.add_widget(layout)

class BudgetTab(MDBoxLayout):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            kwargs.pop('name')
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [20, 20, 20, 20]
        self.trip = None
        self.expenses = []
        self.budget_summary = {}
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
        
        # Budget summary card
        self.budget_summary_card = MDCard(
            size_hint=(0.9, None),
            height=200,
            elevation=2,
            pos_hint={'center_x': 0.5}
        )
        self.content_container.add_widget(self.budget_summary_card)
        
        # Expenses list
        self.expenses_label = MDLabel(
            text="Recent Expenses",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40,
            font_style="H5"
        )
        self.content_container.add_widget(self.expenses_label)
        
        self.scroll_view.add_widget(self.content_container)
        self.add_widget(self.scroll_view)
        
        # Floating action button
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={'right': 0.95, 'bottom': 0.05},
            on_release=self.add_expense
        )
        self.add_widget(self.fab)
    
    def load_trip(self, trip):
        """Load trip data"""
        self.trip = trip
        self.expenses = trip.get('expenses', [])
        self.load_budget_summary()
        self.update_expenses_display()
    
    def load_budget_summary(self):
        """Load budget summary from API"""
        app = MDApp.get_running_app()

        def do_load(dt):
            trip_id = getattr(self.trip, 'id', None)
            if trip_id is None:
                # Try to get from dict key '_id' or 'id'
                trip_id = self.trip.get('_id') if isinstance(self.trip, dict) else None
                if trip_id is None:
                    trip_id = self.trip.get('id') if isinstance(self.trip, dict) else None
            if trip_id is None:
                self.calculate_budget_summary()
                return

            summary, error = app.api_client.get_expense_summary(str(trip_id))
            if summary:
                self.budget_summary = summary
                self.update_budget_summary()
            else:
                # Fallback to local calculation
                self.calculate_budget_summary()

        Clock.schedule_once(do_load, 0.1)
    
    def calculate_budget_summary(self):
        """Calculate budget summary locally"""
        total_spent = sum(expense['amount'] for expense in self.expenses)
        budget = self.trip['budget']
        remaining = budget - total_spent
        
        # Category breakdown
        category_totals = {}
        for expense in self.expenses:
            category = expense['category']
            if category in category_totals:
                category_totals[category] += expense['amount']
            else:
                category_totals[category] = expense['amount']
        
        self.budget_summary = {
            'budget': budget,
            'total_spent': total_spent,
            'remaining': remaining,
            'category_breakdown': category_totals
        }
        self.update_budget_summary()
    
    def update_budget_summary(self):
        """Update budget summary display"""
        self.budget_summary_card.clear_widgets()
        
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[15, 15, 15, 15],
            spacing=10
        )
        
        # Title
        title = MDLabel(
            text="💰 Budget Summary",
            theme_text_color="Primary",
            size_hint_y=None,
            height=30,
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Budget info
        budget_info = f"Budget: ${self.budget_summary['budget']:,.2f}"
        budget_label = MDLabel(
            text=budget_info,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=25,
            font_style="Body1"
        )
        layout.add_widget(budget_label)
        
        # Spent info
        spent_info = f"Spent: ${self.budget_summary['total_spent']:,.2f}"
        spent_label = MDLabel(
            text=spent_info,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=25,
            font_style="Body1"
        )
        layout.add_widget(spent_label)
        
        # Remaining info
        remaining = self.budget_summary['remaining']
        remaining_color = "Primary" if remaining >= 0 else "Error"
        remaining_info = f"Remaining: ${remaining:,.2f}"
        remaining_label = MDLabel(
            text=remaining_info,
            theme_text_color=remaining_color,
            size_hint_y=None,
            height=25,
            font_style="Body1"
        )
        layout.add_widget(remaining_label)
        
        # Category breakdown
        if self.budget_summary.get('category_breakdown'):
            category_text = "Category Breakdown:\n"
            for category, amount in self.budget_summary['category_breakdown'].items():
                category_text += f"• {category.title()}: ${amount:.2f}\n"
            
            category_label = MDLabel(
                text=category_text.strip(),
                theme_text_color="Secondary",
                size_hint_y=None,
                height=60,
                font_style="Body2"
            )
            layout.add_widget(category_label)
        
        self.budget_summary_card.add_widget(layout)
    
    def update_expenses_display(self):
        """Update the expenses display"""
        # Remove old expenses label
        if hasattr(self, 'expenses_label'):
            self.content_container.remove_widget(self.expenses_label)
        
        # Add new expenses label
        self.expenses_label = MDLabel(
            text=f"Recent Expenses ({len(self.expenses)})",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40,
            font_style="H5"
        )
        self.content_container.add_widget(self.expenses_label)
        
        if not self.expenses:
            # Show empty state
            empty_label = MDLabel(
                text="No expenses recorded yet!\nTap the + button to add your first expense.",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=100
            )
            self.content_container.add_widget(empty_label)
        else:
            # Show recent expenses (last 10)
            recent_expenses = sorted(self.expenses, key=lambda x: x['date'], reverse=True)[:10]
            for expense in recent_expenses:
                card = ExpenseCard(
                    expense=expense,
                    on_edit_callback=self.edit_expense,
                    on_delete_callback=self.delete_expense,
                    size_hint_y=None
                )
                self.content_container.add_widget(card)
    
    def add_expense(self, instance):
        """Show add expense dialog"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=300
        )
        
        self.expense_title_field = MDTextField(
            hint_text="Expense Title",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.expense_title_field)
        
        self.expense_amount_field = MDTextField(
            hint_text="Amount ($)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.expense_amount_field)
        
        self.expense_category_field = MDTextField(
            hint_text="Category (accommodation, food, transport, entertainment)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.expense_category_field)
        
        self.expense_notes_field = MDTextField(
            hint_text="Notes (optional)",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.expense_notes_field)
        
        self.add_expense_dialog = MDDialog(
            title="Add Expense",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.add_expense_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Add",
                    on_release=self.create_expense
                )
            ]
        )
        self.add_expense_dialog.open()
    
    def create_expense(self, instance):
        """Create new expense"""
        # Get form data
        title = self.expense_title_field.text.strip()
        amount_str = self.expense_amount_field.text.strip()
        category = self.expense_category_field.text.strip()
        notes = self.expense_notes_field.text.strip()
        
        # Validate inputs
        if not all([title, amount_str, category]):
            self.show_error("Please fill in all required fields")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.show_error("Amount must be greater than 0")
                return
        except ValueError:
            self.show_error("Invalid amount value")
            return
        
        # Prepare expense data
        expense_data = {
            "title": title,
            "amount": amount,
            "category": category,
            "notes": notes,
            "date": datetime.utcnow().isoformat() + "Z"
        }
        
        # Get app instance
        app = MDApp.get_running_app()

        # Show loading
        self.show_loading("Adding expense...")
        
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

            result, error = app.api_client.create_expense(str(trip_id), expense_data)
            if result:
                self.hide_loading()
                self.add_expense_dialog.dismiss()
                self.expenses.append(result)
                self.load_budget_summary()
                self.update_expenses_display()
                app.show_success_dialog("Success", "Expense added successfully!")
            else:
                self.hide_loading()
                self.show_error(f"Failed to add expense: {error}")

        Clock.schedule_once(do_create, 0.1)
    
    def edit_expense(self, expense):
        """Edit expense (placeholder)"""
        dialog = MDDialog(
            title="Edit Expense",
            text="Edit functionality coming soon!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def delete_expense(self, expense):
        """Delete expense"""
        dialog = MDDialog(
            title="Delete Expense",
            text=f"Are you sure you want to delete '{expense['title']}'?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete_expense(expense, dialog)
                )
            ]
        )
        dialog.open()
    
    def confirm_delete_expense(self, expense, dialog):
        """Confirm expense deletion"""
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

            result, error = app.api_client.delete_expense(str(trip_id), expense['id'])
            if result:
                self.expenses = [e for e in self.expenses if e['id'] != expense['id']]
                self.load_budget_summary()
                self.update_expenses_display()
                app.show_success_dialog("Success", "Expense deleted successfully!")
            else:
                app.show_error_dialog("Error", f"Failed to delete expense: {error}")

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
