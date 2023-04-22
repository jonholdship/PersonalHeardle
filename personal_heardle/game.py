import spotipy
import requests
import pandas as pd


TURN_LENGTHS = [15, 30, 50, 90, 150]
MAX_TURNS = len(TURN_LENGTHS)
CORRECT_ARTIST = "#e79840"
WRONG_GUESS = "#b14530"


class Game:
    """
    Controls the current game state including the song list, what has been played, and the current state of any specific game
    """

    def __init__(self) -> None:
        pass

    def check_guess(self, guess):
        self.past_guesses[self.end_sample] = guess
        correct_guess = guess == self.song["name"]
        if self.song["artists"] == guess.split("-")[0].strip():
            self.guess_colors[self.end_sample] = CORRECT_ARTIST
        else:
            self.guess_colors[self.end_sample] = WRONG_GUESS

        self.end_sample += 1
        return correct_guess, self.end_sample

    def pick_new_song(self, user):
        self.song = user.song_list.sample(1).squeeze()
        while self.song["name"] in user.played_songs:
            self.song = user.song_list.sample(1).squeeze()

        self.song_data = requests.get(self.song["url"]).content

        self.end_sample = 0
        self.past_guesses = len(TURN_LENGTHS) * [""]
        self.guess_colors = len(TURN_LENGTHS) * ["#444444"]
        return self.song["name"]

    def play_music(self):
        end = TURN_LENGTHS[self.end_sample] * 1024
        i = 0
        while i < end:
            yield self.song_data[i : i + 1024]
            i += 1024
