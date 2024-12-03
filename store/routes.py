import os
from typing import Any

from store import app, db, queries, utils, THUMBNAIL_UPLOAD_DIRECTORY

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import text



@app.route("/")
def home_page():
    cookie = request.cookies.get("name")
    print("<>home_page", cookie)

    query: str = "SELECT name FROM tags;"
    tags = utils.flattened(db.session.execute(text(query)).fetchall())
    trending_games: list[dict] = queries.fetch_trending_games()
    return render_template("home.jinja", tags=tags, trending_games=trending_games, cookie=cookie)


@app.route("/users")
def users_page():
    query: str = f"SELECT * FROM users"
    result_set: Any = db.session.execute(text(query))
    users = result_set.mappings().all()
    return render_template("users.jinja", users=users)


@app.route("/games")
def games_page():
    cookie = request.cookies.get("name")
    print("<>games_page", cookie)
    if not cookie:
        return redirect(url_for("login_page"))
    query: str = f"SELECT * FROM games"
    result_set: Any = db.session.execute(text(query))
    games = result_set.mappings().all()
    return render_template("games.jinja", games=games, cookie=cookie)


@app.route("/library")
def library_page():
    cookie = request.cookies.get("name")
    print("<>library_page", cookie)
    if not cookie:
        return redirect(url_for("login_page"))
    username = cookie
    games_owned = queries.fetch_games_owned(queries.fetch_userid_by_username(username))
    print(games_owned)
    return render_template("library.jinja", games_owned=games_owned, cookie=cookie)


@app.route("/add_game", methods=["GET", "POST"])
def add_game_page():
    cookie = request.cookies.get("name")
    print("<>library_page", cookie)
    if not cookie:
        return redirect(url_for("login_page"))

    username = cookie

    if request.method == "GET":
        return render_template("add_game.jinja", cookie=cookie)
    elif request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        thumbnail = request.files["thumbnail"]
        try:
            upload_path = os.path.join(THUMBNAIL_UPLOAD_DIRECTORY, thumbnail.filename)
            thumbnail.save(upload_path)
        except Exception as e:
            print(e)
            return {"msg": "error"}, 500
        queries.insert_game(name, description, price, upload_path.split(
            "/home/tizian/hochschule_albstadt-sigmaringen/hacking_mit_python/gamestore/store"
        )[1])
        gameid = queries.fetch_gameid_by_gamename(name)
        queries.add_game_to_trending(gameid)
        return render_template("add_game.jinja", cookie=cookie)



@app.route("/game/<string:name>")
def game_page(name: str):
    username = request.cookies.get("name")
    owned = False
    gameid = queries.fetch_gameid_by_gamename(name)
    game: dict = queries.fetch_game_by_name(name)

    if username is None:
        return render_template("game.jinja", name=game["name"], price=game["price"],
            description=game["description"], thumbnail_path=game["thumbnail_path"], game_id=game["id"],
            owned=owned, cookie=username)


    owned = queries.fetch_game_owned(queries.fetch_userid_by_username(username),
        queries.fetch_gameid_by_gamename(name))
    return render_template("game.jinja", name=game["name"], price=game["price"],
        description=game["description"], thumbnail_path=game["thumbnail_path"], game_id=game["id"],
        user_id=queries.fetch_userid_by_username(username), owned=owned, cookie=username)


@app.route("/buy_game", methods=["POST"])
def buy_game():
    body = request.json
    print(body)
    userid = body.get("userId")
    gameid = body.get("gameId")
    queries.add_game_to_user(userid, gameid)
    return "Success"



@app.route('/login', methods=['GET','POST'])
def login_page():
    print(">>>>>>login_page")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or isinstance(username, str) is False:
            print("something wrong with username")
            return render_template('login.jinja', cookie=None)
        if password is None or isinstance(username, str) is False or len(password) < 3:
            print("something wrong with password")
            return render_template('login.jinja', cookie=None)


        query_stmt = f"select name from users where name='{username}' and password='{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        user = result.fetchone()
        print(user)

        # ' UNION SELECT GROUP_CONCAT(CONCAT(name, ':', password)) FROM users#
        # ' UNION SELECT GROUP_CONCAT(name, ':', password SEPARATOR ';') FROM users#
        if not user:
            print("try again ....")
            #flash(f"Try again", category='warning')
            return render_template('login.jinja', cookie=None)

        resp = redirect("/")
        print(user)
        resp.set_cookie("name", user[0])
        return resp

    return render_template('login.jinja', cookie=None)


@app.route('/logout')
def logout():
    print(">>>>>>>logout_page")
    resp = redirect("/")
    resp.set_cookie("name", "", expires=0)
    return resp



@app.route("/register", methods=["GET", "POST"])
def register_page():
    print(">>>>>>register_page")
    if request.method == "POST":
        username = request.form.get("username")
        email_address = request.form.get("emailAddress")
        password = request.form.get("password")

        if username is None or isinstance(username, str) is False:
            print("something wrong with username")
            return render_template("register.jinja")
        if email_address is None or isinstance(email_address, str) is False:
            print("something wrong with email_address")
            return render_template("register.jinja")
        if password is None or isinstance(username, str) is False or len(password) < 3:
            print("something wrong with password")
            return render_template("register.jinja")

        query = f"INSERT INTO users (name, email_address, password) VALUES ('{username}', '{email_address}', '{password}')"
        result = db.session.execute(text(query))
        db.session.commit()

        return redirect(url_for("games_page"))

    return render_template("register.jinja")
