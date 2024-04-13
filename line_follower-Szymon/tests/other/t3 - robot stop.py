import RPi.GPIO as GPIO
from gpiozero import Motor
import time


def analogRead():
	value = [0,0,0,0,0,0]
	#Read Channel0~channel4 AD value
	for j in range(0,6):
		GPIO.output(5, GPIO.LOW)
		for i in range(0,4):
			#sent 4-bit 24
			if(((j) >> (3 - i)) & 0x01):
				GPIO.output(24,GPIO.HIGH)
			else:
				GPIO.output(24,GPIO.LOW)
			#read MSB 4-bit data
			value[j] <<= 1
			if(GPIO.input(23)):
				value[j] |= 0x01
			GPIO.output(25,GPIO.HIGH)
			GPIO.output(25,GPIO.LOW)
		for i in range(0,6):
			#read LSB 8-bit data
			value[j] <<= 1
			if(GPIO.input(23)):
				value[j] |= 0x01
			GPIO.output(25,GPIO.HIGH)
			GPIO.output(25,GPIO.LOW)
		time.sleep(0.05)
		GPIO.output(5,GPIO.HIGH)
	return value[1:]

def covnvertTOmoves(readArray):
	leftMax = readArray[0]
	left = readArray[1]
	forward = readArray[2]
	right = readArray[3]
	rightMax = readArray[4]

	if forward < left and forward < right:
		return "F"

	elif right < forward and right < rightMax:
		return "R"

	elif rightMax < right:
		return "MR"

	elif left < forward and left < leftMax:
		return "L"

	elif leftMax < left:
		return "ML"

class MoveRobot():
	def forward(self):
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
	def stop(self):
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)

	def littleLeft(self):
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
	def littleRight(self):
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)

	def sharpLeft(self):
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.HIGH)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
	def sharpRight(self):
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.HIGH)




if __name__ == "__main__":
	gpios = [25, 24, 5, 6, 26, 12, 13, 20, 21]
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(23,GPIO.IN,GPIO.PUD_UP)
	for io in gpios:
		GPIO.setup(io,GPIO.OUT)

	GPIO.output(6, GPIO.HIGH)
	GPIO.output(26, GPIO.HIGH)

	move = MoveRobot()

	while True:
		move.stop()