import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        
        # Get all audio files
        self.tracks = [f for f in os.listdir(music_folder) if f.endswith(('.wav', '.mp3'))]
        self.current_track = 0
        self.playing = False
        self.start_time = 0  
        self.paused_time = 0  
        self.current_position = 0  
        
        # Track information (artist and title)
        self.tracks_info = {
            "track1.wav": {"title": "Sample Guitar", "artist": "Guitar G-minor"},
            "track2.wav": {"title": "Simple Melody", "artist": "SampleTrack"},
        }
    
    def get_current_track_info(self):

        track_name = self.tracks[self.current_track]
        if track_name in self.tracks_info:
            info = self.tracks_info[track_name]
            return info.get('title', 'Unknown'), info.get('artist', 'Unknown Artist')
        return track_name, 'Unknown Artist'
    
    def get_current_time(self):

        if self.playing:
            elapsed = pygame.time.get_ticks() / 1000.0 - self.start_time
            return self.paused_time + elapsed
        return self.paused_time
    
    def play(self):
        if not self.tracks:
            print("No tracks found!")
            return
        path = os.path.join(self.music_folder, self.tracks[self.current_track])
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.playing = True
        self.start_time = pygame.time.get_ticks() / 1000.0
        self.paused_time = 0
        
        # Display track info in console
        title, artist = self.get_current_track_info()
        print(f"Now Playing: {title} - {artist}")
    
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused_time = 0
        self.current_position = 0
        print("Stopped")
    
    def next_track(self):
        self.stop()
        self.current_track = (self.current_track + 1) % len(self.tracks)
        self.play()
    
    def previous_track(self):
        self.stop()
        self.current_track = (self.current_track - 1) % len(self.tracks)
        self.play()
    
    def update(self):
        """Update current position (call this every frame)"""
        if self.playing:
            self.current_position = self.get_current_time()
    
    def quit(self):
        self.stop()
        pygame.mixer.quit()