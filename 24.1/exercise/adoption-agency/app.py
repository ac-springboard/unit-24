from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import InputRequired, NumberRange, Optional

app = Flask(__name__)
app.config['SECRET-KEY'] = 'my-secret-key'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///unit_24"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


######################################################################
#                                                                    #
#                             ROUTES                                 #
#                                                                    #
######################################################################

@app.route('/')
@app.route('/list')
def list_view():
    return render_template('list.html')


@app.route('/add', methods=['GET', 'POST'])
def add_view():
    form = PetForm()
    if form.validate_on_submit():
        return redirect('/list')
    else:
        return render_template('form_add.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit_view():
    form = PetForm()
    if form.validate_on_submit():
        return redirect('/list')
    else:
        return render_template('form_edit.html', form=form)


######################################################################
#                                                                    #
#                              FORMS                                 #
#                                                                    #
######################################################################
class PetForm(FlaskForm):
    name = StringField('Pet Name*',
                       validators=[InputRequired(message='Pet Name is required')])
    species = StringField('Species*',
                          validators=[InputRequired(message='Species is required')])
    photo_url = StringField('Photo URL')
    age = IntegerField('Age',
                       validators=[Optional(), NumberRange(0, 150, message='Age must be between 0 and 150 or empty.')])
    notes = StringField('Notes')
    available = BooleanField('Available', default='yes')


######################################################################
#                                                                    #
#                             MODELS                                 #
#                                                                    #
######################################################################
class Pet(db.Model):
    """
    - Initializes the pets table on postgres.
    - Represents a post from the posts table.
    """
    __tablename__ = 'pets'

    def __init__(self, obj_dict):
        self.update_columns(obj_dict)

    # COLUMNS

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   index=True)
    name = db.Column(db.String(50),
                     nullable=False)
    species = db.Column(db.Text,
                        nullable=True)
    photo_url = db.Column(db.Text,
                          nullable=True)
    age = db.Column(db.Integer,
                    nullable=True)
    notes = db.Column(db.Text,
                      nullable=True)
    available = db.Column(db.Boolean,
                          default=True,
                          nullable=False)

    # METHODS

    def update_columns(self, dct):
        """
        Updates the data of this post from a dictionary.
        """
        self.id = dct.get('id', None)
        self.name = dct.get('title') or None
        self.species = dct.get('content') or None
        self.photo_url = dct.get('user_id') or None
        self.age = dct.get('user_id') or None
        self.notes = dct.get('user_id') or None
        self.available = dct.get('user_id') or True


######################################################################
#                                                                    #
#                        DATABASE SEEDING                            #
#                                                                    #
######################################################################
db.drop_all()
db.create_all()
db.session.commit()
