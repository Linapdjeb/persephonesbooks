import requests
import urllib.parse
import csv

from flask import redirect, render_template, request, session
from functools import wraps

from random import seed
from random import randint

# seed random number generator
seed(1)


def error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(book):
    """Look up quote for symbol."""

    # Contact API :keyes&key{api_key}
    try:
        api_key = "AIzaSyBk6Tiitk-jMehsQiYA2jpl_MdSu2H4irY"
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(book)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        items = quote["items"]

        with open('books.txt', 'w') as f:
            writer = csv.writer(f)
            for key in items[:10]: #.items() , value
                # writer.writerow([key, value])
                writer.writerow(key)

        bookinfo = items[:10]
        return bookinfo
    except (KeyError, TypeError, ValueError):
        return None


def getquotes():
    """Look up quote for symbol."""

    # Contact API :keyes&key{api_key}
    try:
        url = f"http://api.quotable.io/quotes?page={randint(0, 90)}"
        response = requests.get(url)

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quotes = response.json()
        noice = quotes['results']
        # with open('user.txt', 'w') as f:
        #     writer = csv.writer(f)
        #     for i in noice: #.items() , value
        #         # writer.writerow([key, value])
        #         writer.writerow(i)

        return noice
    except (KeyError, TypeError, ValueError):
        return None


# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"

