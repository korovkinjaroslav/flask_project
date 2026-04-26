from flask import Flask
from models.data import db_session
from models.data.users import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
db_session.global_init("main_directory/models/db/database.db")


@app.route("/")
def start():
    db_sess = db_session.create_session()
    return str(db_sess.query(User).count())


def main():
    app.run()


if __name__ == '__main__':
    main()
