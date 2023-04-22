from flask import session, request, redirect, render_template, Response, request
import spotipy
from .user import User
from .game import Game, MAX_TURNS
from personal_heardle import app

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    session["game"] = Game()

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-library-read user-top-read",
        cache_handler=cache_handler,
        show_dialog=True,
    )

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("index.html", auth_url=auth_url)

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    session["user"] = User(spotify)
    return redirect("/play")


@app.route("/play", methods=["POST", "GET"])
def game_page():
    if request.method == "GET":
        new_song = session["game"].pick_new_song(session["user"])
        session["user"].played_songs.append(new_song)
    else:
        guess = request.form["guess"]
        won_game, n_rounds = session["game"].check_guess(guess)
        if won_game:
            wins, games = session["user"].add_score(n_rounds)
            session["n_wins"] = wins
            session["n_games"] = games
            session.modified = True

            return redirect("/winner")
        if n_rounds == MAX_TURNS:
            wins, games = session["user"].add_score(0)
            session["n_wins"] = wins
            session["n_games"] = games
            session.modified = True

            return redirect("/loser")
    session.modified = True
    print(session["game"].end_sample)
    return render_template(
        "play.html",
        songs=session["user"].song_list["name"].values,
        guesses=session["game"].past_guesses,
        colours=session["game"].guess_colors,
        n_guesses=len(session["game"].past_guesses),
        player_name=session["user"].name,
    )


@app.route("/winner")
def win_game():
    return render_template(
        "end.html",
        message="You know your music!",
        song=session["game"].song,
        plot_url=session["user"].get_plot(),
        n_wins=session["n_wins"],
        n_games=session["n_games"],
    )


@app.route("/loser")
def lose_game():
    return render_template(
        "end.html",
        message="Sorry You're Not a Winner",
        song=session["game"].song,
        plot_url=session["user"].get_plot(),
        n_wins=session["n_wins"],
        n_games=session["n_games"],
    )


@app.route("/wav")
def streamwav():
    session.modified = True
    return Response(session["game"].play_music(), mimetype="audio/x-wav")


@app.route("/sign_out")
def sign_out():
    session.pop("token_info", None)
    return redirect("/")
