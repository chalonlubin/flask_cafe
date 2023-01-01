"""Flask App for Flask Cafe."""

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os

from forms import AddCafeForm, SignupForm, LoginForm
from models import db, connect_db, Cafe, City, User
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskcafe'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to cafe list.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    do_logout()

    form = SignupForm()

    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            description=form.description.data,
            password=form.password.data,
            email=form.email.data,
            image_url=form.image_url.data or None,
        )

        try:
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)

        flash("You are signed up and logged in.")
        return redirect("/cafes")

    else:
        return render_template('auth/signup-form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login. Redirects on success to cafe list."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/cafes")

        flash("Invalid credentials.", 'danger')

    return render_template('auth/login-form.html', form=form)

@app.post('/logout')
def logout():
    """Handle logout of user. Redirects to homepage."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")

#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""
    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    return render_template("homepage.html")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    """Show Form / Add Cafe"""

    form = AddCafeForm()
    form.city_code.choices = City.choices_vocab()

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or None,
        )

        db.session.add(cafe)
        db.session.commit()

        flash(f"{cafe.name} added.", "success")
        return redirect(f"/cafes/{cafe.id}")

    return render_template('/cafe/add-form.html', form=form)


@app.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    """Show Edit Form / Edit Cafe Details"""

    cafe = Cafe.query.get_or_404(cafe_id)
    form = AddCafeForm(obj=cafe)
    form.city_code.choices = City.choices_vocab()

    if form.validate_on_submit():
        cafe.name = form.name.data,
        cafe.description = form.description.data,
        cafe.url = form.url.data,
        cafe.address = form.address.data,
        cafe.city_code = form.city_code.data,
        cafe.image_url = form.image_url.data or None

        db.session.commit()

        flash(f"{cafe.name} edited.", "success")
        return redirect(f"/cafes/{cafe_id}")

    else:
        return render_template('cafe/edit-form.html', cafe=cafe, form=form)
