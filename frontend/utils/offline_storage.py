import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class OfflineStorage:
    def __init__(self, storage_file: str = "offline_data.json"):
        self.storage_file = storage_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from storage file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading offline data: {e}")
        return {
            "trips": [],
            "pending_actions": [],
            "last_sync": None
        }
    
    def _save_data(self):
        """Save data to storage file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving offline data: {e}")
    
    def cache_trips(self, trips: List[Dict[str, Any]]):
        """Cache trips data for offline access"""
        self.data["trips"] = trips
        self.data["last_sync"] = datetime.utcnow().isoformat()
        self._save_data()
    
    def get_cached_trips(self) -> List[Dict[str, Any]]:
        """Get cached trips data"""
        return self.data.get("trips", [])
    
    def cache_trip(self, trip: Dict[str, Any]):
        """Cache a single trip"""
        trips = self.get_cached_trips()
        # Update existing trip or add new one
        trip_updated = False
        for i, cached_trip in enumerate(trips):
            if cached_trip.get("id") == trip.get("id"):
                trips[i] = trip
                trip_updated = True
                break
        
        if not trip_updated:
            trips.append(trip)
        
        self.data["trips"] = trips
        self._save_data()
    
    def get_cached_trip(self, trip_id: str) -> Optional[Dict[str, Any]]:
        """Get a cached trip by ID"""
        trips = self.get_cached_trips()
        for trip in trips:
            if trip.get("id") == trip_id:
                return trip
        return None
    
    def add_pending_action(self, action_type: str, data: Dict[str, Any]):
        """Add a pending action to be synced when online"""
        action = {
            "type": action_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "id": f"{action_type}_{datetime.utcnow().timestamp()}"
        }
        self.data["pending_actions"].append(action)
        self._save_data()
    
    def get_pending_actions(self) -> List[Dict[str, Any]]:
        """Get all pending actions"""
        return self.data.get("pending_actions", [])
    
    def remove_pending_action(self, action_id: str):
        """Remove a pending action after successful sync"""
        self.data["pending_actions"] = [
            action for action in self.data["pending_actions"]
            if action.get("id") != action_id
        ]
        self._save_data()
    
    def clear_pending_actions(self):
        """Clear all pending actions"""
        self.data["pending_actions"] = []
        self._save_data()
    
    def is_online(self) -> bool:
        """Check if device is online (simple implementation)"""
        try:
            import requests
            requests.get("http://www.google.com", timeout=5)
            return True
        except:
            return False
    
    def get_last_sync(self) -> Optional[str]:
        """Get last sync timestamp"""
        return self.data.get("last_sync")
    
    def update_last_sync(self):
        """Update last sync timestamp"""
        self.data["last_sync"] = datetime.utcnow().isoformat()
        self._save_data()




