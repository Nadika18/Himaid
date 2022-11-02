import board
import busio
import digitalio
import time
import json
import adafruit_rfm9x


# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP13)
RESET = digitalio.DigitalInOut(board.GP21)
# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.GP25)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!
deviceid = 3
# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

while True:
    packet = rfm9x.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
    else:
        # Received a packet!
        LED.value = True
        try:
            packet_text = str(packet, "ascii")
        except:
            continue
        json_packet_text = json.loads(packet_text)

        print("Received (ASCII): {0}".format(packet_text))
        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))
   
        if deviceid != json_packet_text["i"]:
        	time.sleep(5)
        	print("Retransmitting")
        	rfm9x.send(bytes(packet_text,"utf-8"))        
