from flask import Flask, render_template, request, redirect, jsonify

from utils.db import db
from models.medic import *


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medic.db'

@app.route('/')
def index():
    patient = Patients.query.all()
    return render_template('index.html',  content=patient)

@app.route('/patients')
def patients():
    return render_template('patient.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/submit", methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    age = form_data.get('age')
    bmi = form_data.get('bmi')
    children = form_data.get('children')
    charges = form_data.get('charges')
    region = form_data.get('region')


    patient = Patients.query.filter_by(age=age).first()
    if not patient:
        patient = Patients(age=age, bmi=bmi, children=children, charges=charges, region=region)
        db.session.add(patient)
        db.session.commit()
    print("sumitted successfully")
    return redirect('/')



@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_user(id):
    task = Patients.query.get(id)
    print("task: {}".format(task))

    if not task:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
        data = request.json
        patient = Patients.query.get(patient_id)  # Assuming you're using SQLAlchemy

        if patient:
            patient.age = data['age']
            patient.bmi = data['bmi']
            patient.children = data['children']
            patient.charges = data['charges']
            patient.region = data['region']

            db.session.commit()
            return jsonify({"message": "Patient updated successfully"})
        else:
            return jsonify({"message": "Patient not found"}), 404


@app.route('/add', methods=['POST'])
def add_patient():
    try:
        # Get the data from the request
        data = request.get_json()

        # Create a new patient instance
        patient = Patients(
            age=data.get('age'),
            bmi=data.get('bmi'),
            children=data.get('children'),
            charges=data.get('charges'),
            region=data.get('region')
        )

        # Add to the database
        db.session.add(patient)
        db.session.commit()

        # Respond with a success message
        return jsonify({'message': 'Patient added successfully'}), 201

    except Exception as e:
        # Handle errors
        db.session.rollback()  # Rollback in case of error
        return jsonify({'message': str(e)}), 400


if __name__ =='__main__':
    app.run(host='127.0.0.1',port=5003,debug=True)