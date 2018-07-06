import os

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    book=db.execute("select * from books").fetchall()
    return render_template("index.html",book_title=book)

@app.route("/index",methods=["POST"])
def search():
    book_title=request.form.get("book_title")
    
    if db.execute("SELECT * FROM books WHERE title = :title", {"book_title": book_title}).rowcount == 0:
        return render_template("error.html", message="The book you are searching for does not exist.")


    info=db.execute("select * from books where title=:title").fetchall()
    return render_template("Details.html",info=info)
    
"""    
@app.route("/login")
def login():
    #login user
    username=request.form.get("uname")
    password=request.form.get("pwd")

    #
    if db.execute
"""
