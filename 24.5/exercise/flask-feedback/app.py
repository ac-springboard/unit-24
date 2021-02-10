"""Feedback Flask app."""
import os

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from decorators import authenticated, authorized
from models import connect_db, db, User, Feedback
from repository import reset_tables_with_test_users, set_test_authorizations
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

# CONFIG ENVIRONMENT

# os.environ["FLASK_RUN_FROM_CLI"] = "true"
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_APP'] = 'app.py'

# CREATE AND CONFIG THE APP

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# DATABASE

connect_db(app)
reset_tables_with_test_users(db)
# set_test_authorizations()


def logged_user(lu):
    logu = lu

    def get_logged_user():
        nonlocal logu
        return logu

    return get_logged_user

glu = None

# ROUTES


@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        global glu
        glu = logged_user(user)

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            global glu
            glu = logged_user(user)
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
@authenticated
def logout():
    """Logout route."""

    session.pop("username")
    logged_user( None )
    return redirect("/login")


@app.route("/users/<username>")
@authenticated
def show_user(username):
    """Example page for logged-in-users."""

    # if "username" not in session or username != session['username']:
    #     raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form, is_authorized=is_authorized)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
@authenticated
def new_feedback(username):
    """Show add-feedback form and process it."""

    # if "username" not in session or username != session['username']:
    #     raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
@authenticated
@authorized('update_feedback')
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    # if "username" not in session or feedback.username != session['username']:
    #     raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
@authenticated
@authorized('delete_feedback')
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    # if "username" not in session or feedback.username != session['username']:
    #     raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")


@app.route("/feedback")
@authenticated
def list_feedbacks():
    # logged_username = session['username']
    # logged_user = User.query.filter_by(username=logged_username).first()
    feedbacks = Feedback.query.all()
    return render_template('/feedback/list.html',
                           logged_user=glu(),
                           feedbacks=feedbacks,
                           is_authorized=is_authorized)


@app.route("/contact-us")
def contact_us():
    return render_template('admin/contact_us.html')


def is_authorized(ref_user_username, resource_key):
    global glu
    return glu().is_admin or glu().username == ref_user_username or resource_key in glu().get_authorizations()


# @app.errorhandler(302)
# def error_302():
#     return render_template('302.html')


# @app.errorhandler(404)
# def error_404():
#     return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
