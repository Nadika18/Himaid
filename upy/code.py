import time
import board
import busio
import json
import digitalio
import adafruit_gps
import adafruit_rfm9x

def _format_datetime(datetime):
    return "{:02}:{:02}".format(
        datetime.tm_hour,
        datetime.tm_min,
    )

RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP13)
RESET = digitalio.DigitalInOut(board.GP21)

# Define the onboard LED ad PUSH_BUTTON
LED = digitalio.DigitalInOut(board.GP25)
LED.direction = digitalio.Direction.OUTPUT

BUTTON = digitalio.DigitalInOut(board.GP28)
BUTTON.direction = digitalio.Direction.INPUT

# Initialize SPI bus.
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
deviceid=1
rfm9x.tx_power = 23
  
prev_time = time.monotonic()
prev_send_time = time.monotonic() - 50

def senddata():
    LED.value = True
    print("button pressed")
    print("getting gps info")
    time.sleep(2)
    prev_update_time = time.monotonic()
    while True:
        gps.update()
        current_update_time = time.monotonic()
        if current_update_time - prev_update_time >= 1.0:
            prev_update_time = current_update_time
            if not gps.has_fix:
                print('Waiting for fix...')
                continue
            else:
                break
    print("Got GPS data, sending through lora")  # Print a separator line.
    gps_time = _format_datetime(gps.timestamp_utc)
    data = {
    "i" : deviceid,
    "l" : [gps.latitude,gps.longitude],
    "a" : gps.altitude_m,
    "t" : gps_time
    }
    #data = {
    #"i" : 1,
    #"l" : [27.6914,84.444],
    #"a" : 1300,
    #"t" : "13:22"
    #}
    json_encoded = json.dumps(data)
    rfm9x.send(bytes(json.dumps(data), "utf-8"))
    print("sent data")
    LED.value = False

while True:
    pack = rfm9x.receive()
    if pack is not None:
        try:
            packet_text = str(packet, "ascii")        
            json_packet_text = json.loads(packet_text)        
            print(json_packet_text)
            if(json_packet_text["i"] == "r" and json_packet_text["d"] == deviceid):
                senddata()
            else:
                rfm9x.send(bytes(packet_text, "utf-8"))
        except:
            continue

    curr_time = time.monotonic()
    if curr_time - prev_time >= 1800:
        gps.update()
        prev_time = curr_time
    LED.value = False
    if BUTTON.value == True:
        senddata()

