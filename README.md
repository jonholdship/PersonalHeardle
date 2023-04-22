# Personal Heardle

A game based on [Heardle](https://www.heardle.app) which uses your Spotify account to play songs you know. 

## Set Up
PersonalHeardle is a Python/Flask app, requirements for which can be found in `requirements.txt`. Once all requirements are installed, you simply run

```flask run```

from the repository root directory. This will launch a web app which you can access via browser.

### Spotify Developer
Spotify's API requires that you register any app that will interact with it. In doing so you will be given a client ID and secret. Your app set up requires you to specify the URL to which spotify should redirect users after authenticating, this should be your app url as the "/" Flask route handles log in. If you're in development mode, you will also need to register the email addresses associated with the Spotify accounts of anyone who will use the app.

Once set up, you should create a `config.yaml` file in the main directory and include the following keys: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI`. These are required for your app to run.
