#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
	text = input("Spotify Album ID to write to tag: ")
	print("Place the tag on the reader. Waiting for tag...")
	reader.write(text)
	print("ID written to tag!")
finally:
	GPIO.cleanup()





