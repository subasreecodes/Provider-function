from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

app = Flask(__name__)

password = "password@123"
encoded_password = urllib.parse.quote_plus(password)

#old sql db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
#new sql db
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/user_test'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    doctor_name = db.Column(db.String(100))
    date = db.Column(db.String(10))  # String for simplicity in this example
    time = db.Column(db.String(8))   # String for simplicity in this example

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    bookings = Booking.query.all()
    return render_template('index.html', bookings=bookings)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    patient_name = request.form['patient_name']
    doctor_name = request.form['doctor_name']
    date = request.form['date']
    time = request.form['time']
    
    new_booking = Booking(patient_name=patient_name, doctor_name=doctor_name, date=date, time=time)
    db.session.add(new_booking)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete_booking/<int:id>', methods=['POST'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_booking/<int:id>', methods=['POST'])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.patient_name = request.form['patient_name']
    booking.doctor_name = request.form['doctor_name']
    booking.date = request.form['date']
    booking.time = request.form['time']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



