import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
# import json

from helpers import error, getquotes, lookup, login_required
from database import *

# Configure application
app = Flask(__name__, template_folder='templates')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
UPLOAD_FOLDER = 'static/images/users'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# upload blog post images
UPLOAD_BLOG_IMAGE = 'static/images/blogs'
app.config['UPLOAD_BLOG_IMAGE'] = UPLOAD_BLOG_IMAGE

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# that didn't work for some reasons i'm too lazy to investigate
# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///C:/Users/NANO COMP/Desktop/website/PBooks.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")
# \Users\NANO COMP\Desktop\website\PBooks.db


@app.route("/")
def index():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("index.html", name=username)
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("about.html", name=username)
    else:
        return render_template("about.html")


# I hate myself for hardcoding this
# the articles
@app.route("/articles")
def articles():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("articles.html", name=username)
    else:
        return render_template("articles.html")

@app.route("/article1")
def article1():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article1.html", name=username)
    else:
        return render_template("article1.html")

@app.route("/article2")
def article2():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article2.html", name=username)
    else:
        return render_template("article2.html")

@app.route("/article3")
def article3():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article3.html", name=username)
    else:
        return render_template("article3.html")

@app.route("/article4")
def article4():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article4.html", name=username)
    else:
        return render_template("article4.html")

@app.route("/article5")
def article5():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article5.html", name=username)
    else:
        return render_template("article5.html")

@app.route("/article6")
def article6():
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("article6.html", name=username)
    else:
        return render_template("article6.html")     


@app.route("/quotes")
def quotes():

    # inport the quotes
    quotes = getquotes()

    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("quotes.html", name=username, quotes=quotes)
    else:
        return render_template("quotes.html", quotes=quotes)
    
@app.route("/readability", methods=["GET", "POST"])
def readability():

    if request.method == "POST":
        if request.form.get("button") == "submit":
            
            # variables 
            txt = request.form.get("textarea")
            letters = 0
            words = 1
            sentences = 0
            for i in range(len(txt)):
                if txt[i].isalpha():
                    letters += 1
    
                elif txt[i].isspace():
                    words += 1
        
                elif txt[i] == "." or txt[i] == "?" or txt[i] == "!":
                    sentences += 1
            
            # calculate the grade
            grade = 0.0588 * (100 * (letters / words)) - 0.296 * (100 * (sentences / words)) - 15.8

            txtgrade = ""
            if grade < 1:
                txtgrade = "Before Grade 1"
                
            elif grade > 16:
                txtgrade = "Grade 16+"
            else:
                txtgrade = f"Grade {round(grade)}"
            
            display = True
            if session.get("user_id"):
                username = get_username(session["user_id"])[0][0]
                return render_template("readability.html", text=txt,letters=letters, words=words, sentences=sentences, txtgrade=txtgrade, display=display, name=username)
            else:
                return render_template("readability.html", text=txt,letters=letters, words=words, sentences=sentences, txtgrade=txtgrade, display=display)
        # else:
        #     return render_template("readability.html")
    # else:
    else:
        if session.get("user_id"):
            username = get_username(session["user_id"])[0][0]
            return render_template("readability.html", name=username)
        else:
            return render_template("readability.html")

# search page
@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "POST":
        if request.form['button'] == 'searchbook':
            if not request.form.get('search'):
                return error("Must Provide Book!", 400)
            
            inp = request.form.get('search')
            bookinfo = lookup(inp)

            if len(bookinfo) < 1 :
                return error("Must Provide Book!", 400)
            else:
                if session.get("user_id"):
                    username = get_username(session["user_id"])[0][0]
                    return render_template("search.html", name=username, inp=inp, bookinfo=bookinfo)
                else:
                    return render_template("search.html", inp=inp, bookinfo=bookinfo)
        
    else:
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        username = request.form.get("username").lower()
        result = select_user(username)
        

        # Ensure username exists and password is correct
        if len(result) != 1 or not check_password_hash(result[0][2], request.form.get("password")):
            return error("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = result[0][0]

        # Redirect user to home page
        # flash("Successfully logged in!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/users")
@login_required
def users():
    result = get_users()
    # usersnames = []
    # for i in range(result):
    #     usersnames.append(f"{result[i][1]}")
    # username = get_username(session["user_id"])[0][0]
    # notes = getnotes(session["user_id"])f"<h1>{}</h1>"
    return 


# def user():
#     result = get_user(session["user_id"])
#     img = f"static/images/users/{result[0][1]}.png"
#     name = result[0][1]
#     return render_template("layout.html", name=name, img=img)


@app.route("/home")
@login_required
def home():
    # get user and userinfo
    dude = get_user(session["user_id"])
    dudeinfo = get_userinfo(session["user_id"])
    dudename = dude[0][1]
    # dudeimg = f"static/images/users/{dudename}.png"

    # get user's notes
    notes = getnotes(session["user_id"])
    return render_template("home.html", info=dudeinfo, name=dudename, notes=notes)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    flash("Successfully logged out. BYEEE!")
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = select_user(username)

        # Ensure the username doesn't exists
        if len(rows) != 0:
            return error("username already exists", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return error("passwords must match", 400)

        
        # Generate the hash of the password  (, method="pbkdf2:sha256", salt_length=8)
        hashword = generate_password_hash(password)
        # pfp = "C:\\Users\\NANO COMP\\Desktop\\website\\static\\images\\avatar.gif"

        # Insert the new user
        # primkey = insert_user(username.lower(), hashword, email, convertToBinaryData(pfp))
        primkey = insert_user(username.lower(), hashword, email)
        if primkey is None:
            return error("OKAY, what did you do this time You little #%& ?!", 400)
        
        session["user_id"] = primkey
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        
        if request.form['btn'] == 'Delete Account':

            pwd = request.form.get("password")
            result = get_user(session["user_id"])
            if not check_password_hash(result[0][2], pwd):
                return error("Wrong password", 400)
            else:
                session.clear()
                flash("Ironicly Account Deleted !")
                return redirect("/account")

        if request.form['btn'] == 'Save Changes':

            fullname = request.form.get("fullname")
            profession = request.form.get("prof")
            address = request.form.get("address")
            pinfo = request.form.get("pinfo")

            userinfo = get_userinfo(session["user_id"])
            if len(userinfo) >= 1:
                update_user = update_userinfo(fullname, profession, address, pinfo, session["user_id"])
                if update_user:
                    flash("Personal info Updated !")
                    return redirect("/account")
            else:
                insertinfo = insert_userinfo(fullname, profession, address, pinfo, session["user_id"])
                if insertinfo:
                    flash("Personal info saved !")
                    return redirect("/account")
            

        if request.form['btn'] == 'Save Password':

            oldpassword = request.form.get("oldpassword")
            newpassword = request.form.get("newpassword")
            confirmation = request.form.get("confirmation")

            result = get_user(session["user_id"])
            if not check_password_hash(result[0][2], oldpassword):
                return error("Wrong former password", 400)
            elif newpassword != confirmation:
                return error("Password and confirmation must match", 400)

            update = update_password(generate_password_hash(newpassword), session["user_id"])
            if update:
                flash("Password changed !")
                return redirect("/account")
            
        if request.form['btn'] == 'Upload':
            if request.files:
                result = get_user(session["user_id"])
                newpfp = request.files["inputimg"]
                # newpfp.save(f'static/images/users/newpfp')
                if newpfp.filename == '' or not newpfp and not allowed_file(newpfp.filename):
                    return error("What on earth are you tryna upload, dumbass ?!")
                
                filename = secure_filename(newpfp.filename)
                newpfp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                with open(f"static/images/users/{filename}", 'rb') as rimg:
                    with open(f"static/images/users/{result[0][1]}.png", 'wb') as wimg:
                        for line in rimg:
                            img = wimg.write(line)
                
                os.remove(f"static/images/users/{filename}")
                flash("profil picture updated!")
                return redirect("/account")

        if request.form['btn'] == 'deletepic':
            username = get_username(session["user_id"])[0][0]
            with open(f"static/images/avatar.gif", 'rb') as rimg:
                    with open(f"static/images/users/{username}.png", 'wb') as wimg:
                        for line in rimg:
                            img = wimg.write(line)

            flash("profil picture deleted!")
            return redirect("/account")
            
    else:
        result = get_user(session["user_id"])
        info = get_userinfo(session["user_id"])
        # img = writeTofile(result[0][-1], f"static/images/users/{result[0][1]}.png")
        img = f"static/images/users/{result[0][1]}.png"
        return render_template("account.html", result=result, info=info, name=result[0][1])


# NOT_ALLOWED_CHARS = {'\'','"','[',']','{','}','`','&','^','%','/'}
# def scan_txt(txt):
#     text = txt
#     for j in txt:
#         # if j in NOT_ALLOWED_CHARS:
#         #     text.replace(j, '')
#         return text


@app.route("/addblog", methods=["GET", "POST"])
@login_required
def addblog():
    if request.method == "POST":

        title = request.form.get("title")
        intro = request.form.get("intro")
        mainbody = request.form.get("mainbody")
        conclusion = request.form.get("conclusion")
        author = get_username(session["user_id"])[0][0]

        if request.files:
            image = request.files["image"]
            if image.filename == '' or not image and not allowed_file(image.filename):
                return error("What on earth are you tryna upload, dumbass ?!")
            
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_BLOG_IMAGE'], filename))

            with open(f"static/images/blogs/{filename}", 'rb') as rimg:
                with open(f"static/images/blogs/{title}.png", 'wb') as wimg:
                    for line in rimg:
                        img = wimg.write(line)
            
            os.remove(f"static/images/blogs/{filename}")
            inserted = insertpost(title, intro, mainbody, conclusion, author)
            if inserted:
                flash("Blog Post Published !")
                return redirect(request.url)
    else:
        username = get_username(session["user_id"])[0][0]
        return render_template("addblog.html", name=username)


@app.route("/blogposts", methods=["GET", "POST"])
# @login_required
def blogposts():
    if request.method == "POST":
        title = request.form["title"]
        return redirect(url_for('blogpost', title=title))
    else:
        # get all posts from db in descesnding order
        if session.get("user_id"):
            username = get_username(session["user_id"])[0][0]
            posts = get_posts()
            return render_template("blogposts.html", posts=posts, name=username)
        else:
            posts = get_posts()
            return render_template("blogposts.html", posts=posts)


@app.route("/myposts", methods=["GET", "POST"])
@login_required
def myposts():
    if request.method == "POST":
        if request.form["btn"] == "readmore":
            title = request.form["title"]
            return redirect(url_for('blogpost', title=title))
        if request.form["btn"] == "delete":
            title = request.form["title"]
            username = get_username(session["user_id"])[0][0]
            deleted = deletepost(title, username)
            if deleted:
                os.remove(f"static/images/blogs/{title}.png")
                flash("Post Deleted!")
                return redirect('/myposts')
    else:
        # get user's posts from db in descesnding order
        username = get_username(session["user_id"])[0][0]
        result = get_myposts(username)
        return render_template("myposts.html", name=username, posts=result)


@app.route("/users/leedafuq")
def leedafuq():
    return render_template("users.html")

@app.route("/blogpost/<title>")
# @login_required
def blogpost(title):

    # get post from db where title = title
    result = getpost(title)
    
    if session.get("user_id"):
        username = get_username(session["user_id"])[0][0]
        return render_template("blogpost.html", name=username, result=result)
    else:
        return render_template("blogpost.html",result=result)

@app.route("/notebook", methods=["GET", "POST"])
@login_required
def notebook():
    if request.method == "POST":
        if request.form["btn"] == "addnote":
            title = request.form.get("notitle")
            content = request.form.get("content")
            # insert notes into db with user_id and datetime
            added = addnote(title, content, session["user_id"])
            if added:
                flash("Note Added Successefully!")
                return redirect(request.url)

        # if request.form["btn"] == "editnote":
        #     content = request.form.get("content")
        #     edited = editnote(content, session["user_id"])
        #     if edited:
        #         flash("Note Edited Successefully!")
        #         return redirect(request.url)

        if request.form["btn"] == "deletenote":
            title = request.form["title"]
            deleted = deletenote(title, session["user_id"])
            if deleted:
                flash("Note Deleted Successefully!")
                return redirect(request.url)
    else:
        # get all notes from db in descending order
        username = get_username(session["user_id"])[0][0]
        notes = getnotes(session["user_id"])
        return render_template("notebook.html", name=username, notes=notes)







def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

