from store import db, utils

from sqlalchemy import TextClause, text



def fetch_trending_games() -> list[dict]:
    query: str = """SELECT g.id, g.name, g.description, g.price, g.thumbnail_path
                    FROM games g
                    JOIN game_tag gt ON g.id = gt.game_id
                    JOIN tags t ON gt.tag_id = t.id
                    WHERE t.name = 'Trending';"""
    result_set = db.session.execute(text(query))
    trending_games = result_set.mappings().all()
    return trending_games


def fetch_game_by_name(name: str) -> dict:
    query: TextClause = text("SELECT * FROM games WHERE name = :name;")
    result_set = db.session.execute(query, {"name": name})
    game: dict | None = result_set.mappings().one_or_none()
    return game


def fetch_game_by_gameid(gameid: str) -> dict:
    query: TextClause = text("SELECT * FROM games WHERE id = :gameid;")
    result_set = db.session.execute(query, {"gameid": gameid})
    game: dict | None = result_set.mappings().one_or_none()
    return game


def fetch_userid_by_username(username: str) -> int | None:
    query: TextClause = text("SELECT id FROM users WHERE name = :name;")
    result_set = db.session.execute(query, {"name": username})
    user: dict | None = result_set.mappings().one_or_none()
    if user is None:
        return None
    return user.get("id")


def fetch_gameid_by_gamename(gamename: str) -> int | None:
    query: TextClause = text("SELECT id FROM games WHERE name = :name;")
    result_set = db.session.execute(query, {"name": gamename})
    game: dict | None = result_set.mappings().one_or_none()
    if game is None:
        return None
    return game.get("id")


def fetch_game_owned(userid: int, gameid: int) -> bool | None:
    query: TextClause = text("SELECT game_id FROM user_game WHERE user_id = :userid;")
    result_set = db.session.execute(query, {"userid": userid})
    gameids: list[int] = utils.flattened(result_set.fetchall())
    return gameid in gameids


def add_game_to_user(userid: int, gameid: int):
    query: TextClause = text("INSERT INTO user_game (user_id, game_id) VALUES (:userid, :gameid);")
    result_set = db.session.execute(query, {"userid": userid, "gameid": gameid})
    db.session.commit()


def fetch_games_owned(userid: int) -> list[dict]:
    query: TextClause = text("SELECT game_id FROM user_game WHERE user_id = :userid;")
    result_set = db.session.execute(query, {"userid": userid})
    gameids_owned = utils.flattened(result_set.fetchall())
    games_owned = []
    for gameid_owned in gameids_owned:
        game_owned = fetch_game_by_gameid(gameid_owned)
        if game_owned is not None:
            games_owned.append(game_owned)

    return games_owned


def insert_game(gamename, description, price, thumbnail_path):
    query: TextClause = text("""INSERT INTO games (name, description, price, thumbnail_path) VALUES
        (:name, :description, :price, :thumbnail_path);""")
    result_set = db.session.execute(query, {"name": gamename, "description": description,
        "price": price, "thumbnail_path": thumbnail_path})
    db.session.commit()


def add_game_to_trending(gameid):
    query: TextClause = text("""INSERT INTO game_tag (game_id, tag_id) VALUES (:gameid, :tagid);""")
    result_set = db.session.execute(query, {"gameid": gameid, "tagid": 5})
    db.session.commit()
