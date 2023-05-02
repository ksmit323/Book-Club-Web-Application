import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from runoff import main

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookclub.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show homepage"""

    return render_template("index.html")


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
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(pw)
        check_username = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username is not blank
        if not username:
            return apology("Username can't be blank", 400)

        # Ensure passwords are not left blank
        elif not pw or not confirmation:
            return apology("Password fields can't be blank", 400)

        # Ensure username does not exist already
        elif len(check_username) == 1:
            return apology("Username already taken", 400)

        # Ensure passwords match
        elif pw != confirmation:
            return apology("Passwords don't match", 400)

        else:
            # Add user to the "users" table
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            # Assign the id to the session to remember who logged in
            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]
            # Return to the homepage
            flash("Registered!", "success")
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/suggest", methods=["GET", "POST"])
def suggest():
    """Allow user to make book suggestions"""

    # Variable to track who is logged in
    id = session["user_id"]

    if request.method == "POST":

        # Variables to retrieve information
        name = request.form.get("name")
        suggest1 = request.form.get("suggest1")
        suggest2 = request.form.get("suggest2")

        # Ensure user inputs name
        if not name:
            return apology("Put yo name in, bro!", 403)

        # Ensure user inputs at least one suggestion
        elif not suggest1 and not suggest2:
            return apology("Need at least one book suggestion, yo!", 403)

        # Ensure the user does not suggest the same book twice
        elif suggest1.upper() == suggest2.upper():
            return apology("You can't suggest the same book twice, bro!")

        # Insert info to "suggestions" table
        db.execute("INSERT INTO suggestions (userid, name, suggestion_1, suggestion_2) VALUES(?, ?, ?, ?)", id, name, suggest1, suggest2)

        flash("Thank you for your suggestion!", "success")
        return redirect("/")

    else:

        # Return user to the homepage if they have already suggested something
        rows = db.execute("SELECT * FROM suggestions WHERE userid = ?", id)
        if len(rows) == 1:
            flash("You already made your suggestions, bro!", "error")
            return redirect("/")

        return render_template("suggest.html")

@app.route("/change", methods=["GET", "POST"])
def change():
    """Allow user to change book suggestions"""

    # Variable to track who is logged in
    id = session["user_id"]

    if request.method == "POST":

        # Variables to retrieve information
        change1 = request.form.get("change1")
        change2 = request.form.get("change2")
        suggest1 = db.execute("SELECT suggestion_1 FROM suggestions WHERE userid=?", id)[0]["suggestion_1"].upper()
        suggest2 = db.execute("SELECT suggestion_2 FROM suggestions WHERE userid=?", id)[0]["suggestion_2"].upper()

        # Ensure user inputs at least one suggestion
        if not change1 and not change2:
            return apology("You didn't enter any changes, yo!", 403)

        # Ensure the user does not suggest the same book twice
        elif change1.upper() == change2.upper():
            return apology("You can't suggest the same book twice, bro!")

        # Ensure the user does not suggest a book they already suggested
        elif change1.upper() == suggest1 or change1.upper() == suggest2:
            return apology("You already suggested that book, bro!")

        elif change2.upper() == suggest1 or change2.upper() == suggest2:
            return apology("You already suggested that book, bro!")

        # Update user's first suggestion if they changed it
        if change1:
            db.execute("UPDATE suggestions SET suggestion_1 = ? WHERE userid = ?", change1, id)

        # Update user's second suggestion if they changed it
        if change2:
            db.execute("UPDATE suggestions SET suggestion_2 = ? WHERE userid = ?", change2, id)

        flash("You have successfully changed your suggestion!", "success")
        return redirect("/")

    else:
        # Return user to the homepage if they haven't yet suggested anything
        rows = db.execute("SELECT * FROM suggestions WHERE userid = ?", id)
        if len(rows) == 0:
            flash("You haven't suggested anything yet, bro!", "error")
            return redirect("/")

        else:
            return render_template("change.html")


@app.route("/recommendations", methods=["GET"])
def recommendations():
    """Allow user to view all recommendations made so far"""

    recommendations = db.execute("SELECT * FROM suggestions")

    # Return to homepage if no suggestions have been made yet
    if len(recommendations) == 0:
        flash("No recommendations yet, bro!", "error")
        return redirect("/")

    # Render table of all suggested books
    else:
        return render_template("recommendations.html", recommendations=recommendations)


@app.route("/vote", methods=["GET", "POST"])
def vote():
    """Allow user to vote on books to choose"""

    # Variable to track who is logged in
    id = session["user_id"]

    if request.method == "POST":

        # Variables to retrieve info
        first = request.form.get("first")
        second = request.form.get("second")
        third = request.form.get("third")

        # User must input a first choice
        if not first:
            return apology("You need a First Choice, bro!")

        # Insert votes into "vote" table
        else:
            db.execute("INSERT INTO votes (userid, first, second, third) VALUES(?, ?, ?, ?)", id, first, second, third)
            flash("You have succesfully voted, bro!", "success")
            return redirect("/")

    else:

        # Return user to the homepage if they have already voted
        rows = db.execute("SELECT * FROM votes WHERE userid = ?", id)
        if len(rows) == 1:
            flash("You already voted, bro!", "error")
            return redirect("/")

        else:
            suggestions = db.execute("SELECT * FROM suggestions")
            return render_template("vote.html", suggestions=suggestions)


@app.route("/results", methods=["GET", "POST"])
def results():
    """Allow users to see the results of the vote"""

    # Only render results if everyone has voted based on the number of registered users
    if len(db.execute("SELECT * FROM votes")) < len(db.execute("SELECT * FROM users")):
        flash("Voting has not ended yet, bro!")
        return redirect("/")

    else:
        winner = main()
        return render_template("results.html", winner=winner)