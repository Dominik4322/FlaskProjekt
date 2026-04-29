from flask import Blueprint, request, render_template
from services.igdb_service import search_games
import datetime

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    games = []

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            games = search_games(name)

            # 👇 TUTAJ to dodajesz
            for g in games:
                if "first_release_date" in g:
                    g["first_release_date"] = datetime.datetime.fromtimestamp(
                        g["first_release_date"]
                    ).strftime("%Y-%m-%d")

    return render_template("index.html", games=games)