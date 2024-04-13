import RPi.GPIO as GPIO
from gpiozero import Motor
from gpiozero import PWMOutputDevice
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

	if forward < 350 and forward < left and forward < right:
		return "F"

	elif right < 350 and right < forward and right < rightMax:
		return "R"

	elif rightMax < 350 and rightMax < right:
		return "MR"

	elif left < 350 and left < forward and left < leftMax:
		return "L"

	elif leftMax < 350 and leftMax < left:
		return "ML"

	else:
		return "F"

class MoveRobot():
	def __init__(self):
		self.m1a = PWMOutputDevice(21)
		self.m1b = PWMOutputDevice(20)
		self.m2a = PWMOutputDevice(12)
		self.m2b = PWMOutputDevice(13)

	def forward(self):
		self.m1a.value = 0.1
		self.m1b.value = 0
		self.m2a.value = 0.1
		self.m2b.value = 0
	
	def stop(self):
		self.m1a.value = 0
		self.m1b.value = 0
		self.m2a.value = 0
		self.m2b.value = 0

	def littleLeft(self):
		self.m1a.value = 0.1
		self.m1b.value = 0
		self.m2a.value = 0
		self.m2b.value = 0
	
	def littleRight(self):
		self.m1a.value = 0
		self.m1b.value = 0
		self.m2a.value = 0.1
		self.m2b.value = 0

	def sharpLeft(self):
		self.m1a.value = 0.15
		self.m1b.value = 0
		self.m2a.value = 0
		self.m2b.value = 0.15
	
	def sharpRight(self):
		self.m1a.value = 0
		self.m1b.value = 0.15
		self.m2a.value = 0.15
		self.m2b.value = 0




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
		array = analogRead()
		moves = covnvertTOmoves(array)

		if moves == "F":
			move.forward()
		elif moves == "R":
			move.littleRight()
		elif moves == "L":
			move.littleLeft()
		elif moves == "MR":
			move.littleRight()
		elif moves == "ML":
			move.littleLeft()
		
		print(moves)