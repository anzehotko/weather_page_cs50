import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from collections import defaultdict
from datetime import datetime

from helpers import apology, login_required, lookup, search

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///weather.db")

# Make sure API key is set
os.environ["API_KEY"] = "f8ab2680eff6bdde9dd496be208ea565"
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")







@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Show weather data"""
    if request.method == "POST":
        if search(request.form.get("city")) == None:
            return apology("We couldn't find a city with a name similar to the one you provided.")
        list = search(request.form.get("city"))
        return render_template("search_result.html", list=list)

    else:
        return render_template("index.html")



@app.route("/city/<name>", methods=["GET", "POST"])
def city(name):
    global name1
    name1 = name
    city_inf = lookup(name1)
    urli = city_inf["urli"]
    forecast = city_inf["forecast"]
    return render_template("weatherlim.html", city_inf=city_inf, urli=urli, forecast=forecast)

@app.route("/hourly/<day>")
def hourly(day):
    city_inf = lookup(name1)
    forecast = city_inf["forecast"]
    info = forecast[day]
    hourly = defaultdict(list)
    for dict in info[:-1]:
        time_s = dict["dt_txt"]
        time_object = datetime.strptime(time_s, "%Y-%m-%d %H:%M:%S")
        time = time_object.strftime("%H:%M")
        temp = round(dict["main"]["temp"], 0)
        temperature = f"{temp} °C"
        icon = dict["weather"][0]["icon"]
        link1 = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        new_items = [temperature, link1]
        hourly[time] += new_items
    return render_template("hourly.html", hourly=hourly, day=day, name1=name1)

@app.route("/favorites")
@login_required
def favorites():
    """See the list of your favorite cities!"""
    existing = db.execute("SELECT favorite FROM users WHERE id=?", session["user_id"])
    favorites_names = existing[0]['favorite']
    if favorites_names == None:
        return apology("You have no favorites added to the list!")
    if ";" not in favorites_names:
        favorites_list = [favorites_names]
    else:
        favorites_list = favorites_names.split(";")
    return render_template("favorites.html", favorites_list=favorites_list)


@app.route("/add_favorites")
@login_required
def add_favorites():
    """Add current location to favorites"""
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]
    existing = db.execute("SELECT favorite FROM users WHERE username=?", username)
    intro = existing[0]['favorite']
    if intro == None:
        new = name1
        db.execute("UPDATE users SET favorite = ? WHERE username=?", new, username)
    else:
        new = f"{intro};{name1}"
        if name1 not in intro:
            db.execute("UPDATE users SET favorite = ? WHERE username=?", new, username)
        else:
            return apology("This location is already in your favourites list!")
    return city(name1)

@app.route("/remove_favorites/<name>")
@login_required
def remove_favorites(name):
    """Remove locations from your favorites list"""
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]
    existing = db.execute("SELECT favorite FROM users WHERE username=?", username)
    favorites_names = existing[0]['favorite']
    favorites_list = favorites_names.split(";")
    if name in favorites_list:
        favorites_list.remove(name)
        favorites_names = ";".join(favorites_list)
    db.execute("UPDATE users SET favorite = ? WHERE username=?", favorites_names, username)
    return favorites()




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't already exist
        if len(rows) != 0:
            return apology("username already exists")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password and confirmation match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation do not match!")

        # Add the user's entry into the database
        # Getting username and password from forms in "register.html" and storing them in separate variables.
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))


        # Insert new submission into SQL database!
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

