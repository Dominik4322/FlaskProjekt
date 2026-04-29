from flask import Blueprint, request, render_template
from extensions import db
from models import Game
from services.igdb_service import search_games
import datetime
from flask import redirect

main = Blueprint("main", __name__)


# 🔍 Strona główna + wyszukiwanie
@main.route("/", methods=["GET", "POST"])
def home():
    games = []

    if request.method == "POST":
        name = request.form.get("name")

        if name:
            games = search_games(name)

            # konwersja daty z timestamp
            for g in games:
                if "first_release_date" in g:
                    g["first_release_date"] = datetime.datetime.fromtimestamp(
                        g["first_release_date"]
                    ).strftime("%Y-%m-%d")

    return render_template("index.html", games=games)


# 💾 Dodawanie gry do bazy
@main.route("/add-game", methods=["POST"])
def add_game():
    igdb_id = request.form.get("igdb_id")
    name = request.form.get("name")
    rating = request.form.get("rating")
    release_date = request.form.get("release_date")

    existing = Game.query.filter_by(igdb_id=igdb_id).first()

    if not existing:
        game = Game(
            igdb_id=igdb_id,
            name=name,
            rating=float(rating) if rating else None,
            release_date=release_date if release_date else None
        )

        db.session.add(game)
        db.session.commit()

    # 👇 TO ZAMIENIA JSON NA NAWIGACJĘ
    return redirect("/")


# 📚 Lista zapisanych gier (na razie JSON)
@main.route("/my-games")
def my_games():
    games = Game.query.all()

    return render_template("my_games.html", games=games)

@main.route("/delete-game/<int:id>", methods=["POST"])
def delete_game(id):
    game = Game.query.get(id)

    if game:
        db.session.delete(game)
        db.session.commit()

    return redirect("/my-games")