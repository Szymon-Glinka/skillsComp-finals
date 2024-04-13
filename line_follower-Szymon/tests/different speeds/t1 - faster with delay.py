import RPi.GPIO as GPIO
from gpiozero import Motor
import time

class RobotSee():
	def analogRead(self):
		"""Funtion used to read values from IR sensord"""
		value = [0,0,0,0,0,0]

		#== Read Channel0~channel4 AD value ==
		for j in range(0,6):
			GPIO.output(5, GPIO.LOW)
			for i in range(0,4):
				#--- sent 4-bit at adress 24 ---
				if(((j) >> (3 - i)) & 0x01):
					GPIO.output(24,GPIO.HIGH)
				else:
					GPIO.output(24,GPIO.LOW)
				#--- read MSB(most significant) 4-bit data ---
				value[j] <<= 1
				if(GPIO.input(23)):
					value[j] |= 0x01
				GPIO.output(25,GPIO.HIGH)
				GPIO.output(25,GPIO.LOW)

			for i in range(0,6):
				#--- read LSB(least significant bit) 8-bit data ---
				value[j] <<= 1
				if(GPIO.input(23)):
					value[j] |= 0x01
				GPIO.output(25,GPIO.HIGH)
				GPIO.output(25,GPIO.LOW)
			time.sleep(0.005)
			GPIO.output(5,GPIO.HIGH)
		return value[1:]

	def covnvertTOmoves(self, readArray):
		"""Function that converts data from array into moves"""
        #--- Set data from array to their corresponding values ---
		leftMax = readArray[0]
		left = readArray[1]
		forward = readArray[2]
		right = readArray[3]
		rightMax = readArray[4]

		millis = round(time.time()*1000)



		#--- dummy variable ---
		lastRead = ""

		#== a bach of if's that convert values from variables into understable code ==
		#--- if line in the middle is detected return F (forward) ---
		if forward < 350 and forward < left and forward < right:
			lastRead = "F"
			return "F"

		#--- if line on the right sensor is detected return R(slightly right) ---        
		elif right < 350 and right < forward and right < rightMax:
			lastRead = "R"
			return "R"

		#--- if line on the far right is detected return MR(max right) ---
		elif rightMax < 350 and rightMax < right:
			lastRead = "MR"
			return "MR"

		#--- if line on the left is detected return L(slightly left) ---
		elif left < 350 and left < forward and left < leftMax:
			lastRead = "L"
			return "L"

		#--- if line on the far left is detected return ML(max left) ---
		elif leftMax < 350 and leftMax < left:
			lastRead = "ML"
			return "ML"

		else:
			return lastRead

class RobotMove():
	#--- initialize PWM ---
	def __init__(self):
		"""A set of functions that generates motion"""
		self.leftPWM = GPIO.PWM(6,1000)
		self.rightPWM = GPIO.PWM(26,1000)
		
	#--- Move forward - both motors with the same speed and in the same direction ---
	def forward(self):
		self.leftPWM.start(80)
		self.rightPWM.start(80)
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
    #--- Stop robot ---
	def stop(self):
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)

    #--- Move a little bit to the left with left motor and decreased speed ---
	def littleLeft(self):
		self.leftPWM.start(24)
		self.rightPWM.start(24)
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
    #--- move a little bit to the right with right motor and decreased speed ---
	def littleRight(self):
		self.leftPWM.start(24)
		self.rightPWM.start(24)
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)

    #--- move sharp to the left with speed decreased even more and with two motors spinning oppositely ---
	def sharpLeft(self):
		self.leftPWM.start(24)
		self.rightPWM.start(24)
		GPIO.output(21, GPIO.LOW)
		GPIO.output(20, GPIO.HIGH)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
	
    #--- move sharp to the right with speed decreased even more and with two motors spinning oppositely ---
	def sharpRight(self):
		self.leftPWM.start(24)
		self.rightPWM.start(24)
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.HIGH)


#== Main program's loop ==
if __name__ == "__main__":
    #== initialize gpio ==
	gpios = [25, 24, 5, 6, 26, 12, 13, 20, 21] #define gpio pines
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(23,GPIO.IN,GPIO.PUD_UP)

    #--- set up gpio according to the array ---
	for io in gpios:
		GPIO.setup(io,GPIO.OUT)


    #--- create object move and see ---
	move = RobotMove()
	see = RobotSee()

    #== infinite loop to run the algorythm ==
	while True:
		array = see.analogRead() #read data from ir sensors
		moves = see.covnvertTOmoves(array) #convert data from sensors into instrucions

        #--- Move the robot ---
		if moves == "F":
			move.forward()
		elif moves == "R":
			move.littleRight()
		elif moves == "L":
			move.littleLeft()
		elif moves == "MR":
			move.sharpRight()
		elif moves == "ML":
			move.sharpLeft()

		time.sleep(0.01)