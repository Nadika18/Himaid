from flask import Flask, render_template, url_for, redirect, request, jsonify
from datetime import datetime
from peewee import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
from datetime import datetime
import json

if os.uname().nodename == "rpi":
    import board
    import busio
    import digitalio
    import adafruit_rfm9x

    RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    LED = digitalio.DigitalInOut(board.D13)
    LED.direction = digitalio.Direction.OUTPUT
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
    rfm9x.tx_power = 23

db = SqliteDatabase("users.db")
app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
class BaseTable(Model):
    class Meta:
        database = db

class Device(BaseTable):
    serial_number = IntegerField(unique=True)
    occupied = BooleanField()

class User(BaseTable):
    name = TextField()
    age = IntegerField()
    StartDate = TextField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Country = TextField()
    fileName= TextField()
    EmergencyContact = TextField()
    DeviceID = ForeignKeyField(Device, backref="id")

class Location(BaseTable):
    DeviceID = ForeignKeyField(Device, backref="id")
    Latitude = FloatField()
    Longitude = FloatField()
    LastUpdate = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Connection to database and create tables
db.connect()
db.create_tables([User,Device, Location])

# Index page
@app.route('/')
def dashboard():
    users = User.select()
    return render_template('dashboard.html', users=users)

# Register user route
@app.route('/register',methods=['GET','POST'])
def register():
    try:
        devices = Device.select()
    except:
        devices = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        country = request.form.get('country')
        emergency = request.form.get('contact')
        device = request.form.get('dev_id')
        file=request.files['file']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        print("________{}________".format(device))
        User.create(name=name, age=age, Country=country, EmergencyContact=emergency, DeviceID=device,fileName=filename)
        Device.update({Device.occupied: True}).where(Device.id == device).execute()

        return redirect(url_for('dashboard'))
    return render_template('register.html', devices = devices)

# Register user route
@app.route('/registerdevice',methods=['GET','POST'])
def registerdevice():
    if request.method == 'POST':
        devid = request.form.get('dev-id')
        occupied = False
        Device.create(id=1,serial_number=devid, occupied=occupied)
        return redirect(url_for('dashboard'))
    return render_template('register-device.html')

# Profile Route
@app.route('/profile/<int:device>')
def profile(device):
    user = User.get(User.DeviceID == device)
    try:
        location = Location.get(Location.DeviceID == device)
        lat = location.Latitude
        lon = location.Longitude
    except:
        lat = 28.37
        lon = 83.67
    return render_template('profile.html', user=user, lat=lat, long=lon)

@app.route('/delete/<username>')
def delete(username):
    obj=User.get(User.DeviceID==username)
    Device.update({Device.occupied: False}).where(Device.id == obj.DeviceID).execute()
    obj.delete_instance()
    return redirect(url_for('dashboard'))

@app.route('/update')
def update():
    if os.uname().nodename == "rpi":
        packet = rfm9x.receive()
        if packet is not None:
            LED.value = True
            rssi = rfm9x.last_rssi
            try:
                packet_text = str(packet,"ascii")
            except:
                return jsonify({})
            packet_json = json.loads(packet_text)
            try:
                print(packet_json["l"])
                loc = Location.get(Location.Latitude == packet_json["l"][0])
            except:
                Location.create(DeviceID = packet_json["i"], Latitude = packet_json["l"][0], Longitude = packet_json["l"][1])
            LED.value = False
            return jsonify(packet_json)
        LED.value = False
    return jsonify({})
        
# server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8000)

