from personal_heardle import app
import os

"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    app.run(
        threaded=True,
        port=int(
            os.environ.get(
                "PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 5000).split(":")[-1]
            )
        ),
    )
