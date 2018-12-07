import time
import nexmo
import datetime
import os
import bluetooth


curr = datetime.datetime.now()

registeredAddr = {
					"8C:85:90:AA:AF:B0" : "Emmanuel Sedicol", 
					"84:98:66:29:21:6A" : "Nathaniel Sedicol",
					"84:98:66:29:21:6B" : "Maria Sedicol",
					"84:98:66:29:21:6C" : "James Sedicol"
				 }

number = {	
		"Emmanuel Sedicol": 35386376743,
		"Nathaniel Sedicol":35386376743,
		"James Sedicol": 35386376743,
		"Maria Sedicol": 35386376743		
		}

foundAddr = [] 

def comapare(registeredAddr, foundAddr, number):
	os.system('clear')
	print ('''
		============================================
			    Presence Detection
		============================================
		  ''')
	print("\t\t[ Current Time: ", curr.hour,"hr",  " : " , curr.minute,"min", " : ", curr.second, "sec ]\n\n")
	
	try:
		for x in registeredAddr:
			if x in foundAddr:
				name = registeredAddr[x]
				print ("-> [ ",name , " is on the Bus ]\n")
	except:
		print("No Device Found")

	try:
		print("\n< ------------------------- Absent ..... ------------------------- >\n")
		for x in registeredAddr:
			if x not in foundAddr:
				name = registeredAddr[x]
				no = number[name]
				print ("\t\t[ ",name, " is not Present!!!!!! ]\n")
				sendMessage(no, name)
	except:
		print("No Device Found")




def sendMessage(sendTo, name):
	c = nexmo.Client(key='4179aed7', secret='B6ED8JS3Kap5bIsI')
	c.send_message({
		    'from': 'Nexmo',
		    'to': str(sendTo),
		    'text': '%s missed the bus on (%d/%d/%d.)' % (name, curr.month, curr.day, curr.year)
		})
	print("\t[ Current Balance -->", c.get_balance() ,"]")
	print("\t<-- Alert message sent to [ ", name, "] parents!!!!! -->\n\n")
	


def main():
	os.system('clear')
	print ('''
		============================================
			 Parental Monitor Application
		============================================
		  ''')

	for x in range(0, 11):
		time.sleep(.2)
		count = x
		print ("	Bus Closing in => ", (10 - x ))
			
	print("\n< ------------------------- Calculating ..... ------------------------- >\n")

	nearby_devices = bluetooth.discover_devices(lookup_names=True)
	print("\n\t\t\t[ Number of devices found %d ]" % len(nearby_devices))


	for addr, name in nearby_devices:
		print("\t\t[ %s - %s ]"% (addr, name))
		foundAddr.append(addr)

		comapare(registeredAddr, foundAddr, number)
		countemptySeat(foundAddr)


def countemptySeat(foundAddr):
	os.system('clear')
	print ('''
		============================================
			Number of Available Seats
		============================================
		  ''')
	maxSeats = 40
	numberOfPeople = len(foundAddr)
	x = maxSeats - numberOfPeople
	print("\t\tNumber of Available seats in the Bus : [", x, "]\n\n")

main()
