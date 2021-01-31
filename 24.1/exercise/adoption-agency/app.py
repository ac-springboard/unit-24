from flask import Flask, render_template, redirect, request

from forms import PetForm

app = Flask(__name__)
app.config['SECRET-KEY'] = 'my-secret-key'
app.config['WTF_CSRF_ENABLED'] = False


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
