from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, random, os
import requests, json
import subprocess
from importlib import import_module

print ("[INFO] LunaBot Init.")

chrome_options = Options()

# Remember to turn this option on after you've scanned the QR Code, for extra performance
# chrome_options.add_argument("--headless")

ok = False
while (ok == False):
	try:
		driver2 = webdriver.Chrome(chrome_options=chrome_options)
		driver2.get("https://www.cleverbot.com")

		print ("[INFO] Cleverbot Engine Has Been Loaded.")

		chrome_options.add_argument("--user-data-dir={0}".format(os.path.expanduser("~/LunaBot/Data")))

		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.get("https://web.whatsapp.com/")

		print ("[INFO] WhatsappWeb Has Been Loaded.")
		ok = True
	except Exception as e:
		print (e)
		print ("[ERR] Something went wrong, retrying in 5 seconds...")
		time.sleep(5)

### Utils
def docCSSSelect (path):
	return driver.execute_script("return document.querySelector(\"" + path + "\")")
	
def CSSSelect (obj, path):
	return driver.execute_script("return arguments[0].querySelector(\"" + path + "\")", obj)

def docCSSSelectMulti (path):
	return driver.execute_script("return document.querySelectorAll(\"" + path + "\")")
	
def CSSSelectMulti (obj, path):
	return driver.execute_script("return arguments[0].querySelectorAll(\"" + path + "\")", obj)

def docClassSelectMulti (path):
	return driver.execute_script("return document.getElementsByClassName(\"" + path + "\")")
	
def ClassSelectMulti (obj, path):
	return driver.execute_script("return arguments[0].getElementsByClassName(\"" + path + "\")", obj)
 
def docClassSelect (path):
	return docClassSelectMulti(path)[0] #Hack

def ClassSelect (obj, path):
	return ClassSelectMulti(obj, path)[0] #Hack

def GetCleverMessage (text):
	driver2.execute_script("cleverbot.sendAI(arguments[0])", text)
	while (driver2.execute_script('return cleverbot.aistate') != 0):
		pass
				
	return driver2.execute_script('return cleverbot.reply')
	
### Global Objects
msgside = None

defmsg = """\U0001F314\U0001F499 LunaBot *(v1.2)*

"""

helpmsg = """Python port of the *LunaBot Project*

Commands:
	*- !luna help:* Displays this message
	*- !luna ping:* Check online status
	*- !luna 4chan _board_:* Start browsing 4chan
	*- !luna say _something_:* Make Luna say silly words
	*- !luna sendmail _from@address_ _to@address_ _message_:* Send an e-mail
	*- !luna weather _city_:* Get weather info for current city
	*- !luna fortune:* Come get your fortune!
	*- !luna listmodules:* List installed modules.
	*- !luna loadmodule _modulename_:* Load a module. You can then access it with $message.
	*- !...:* Talk with Luna
	
If you mistype a command your message will be automatically piped to the *chatter* engine
"""
### Modules
mod = {}
mod_session = {}

### Jingles
fortune_common = ["Good Luck", "Average Luck", "Bad Luck", "Outlook good"]
fortune_rare = ["Excellent Luck", "Good news will come to you by mail", "( ´_?`)??? ", "Better not tell you now", "You will meet a dark handsome stranger", "ayy lmao"]
fortune_epic = ["Very Bad Luck", "le ebin dubs xDDDDDDDDDDDD", "you gon' get some dicc", "Get Shrekt", "NOT SO SENPAI BAKA~KUN"]
fortune_legendary = ["(YOU ARE BANNED)", "YOU JUST LOST THE GAME", "GODLY LUCK"]

### Jingles Data
lastfortune = 0

### INIT FUNC
def Init ():
	init = False
	global msgside
	while (init == False):
		try:
			msgside = driver.find_element_by_id("side")
			if (msgside != None):
				init = True
		except Exception as e:
			print (e)
		time.sleep(1)
	
### SND MESSAGE PROCEDURE
def SendMsg (text):
	txtbox = docClassSelect("_2S1VP")
	driver.execute_script("var elem = arguments[0]; elem.innerHTML = arguments[1]; arguments[0].dispatchEvent(new InputEvent('input', {bubbles: true, composer: true}))", txtbox, text)
	txtbox.send_keys(Keys.RETURN)

### MSG ANALYSIS LOOP
def CheckChat (clk):
	global fortune_common
	global fortune_rare
	global fortune_epic
	global fortune_legendary
	
	global lastfortune
	
	clk.click()
	chatname = docCSSSelect("._3XrHh > span").get_attribute("innerText")
	inmsgs = docClassSelectMulti("vW7d1")
	inmsg = ClassSelect(inmsgs[len(inmsgs) - 1], "selectable-text").get_attribute("innerText")
	
	if (inmsg == ""):
		return
		
	printer = defmsg
	if (inmsg[0] == "!"):
		print ("[INFO] Engaging On Chat: " + chatname)
		print ("[INFO] MSG: " + inmsg)
		
		inmsg = inmsg[1:]
		
		if (inmsg[:4].lower() == "luna"):
			inmsg = inmsg[5:]
			if (inmsg[:4].lower() == "help"):
				printer += helpmsg
			elif (inmsg[:4].lower() == "ping"):
				printer += "*PONG!*"
			elif (inmsg[:3].lower() == "say"):
				inmsg = inmsg[4:]
				if (inmsg == ""):
					printer += "Tell me something to say, too!"
				else:
					printer = inmsg
			elif (inmsg[:7].lower() == "weather"):
				inmsg = inmsg[8:]
				r = requests.get("http://api.apixu.com/v1/current.json?key=PUT_YOUR_KEY_HERE&q=" + inmsg)
				data = json.loads(r.text)
				printer += "*{0} ({1}):*\n\n".format(data["location"]["name"], data["location"]["country"])
				printer += "Local Time: *{0}*\n".format(data["location"]["localtime"])
				printer += "Condition: *{0}*\n".format(data["current"]["condition"]["text"])
				printer += "Temperature: *{0} °C* (Feels Like *{1} °C*)\n".format(data["current"]["temp_c"], data["current"]["feelslike_c"])
				printer += "Wind Speed: *{0} km/h*\n".format(data["current"]["wind_kph"])
				printer += "Pressure: *{0} mbars*\n".format(data["current"]["pressure_mb"])
				printer += "Humidity: *{0}%*\n".format(data["current"]["humidity"])
			elif (inmsg[:7].lower() == "fortune"):
				printer += "Your Fortune: "
				if (lastfortune + 20 < time.time()):
					lastfortune = time.time()
					chance = random.randint(0, 100)
					if (chance <= 50):
						printer += random.choice (fortune_common)
					elif (chance <= 75):
						printer += "_" + random.choice (fortune_rare) + "_"
					elif (chance <= 95):
						printer += "```" + random.choice (fortune_epic) + "```"
					else:
						printer += "*_" + random.choice (fortune_legendary) + "_*"
				else:
					printer += "Reply hazy, try again"
			elif (inmsg[:8].lower() == "sendmail"):
				inmsg = inmsg[9:]
				
				frm = inmsg.split()[0]
				to = inmsg.split()[1]
				ok = False
				
				if (frm != "" and to != "" and frm.find("@") != -1 and to.find("@") != -1):
					msg = inmsg[inmsg.find(to) + len(to) + 1:]
					
					if (msg != ""):
						# Put the SMTP script at this path
						subprocess.call(["expect", "~/LunaBot/smtper", frm, to, msg])
						printer += "Mail Sent!\nFrom: *{0}*\nTo: *{1}*\nMessage:\n{2}".format(frm, to, msg)
						ok = True
						
				if (ok == False):
					printer += "Usage: *!luna sendmail _from@address_ _to@address_ _message_:*"
			elif (inmsg[:10].lower() == "loadmodule"):
				inmsg = inmsg[11:].lower()
				
				ok = True
				for c in inmsg:
					if (c < 'a' or c > 'z'):
						if (c < '0' or c > '9'):
							printer += "Sorry, only alphanumeric module names are allowed."
							ok = False
							break
							
				if (ok == True):
					try:
						mod[inmsg] = None
						mod[inmsg] = import_module("modules." + inmsg + ".wrapper")
						mod_session[chatname] = (mod[inmsg].init(), inmsg) # Module Object + Module Name
						printer += "Module *" + inmsg + "* has been loaded. It says:\n"
						printer += mod[inmsg].getoutput(mod_session[chatname][0])
					except Exception as e:
						print (e)
						printer += "Module *" + inmsg + "* is not installed."
			elif (inmsg[:11].lower() == "listmodules"):
				mods = os.listdir("modules")
				printer += "Installed Modules:\n"
				for modfolder in mods:
					printer += "- *" + modfolder + "*\n"
			else:
				printer = GetCleverMessage(inmsg)
		else:
			printer = GetCleverMessage(inmsg)
			
		SendMsg (printer)
	elif (inmsg[0] == "$"): #Modules
		print ("[INFO] Engaging On Chat: " + chatname)
		print ("[INFO] MSG: " + inmsg)
		
		inmsg = inmsg[1:]
		
		if (chatname not in mod_session):
			printer += "Your group has no modules loaded!\nYou can load one using the following command:\n\n"
			printer += "*!luna loadmodule _modulename_*"
		else:
			modulename = mod_session[chatname][1]
			mod[modulename].query(mod_session[chatname][0], inmsg)
			printer = mod[modulename].getoutput(mod_session[chatname][0])
		
		SendMsg (printer)
		
### MSG CHECKER LOOP
def MsgChecker ():
	children = ClassSelectMulti (msgside, "_2wP_Y")
	i = 0
	
	for child in children:
		i += 1
		actchildren = ClassSelectMulti(child, "_15G96")
		
		if (actchildren == None):
			continue
			
		act = None
				
		if (len(actchildren) == 2):
			act = CSSSelect(actchildren[1],"span")
		elif (len(actchildren) == 1):
			intxt = actchildren[0].get_attribute("innerText")
			if (intxt != "" and intxt != "READ"):
				act = CSSSelect(actchildren[0], "span")
				
		if (act != None):
			driver.execute_script("var bubble = arguments[0]; bubble.innerText = \"READ\";", act)
			CheckChat(child)
			
print ("[WARN] Errors might appear. This is normal Init behaviour.")
Init()
print ("[INFO] Init Successful.")
print ("[INFO] LunaBot is now Active and Listening.")

while True:
	try:
		MsgChecker()
	except Exception as e:
		print (e)