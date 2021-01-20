from flask import render_template, jsonify, request
from app import app, models, db
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/added', methods=['POST'])
def added():
    fname = request.form.get("fname")
    # Add TmpUser to db
    # Create a temporary friend
    tmpFriend = models.TmpFriend(
        name=fname
    )
    # Insert the friend in the database
    db.session.add(tmpFriend)
    db.session.commit()
    # Get the user from the database
    check = models.TmpFriend.query.filter_by(name=fname).first()
    message = 'Successfully added {}'.format(check.get_name())
    return render_template("index.html", title='Home', message=message)


@app.route('/items', methods=['GET'])
def items():
    return render_template("items.html", title='Add Items')
