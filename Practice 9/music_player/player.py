import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.tracks = [f for f in os.listdir(music_folder) if f.endswith(('.wav', '.mp3'))]
        self.current_track = 0
        self.playing = False

    def play(self):
        if not self.tracks:
            print("No tracks found!")
            return
        path = os.path.join(self.music_folder, self.tracks[self.current_track])
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.playing = True
        print(f"Playing: {self.tracks[self.current_track]}")

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        print("Stopped")

    def next_track(self):
        self.stop()
        self.current_track = (self.current_track + 1) % len(self.tracks)
        self.play()

    def previous_track(self):
        self.stop()
        self.current_track = (self.current_track - 1) % len(self.tracks)
        self.play()

    def quit(self):
        self.stop()
        pygame.mixer.quit()