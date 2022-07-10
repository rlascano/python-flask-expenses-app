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


@views.route('/new')
@login_required
def new():
    categories = Category.query.all()
    return render_template('new.html', user=current_user, categories=categories)


@views.route('/create', methods=['POST'])
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
        flash("Registro agregado correctamente")
        return redirect(url_for('views.home'))


@views.route('/edit/<int:id>')
@login_required
def edit(id):
    spent = Spent.query.get(id)
    categorias = Category.query.all()

    return render_template('edit.html', spent=spent, user=current_user, categories=categorias)


@views.route('/update/<int:id>', methods=['POST'])
def update(id):
    spent = Spent.query.get(id)
    if request.method == 'POST':
        fecha = datetime.strptime(request.form.get('fecha'), "%Y-%m-%d")
        descripcion = request.form.get('descripcion')
        categoria_id = request.form.get('categoria')
        monto = request.form.get('monto')

        # TODO validar
        spent.date = fecha
        spent.description = descripcion
        spent.category_id = categoria_id
        spent.amount = monto
        db.session.add(spent)
        db.session.commit()
        flash("Registro editado correctamente")
        return redirect(url_for('views.home'))


@views.route('/delete<int:id>', methods=['POST'])
def delete(id):
    spent = Spent.query.get(id)
    db.session.delete(spent)
    db.session.commit()
    flash('Registro borrado correctamente')
    return redirect(url_for('views.home'))
