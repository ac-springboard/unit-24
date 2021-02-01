from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, HiddenField
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
@app.route('/pets/list')
def list_view():
    pets = get_all_pets()
    return render_template('list.html', pets=pets, page_title="Pet List")


@app.route('/pets/add', methods=['GET', 'POST'])
def add_view():
    form = AddPet()
    if not form.validate_on_submit():
        return render_template('form_add.html', form=form, page_title='Add Pet')
    pet = Pet(form.data)
    add_pet(pet)
    return redirect('/pets/list')


@app.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_view(pet_id):
    pet = get_pet_by_id(pet_id)
    form = EditPet(obj=pet)
    if not form.validate_on_submit():
        return render_template('form_edit.html', form=form, page_title='Edit Pet')
    pet.update_columns(form.data)
    edit_pet(pet)
    return redirect('/pets/list')


######################################################################
#                                                                    #
#                              FORMS                                 #
#                                                                    #
######################################################################
class EditPet(FlaskForm):
    id = HiddenField()
    name = StringField('Pet Name*',
                       validators=[InputRequired(message='Pet Name is required')])
    species = StringField('Species*',
                          validators=[InputRequired(message='Species is required')])
    photo_url = StringField('Photo URL')
    age = IntegerField('Age',
                       validators=[Optional(), NumberRange(0, 150, message='Age must be between 0 and 150 or empty.')])
    notes = StringField('Notes')
    available = BooleanField('Available', default=True)


class AddPet(FlaskForm):
    name = StringField('Pet Name*',
                       validators=[InputRequired(message='Pet Name is required')])
    species = StringField('Species*',
                          validators=[InputRequired(message='Species is required')])
    photo_url = StringField('Photo URL')
    age = IntegerField('Age',
                       validators=[Optional(), NumberRange(0, 150, message='Age must be between 0 and 150 or empty.')])
    notes = StringField('Notes')
    available = BooleanField('Available', default=True)


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
        self.name = dct.get('name') or None
        self.species = dct.get('species') or None
        self.photo_url = dct.get('photo_url') or None
        self.age = dct.get('age') or None
        self.notes = dct.get('notes') or None
        self.available = dct.get('available') or True


######################################################################
#                                                                    #
#                           REPOSITORY                               #
#                                                                    #
######################################################################
def get_all_pets():
    return Pet.query.all()


def add_pet(pet):
    db.session.add(pet)
    db.session.commit()
    db.session.refresh(pet)
    return pet.id


def edit_pet(pet):
    db.session.commit()
    return pet.id


def get_pet_by_id(pet_id):
    return Pet.query.get_or_404(pet_id)


######################################################################
#                                                                    #
#                        DATABASE SEEDING                            #
#                                                                    #
######################################################################
db.drop_all()
db.create_all()

barbecue = Pet({
    'name': 'Barbecue',
    'species': 'Cat',
    'photo_url': '',
    'age': '17',
    'notes': 'Needs more spicy',
    'available': True
})

cooked = Pet({
    'name': 'Cooked',
    'species': 'Chicken',
    'photo_url': '',
    'age': '0',
    'notes': 'Soooo tender...',
    'available': True
})

frozen = Pet({
    'name': 'Frozen',
    'species': 'Duck',
    'photo_url': '',
    'age': '45',
    'notes': 'Expired',
    'available': True
})

db.session.add_all([barbecue, cooked, frozen])
db.session.commit()
