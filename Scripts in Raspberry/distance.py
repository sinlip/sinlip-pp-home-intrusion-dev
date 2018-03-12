#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
import redis

r = redis.Redis(host='REPLACE WITH REDIS URL', port='REPLACE WITH REDIS PORT', password='REPLACE WITH REDIS PASSWORD')


# The callback for 
def checkdist():
	GPIO.output(16, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(16, GPIO.LOW)
	while not GPIO.input(18):
		pass
	t1 = time.time()
	while GPIO.input(18):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)

old_d = 0
diff = 3

time.sleep(2)
try:
	while True:
		d = checkdist()
		print 'Distance: %0.2f m' %d
#		publish.single("topic/sinlip/distance" , d , hostname="test.mosquitto.org")
		percent_diff = old_d/d
		if percent_diff > diff:
			r.set('intrusion', 1)
			r.set('intrusion_timestamp', time.time())
		old_d = d
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()

