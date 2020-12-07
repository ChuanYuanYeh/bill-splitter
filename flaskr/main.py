from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    return render_template('main/index.html')

@bp.route('/upload')
def upload():
    return render_template('main/upload.html')

@bp.route('/manual')
def manual():
    return render_template('main/manual.html')

@bp.route('/add_friend', methods=('GET', 'POST'))
@login_required
def add_friend():
    if request.method == 'POST':
        names = request.form['names']
        error = None

        if not names:
            error = 'At least one name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            for name in names.split(','):
                db.execute(
                    'insert into friend (user_id, full_name)'
                    ' values (?, ?)',
                    (g.user['id'], name)
                )
            db.commit()
            return redirect(url_for('main.view_friend'))

    return render_template('main/add_friend.html')

@bp.route('/view_friend', methods=['GET'])
@login_required
def view_friend():
    db = get_db()
    friends = db.execute(
        'select full_name from friend order by full_name asc'
    ).fetchall()
    return render_template('main/view_friend.html', posts=friends)
