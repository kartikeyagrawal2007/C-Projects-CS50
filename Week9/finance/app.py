import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    stocks = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares >0
        """,
        session["user_id"]
    )
    total = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total"] = stock["shares"] * stock["price"]
        total += stock["total"]
    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        session["user_id"]
    )[0]["cash"]

    grand_total = total + cash

    return render_template(
        "index.html",
        stocks=stocks,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol")
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")
        if not shares:
            return apology("must provide shares")
        if not shares.isdigit():
            return apology("shares must be a positive integer")
        shares = int(shares)
        if shares <= 0:
            return apology("shares must be a positive integer")
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]["cash"]
        total_cost = stock["price"] * shares
        if total_cost > cash:
            return apology("can't afford")
        db.execute(
            """
            INSERT INTO transactions
            (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
            """,
            session["user_id"],
            stock["symbol"],
            shares,
            stock["price"]
        )
        db.execute(
            """
            UPDATE users
            SET cash = ?
            WHERE id = ?
            """,
            cash - total_cost,
            session["user_id"]
        )
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        """
        SELECT symbol,
            shares,
            price,
            transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
        """,
        session["user_id"]
    )

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")
        quote = lookup(symbol)
        if quote is None:
            return apology("Invalid symbol")
        return render_template(
            "quoted.html",
            quote=quote
        )
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if not confirmation:
            return apology("must confirm password")
        if password != confirmation:
            return apology("passwords do not match")
        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password)
            )
        except ValueError:
            return apology("username already exists")
        session["user_id"] = user_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit():
            return apology("Invalid shares")
        shares = int(shares)
        owned = db.execute(
            """
            SELECT SUM(shares) AS total
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            """,
            session["user_id"],
            symbol.upper()
        )[0]["total"]
        if owned is None or owned < shares:
            return apology("too many shares")
        stock = lookup(symbol)
        value = shares * stock["price"]

        db.execute(
            """
            INSERT INTO transactions
            (user_id, symbol, shares, price)
            VALUES (?,?,?,?)
            """,
            session["user_id"],
            stock["symbol"],
            -shares,
            stock["price"]
        )
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]["cash"]
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash + value,
            session["user_id"]
        )
        return redirect("/")

    stocks = db.execute(
        """
        SELECT symbol
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
        """,
        session["user_id"]
    )

    return render_template("sell.html", stocks=stocks)
