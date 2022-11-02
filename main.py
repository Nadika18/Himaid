from typing import Text
from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
from peewee import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
# from playhouse.migrate import *


db = SqliteDatabase("users.db")
app = Flask(__name__)
# migrator = SqliteMigrator(db)

UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# migrate(
#     migrator.add_column('user', 'title', title_field),
#     migrator.add_column('some_table', 'status', status_field),
#     migrator.drop_column('some_table', 'old_column'),
# )
    
class BaseTable(Model):
    class Meta:
        database = db
class User(BaseTable):
    name = TextField()
    age = IntegerField()
    StartDate = TextField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Country = TextField()
    fileName= TextField()
    EmergencyContact = TextField()
    DeviceID = IntegerField(primary_key=True, unique=True, null=False)
    
    class Meta:
        database = db

class Location(BaseTable):
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
        file=request.files['file']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        print(name, age, country, emergency, device,filename)
        User.create(name=name, age=age, Country=country, EmergencyContact=emergency, DeviceID=device,fileName=filename)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# Profile Route
@app.route('/profile/<int:age>')
def profile(age):
    user = User.get(User.age == age)
    return render_template('profile.html', user=user)

@app.route('/delete/<username>')
def delete(username):
    obj=User.get(User.name==username)
    obj.delete_instance()
    return redirect(url_for('dashboard'))
    

# server
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=5000)