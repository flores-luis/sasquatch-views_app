from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

@app.route('/new')
def new_sighting():
    return render_template('create.html')

@app.route('/new/sighting',methods=['POST'])
def create_():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sightings(request.form):
        return redirect('/new')
    data = {
        "Location": request.form["Location"],
        "Comments": request.form["Comments"],
        "sighting_date": request.form["sighting_date"],
        "sasquatch_number": request.form["sasquatch_number"],
        "user_id": session["user_id"]
    }
    Sighting.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("update.html",edit=Sighting.get_one(data),user=User.get_by_id(user_data))

@app.route('/update_db',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sightings(request.form):
        return redirect('/new')
    data = {
        "Location": request.form["Location"],
        "Comments": request.form["Comments"],
        "sighting_date": request.form["sighting_date"],
        "sasquatch_number": request.form["sasquatch_number"],
        "id": request.form["id"],
        "user_id": session['user_id']
    }
    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("read.html",sighting=Sighting.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sighting.destroy(data)
    return redirect('/dashboard')
