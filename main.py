from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
from peewee import *

db = SqliteDatabase("users.db")
app = Flask(__name__)
    
class User(Model):
    name = TextField()
    age = IntegerField()
    StartDate = TextField(default=datetime.now())
    Country = TextField()
    EmergencyContact = TextField()
    DeviceID = IntegerField(primary_key=True, unique=True, null=False)
    class Meta:
        database = db

class Location(Model):
    DeviceID = ForeignKeyField(User, backref="DeviceID")
    Latitude = FloatField()
    Longitude = FloatField()
    LastUpdate = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    class Meta:
        database = db

# Connection to database and create tables
db.connect()
db.create_tables([User, Location])

# Index page
@app.route('/')
def dashboard():
    # Get all users
    users = User.select()
    for user in users:
        print(user.DeviceID)
    return render_template('dashboard.html', users=users)

# Register user route
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        country = request.form.get('country')
        emergency = request.form.get('contact')
        device = request.form.get('device')
        print(name, age, country, emergency, device)
        User.create(name=name, age=age, Country=country, EmergencyContact=emergency, DeviceID=device)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# Profile Route
@app.route('/profile/<int:age>')
def profile(age):
    user = User.get(User.age == age)
    return render_template('profile.html', user=user)

# server
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=8000)