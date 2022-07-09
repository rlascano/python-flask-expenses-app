from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Spent, Category
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        fecha = datetime.strptime(request.form.get('fecha'), "%Y-%m-%d")
        descripcion = request.form.get('descripcion')
        categoria_id = request.form.get('categoria')
        monto = request.form.get('monto')

        # TODO validar
        nuevo_gasto = Spent(date=fecha, description=descripcion, amount=monto,
                            category_id=categoria_id, user_id=current_user.id)
        db.session.add(nuevo_gasto)
        db.session.commit()
        return redirect(url_for('views.home'))

    categories = Category.query.all()
    return render_template('create.html', user=current_user, categories=categories)


'''
@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
'''
