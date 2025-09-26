import websocket as websocket
import json
import threading
from kivy.clock import Clock
from datetime import datetime

class WebSocketClient:
    def __init__(self):
        self.ws = None
        self.connected = False
        self.trip_id = None
        self.on_message_callback = None
    
    def connect(self, trip_id, on_message_callback=None):
        """Connect to WebSocket for a specific trip"""
        self.trip_id = trip_id
        self.on_message_callback = on_message_callback
        
        # WebSocket URL - change this to your backend URL
        ws_url = f"ws://localhost:8000/ws/{trip_id}"
        
        try:
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Start WebSocket in a separate thread
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
        except Exception as e:
            print(f"WebSocket connection error: {e}")
    
    def disconnect(self):
        """Disconnect from WebSocket"""
        if self.ws:
            self.ws.close()
            self.connected = False
    
    def on_open(self, ws):
        """Called when WebSocket connection is opened"""
        self.connected = True
        print(f"Connected to trip {self.trip_id}")
    
    def on_message(self, ws, message):
        """Called when a message is received"""
        try:
            data = json.loads(message)
            if self.on_message_callback:
                # Schedule callback on main thread
                Clock.schedule_once(lambda dt: self.on_message_callback(data))
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")
    
    def on_error(self, ws, error):
        """Called when WebSocket error occurs"""
        print(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Called when WebSocket connection is closed"""
        self.connected = False
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")
    
    def send_message(self, message):
        """Send a message through WebSocket"""
        if self.ws and self.connected:
            try:
                self.ws.send(json.dumps(message))
            except Exception as e:
                print(f"Error sending WebSocket message: {e}")
    
    def broadcast_update(self, update_type, data):
        """Broadcast an update to all connected clients"""
        message = {
            "type": update_type,
            "data": data,
            "timestamp": str(datetime.now())
        }
        self.send_message(message)
