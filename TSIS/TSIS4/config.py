import json
import os

class Config:
    def __init__(self, config_file="settings.json"):
        self.config_file = config_file
        self.default_settings = {
            "snake_color": [0, 255, 0],
            "grid_overlay": True,
            "sound_enabled": True,
            "username": "Player"
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key):
        """Get a setting value"""
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save_settings()