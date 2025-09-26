import requests
import json
from kivy.storage.jsonstore import JsonStore

class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8001"  # Change this to your backend URL
        self.store = JsonStore('user_data.json')
    
    def get_headers(self):
        """Get headers with authorization token"""
        headers = {"Content-Type": "application/json"}
        if self.store.exists('access_token'):
            token = self.store.get('access_token')['token']
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def register(self, email, username, password):
        """Register a new user"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "email": email,
                    "username": username,
                    "password": password
                }
            )
            if 200 <= response.status_code < 300:
                return response.json(), None
            else:
                try:
                    return None, response.json().get("detail", f"HTTP {response.status_code}")
                except Exception:
                    return None, response.text or f"HTTP {response.status_code}"
        except Exception as e:
            return None, str(e)
    
    def login(self, email, password):
        """Login user"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )
            if 200 <= response.status_code < 300:
                return response.json(), None
            else:
                try:
                    return None, response.json().get("detail", f"HTTP {response.status_code}")
                except Exception:
                    return None, response.text or f"HTTP {response.status_code}"
        except Exception as e:
            return None, str(e)
    
    def get_current_user(self):
        """Get current user info"""
        try:
            response = requests.get(
                f"{self.base_url}/auth/me",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get user info")
        except Exception as e:
            return None, str(e)
    
    def update_user_profile(self, user_data):
        """Update user profile"""
        try:
            response = requests.put(
                f"{self.base_url}/auth/profile",
                json=user_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to update profile")
        except Exception as e:
            return None, str(e)
    
    def change_password(self, password_data):
        """Change user password"""
        try:
            response = requests.put(
                f"{self.base_url}/auth/change-password",
                json=password_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return True, None
            else:
                return None, response.json().get("detail", "Failed to change password")
        except Exception as e:
            return None, str(e)
    
    def get_trips(self):
        """Get user trips"""
        try:
            headers = self.get_headers()
            
            response = requests.get(
                f"{self.base_url}/trips/",
                headers=headers
            )
            
            if response.status_code == 200:
                trips = response.json()
                return trips, None
            elif response.status_code == 401:
                return None, "Authentication failed. Please login again."
            else:
                try:
                    error_detail = response.json().get("detail", f"HTTP {response.status_code}")
                except:
                    error_detail = f"HTTP {response.status_code}"
                return None, error_detail
        except Exception as e:
            return None, str(e)
    
    def create_trip(self, trip_data):
        """Create a new trip"""
        try:
            response = requests.post(
                f"{self.base_url}/trips/",
                json=trip_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to create trip")
        except Exception as e:
            return None, str(e)
    
    def get_trip(self, trip_id):
        """Get trip details"""
        try:
            response = requests.get(
                f"{self.base_url}/trips/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get trip")
        except Exception as e:
            return None, str(e)
    
    def update_trip(self, trip_id, trip_data):
        """Update trip"""
        try:
            response = requests.put(
                f"{self.base_url}/trips/{trip_id}",
                json=trip_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to update trip")
        except Exception as e:
            return None, str(e)
    
    def delete_trip(self, trip_id):
        """Delete trip"""
        try:
            response = requests.delete(
                f"{self.base_url}/trips/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return True, None
            else:
                return None, response.json().get("detail", "Failed to delete trip")
        except Exception as e:
            return None, str(e)
    
    def join_trip(self, trip_id):
        """Join a trip using trip ID"""
        try:
            response = requests.post(
                f"{self.base_url}/trips/join/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to join trip")
        except Exception as e:
            return None, str(e)
    
    def get_activities(self, trip_id):
        """Get trip activities"""
        try:
            response = requests.get(
                f"{self.base_url}/activities/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get activities")
        except Exception as e:
            return None, str(e)
    
    def create_activity(self, trip_id, activity_data):
        """Create activity"""
        try:
            response = requests.post(
                f"{self.base_url}/activities/{trip_id}",
                json=activity_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to create activity")
        except Exception as e:
            return None, str(e)
    
    def update_activity(self, trip_id, activity_id, activity_data):
        """Update activity"""
        try:
            response = requests.put(
                f"{self.base_url}/activities/{trip_id}/{activity_id}",
                json=activity_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to update activity")
        except Exception as e:
            return None, str(e)
    
    def delete_activity(self, trip_id, activity_id):
        """Delete activity"""
        try:
            response = requests.delete(
                f"{self.base_url}/activities/{trip_id}/{activity_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return True, None
            else:
                return None, response.json().get("detail", "Failed to delete activity")
        except Exception as e:
            return None, str(e)
    
    def get_expenses(self, trip_id):
        """Get trip expenses"""
        try:
            response = requests.get(
                f"{self.base_url}/expenses/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get expenses")
        except Exception as e:
            return None, str(e)
    
    def create_expense(self, trip_id, expense_data):
        """Create expense"""
        try:
            response = requests.post(
                f"{self.base_url}/expenses/{trip_id}",
                json=expense_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to create expense")
        except Exception as e:
            return None, str(e)
    
    def get_expense_summary(self, trip_id):
        """Get expense summary"""
        try:
            response = requests.get(
                f"{self.base_url}/expenses/{trip_id}/summary",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get expense summary")
        except Exception as e:
            return None, str(e)
    
    def get_packing_items(self, trip_id):
        """Get packing items"""
        try:
            response = requests.get(
                f"{self.base_url}/packing/{trip_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get packing items")
        except Exception as e:
            return None, str(e)
    
    def create_packing_item(self, trip_id, item_data):
        """Create packing item"""
        try:
            response = requests.post(
                f"{self.base_url}/packing/{trip_id}",
                json=item_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to create packing item")
        except Exception as e:
            return None, str(e)
    
    def toggle_packing_item(self, trip_id, item_id):
        """Toggle packing item"""
        try:
            response = requests.put(
                f"{self.base_url}/packing/{trip_id}/{item_id}/toggle",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to toggle packing item")
        except Exception as e:
            return None, str(e)
    
    def update_packing_item(self, trip_id, item_id, item_data):
        """Update packing item"""
        try:
            response = requests.put(
                f"{self.base_url}/packing/{trip_id}/{item_id}",
                json=item_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to update packing item")
        except Exception as e:
            return None, str(e)
    
    def delete_packing_item(self, trip_id, item_id):
        """Delete packing item"""
        try:
            response = requests.delete(
                f"{self.base_url}/packing/{trip_id}/{item_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return True, None
            else:
                return None, response.json().get("detail", "Failed to delete packing item")
        except Exception as e:
            return None, str(e)
    
    def update_expense(self, trip_id, expense_id, expense_data):
        """Update expense"""
        try:
            response = requests.put(
                f"{self.base_url}/expenses/{trip_id}/{expense_id}",
                json=expense_data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to update expense")
        except Exception as e:
            return None, str(e)
    
    def delete_expense(self, trip_id, expense_id):
        """Delete expense"""
        try:
            response = requests.delete(
                f"{self.base_url}/expenses/{trip_id}/{expense_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return True, None
            else:
                return None, response.json().get("detail", "Failed to delete expense")
        except Exception as e:
            return None, str(e)
    
    def get_weather_forecast(self, city, start_date, end_date):
        """Get weather forecast"""
        try:
            response = requests.get(
                f"{self.base_url}/weather/{city}",
                params={
                    "start_date": start_date,
                    "end_date": end_date
                },
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Failed to get weather forecast")
        except Exception as e:
            return None, str(e)

    def get_destination_image(self, destination):
        """Get destination image URL from Unsplash"""
        try:
            # Check if Unsplash API key is configured (not the placeholder)
            unsplash_key = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with actual key or environment variable
            if unsplash_key == "YOUR_UNSPLASH_ACCESS_KEY" or not unsplash_key:
                # Skip Unsplash API call and use local data URL placeholder
                # Create a simple colored rectangle as data URL
                import base64
                from PIL import Image, ImageDraw, ImageFont
                import io

                # Create a 300x150 image with a gradient background
                img = Image.new('RGB', (300, 150), color='#4A90E2')
                draw = ImageDraw.Draw(img)

                # Add some text
                try:
                    # Try to use a default font
                    font = ImageFont.load_default()
                except:
                    font = None

                # Add destination text
                text = destination[:20]  # Limit text length
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (300 - text_width) // 2
                y = (150 - text_height) // 2
                draw.text((x, y), text, fill='white', font=font)

                # Convert to base64 data URL
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                data_url = f"data:image/png;base64,{img_base64}"
                return data_url, None

            # Use Unsplash API (public access, limited)
            query = destination.replace(' ', '+')
            response = requests.get(
                f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={unsplash_key}"
            )
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['urls']['small'], None
            # Fallback to data URL placeholder
            import base64
            from PIL import Image, ImageDraw
            import io

            img = Image.new('RGB', (300, 150), color='#4A90E2')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.load_default()
            except:
                font = None
            text = destination[:20]
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (300 - text_width) // 2
            y = (150 - text_height) // 2
            draw.text((x, y), text, fill='white', font=font)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            data_url = f"data:image/png;base64,{img_base64}"
            return data_url, None
        except Exception as e:
            # Ultimate fallback - simple data URL
            import base64
            from PIL import Image
            import io

            try:
                img = Image.new('RGB', (300, 150), color='#CCCCCC')
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                data_url = f"data:image/png;base64,{img_base64}"
                return data_url, str(e)
            except:
                # If PIL fails, return a minimal data URL
                return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", str(e)
