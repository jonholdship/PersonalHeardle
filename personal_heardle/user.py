import pandas as pd
import re
import json
from .game import MAX_TURNS
import io
import base64
import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "figure.facecolor": (1.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
        "axes.facecolor": (0.0, 1.0, 0.0, 0.0),  # green with alpha = 50%
        "axes.edgecolor": (1.0, 1.0, 1.0, 1.0),
        "text.color": (1.0, 1.0, 1.0, 1.0),
        "savefig.facecolor": (1.0, 1.0, 1.0, 0.0),  # blue  with alpha = 20%
        "ytick.color": (1.0, 1.0, 1.0, 1.0),
        "font.size": 22,
    }
)


def make_name(row):
    name = f"{row['artists']} - {row['track']}"
    name = re.sub("\(.*\)", "", name)
    return name.strip()


def parse_spotify_to_df(json_res):
    df = pd.DataFrame(
        [
            {
                "artists": " and ".join(
                    [artist["name"] for artist in item["track"]["artists"]]
                ),
                "url": item["track"]["preview_url"],
                "track": item["track"]["name"],
                "image": item["track"]["album"]["images"][0]["url"],
            }
            for item in json_res
        ]
    )
    df["name"] = df.apply(make_name, axis=1)
    df = df.dropna()
    return df


USER_DATABASE = "data/users.json"
with open(USER_DATABASE, "r") as f:
    users = json.load(f)


class User:
    def __init__(self, spotify):
        self.name = spotify.me()["display_name"]
        self.id = spotify.me()["id"]
        if self.id not in users:
            self.song_list = self.get_song_list(spotify)
            users[self.id] = self.create_new_user()
            self.song_list.to_csv(users[self.id]["song_list"], index="False")
        else:
            self.song_list = pd.read_csv(users[self.id]["song_list"])
        self.played_songs = users[self.id]["played_songs"]

    def get_song_list(self, spotify):
        results = spotify.current_user_saved_tracks()
        tracks = results["items"]
        while results["next"]:
            results = spotify.next(results)
            tracks.extend(results["items"])
        return parse_spotify_to_df(tracks)

    def create_new_user(self):
        return {
            "games_played": 0,
            "scores": {str(i): 0 for i in range(0, MAX_TURNS + 1)},
            "song_list": f"data/song_lists/{self.id}.csv",
            "played_songs": [],
        }

    def add_score(self, rounds=None):
        users[self.id]["games_played"] += 1

        if rounds:
            users[self.id]["scores"][str(rounds)] += 1
            users[self.id]["played_songs"] = self.played_songs

        with open(USER_DATABASE, "w") as f:
            json.dump(users, f)
        wins = sum(int(y) for y in users[self.id]["scores"].values())

        return wins, users[self.id]["games_played"]

    def get_plot(self):
        scores = users[self.id]["scores"]
        x = [int(x) for x in scores.keys()]
        y = [int(y) for y in scores.values()]

        fig, ax = plt.subplots(figsize=(8, 4), tight_layout=True)
        ax.barh(x, y, color="#45735A")
        for i in range(len(x)):
            if y[i] > 0:
                ax.text(y[i] - 0.2, i + 1, str(y[i]), color="white", va="center")
        ax.set(ylabel="Number of Guesses")
        ax.spines[["right", "top", "bottom"]].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.yaxis.label.set_color("white")

        # no axis changes beyond here
        img = io.BytesIO()
        plt.savefig(img, format="png", dpi=600)
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        return plot_url
