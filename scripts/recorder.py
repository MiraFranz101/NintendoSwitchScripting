import nxbt
from enum import Enum
import time
from random import randint
import pickle
import nxbt
from nxbt import Buttons
from nxbt import Sticks
import keyboard
def random_colour():

    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]
ticksPerSecond =4
print("start nxbt")
# Start the NXBT service
print("reconnect ? y/n")

reconnect = input() == "y"
nx = nxbt.Nxbt()
print("creating controller")
# Get a list of all available Bluetooth adapters
adapters = nx.get_available_adapters()
# Prepare a list to store the indexes of the
# created controllers.
controller_idxs = []
for i in range(0, len(adapters)):
    if nx.get_switch_addresses != [] and reconnect:
        index = nx.create_controller(nxbt.PRO_CONTROLLER,
        	adapter_path=adapters[i],
        	colour_body=random_colour(),
		reconnect_address=nx.get_switch_addresses(),
        	colour_buttons=random_colour())
    else:
        index = nx.create_controller(
                nxbt.PRO_CONTROLLER,
                adapter_path=adapters[i],
                colour_body=random_colour(),
                colour_buttons=random_colour())
    controller_idxs.append(index)

    # Select the last controller for input
    controller_idx = controller_idxs[-1]

print(controller_idx)
print("connecting...", nx.get_switch_addresses())
nx.wait_for_connection(controller_idx)
print("connected.")
class Action(Enum):
	MOVE_UP = "w"
	MOVE_DOWN = "s"
	MOVE_LEFT = "a"
	MOVE_RIGHT = "d"
	B = "h"
	A ="u"
	Y = "z"
	X = "7"
	HOME = "b"
	PLUS = "v"
	LOOK_UP = "up"
	LOOK_DOWN = "down"
	LOOK_LEFT = "left"
	LOOK_RIGHT = "right"
	R = "4"
	ZR = "5"
	L = "2"
	ZL = "1"
	DPAD_UP = "i"
	DPAD_DOWN = "k"
	DPAD_RIGHT = "l"
	DPAD_LEFT = "j"

def getPressButtonFunc(nxbtVar, controller_idx, Button, timePressed = 0.2):
	def pressButton():
		print("pressing", [Button])
		nxbtVar.press_buttons(controller_idx, [Button], timePressed, block= False)
	return pressButton
def getTiltStickFunc(nxbtVar, controller_idx, timePressed = 0.2):
	def tiltStick(stick, xTilt, yTilt):
		nxbtVar.tilt_stick(controller_idx, stick, xTilt, yTilt, block = False)
	return tiltStick

tiltStick = getTiltStickFunc(nx, controller_idx)
buttons = {attr: getattr(nxbt.Buttons, attr) for attr in dir(nxbt.Buttons) if not attr.startswith("__")}
nxbtActions = {
	Action.MOVE_UP: lambda : tiltStick(Sticks.LEFT_STICK, 0, 100),
	Action.MOVE_DOWN: lambda : tiltStick(Sticks.LEFT_STICK, 0, -100),
	Action.MOVE_LEFT: lambda : tiltStick(Sticks.LEFT_STICK, -100, 0),
	Action.MOVE_RIGHT: lambda : tiltStick(Sticks.LEFT_STICK, 100, 0),
	Action.LOOK_UP: lambda : tiltStick(Sticks.RIGHT_STICK, 0, 100),
	Action.LOOK_DOWN: lambda :tiltStick(Sticks.RIGHT_STICK, 0, -100),
	Action.LOOK_LEFT: lambda :tiltStick(Sticks.RIGHT_STICK, -100, 0),
	Action.LOOK_RIGHT: lambda : tiltStick(Sticks.RIGHT_STICK, 100, 0),
}
for action in Action:
	if action not in nxbtActions:
		print("adding", action.name, "button in nxbt:", buttons[action.name])
		nxbtActions[action] = getPressButtonFunc(nx, controller_idx, buttons[action.name])
print(nxbtActions)
# Loop over all Bluetooth adapters and create
# Switch Pro Controllers


file = input("press Enter to start recording or the file to load macro from\n")
macro = ""
if(file):
	with open(file+".macro", 'rb') as file:
    		macro = pickle.load(file)

def on_press(starttime, actionDict, record):
	def checkKeys():
		current_time = time.time() - starttime
		for a in Action:
			if keyboard.is_pressed(a.value):
				print(a)
				if(record):
					actionDict[current_time] = a
				nxbtActions[a]()
	return checkKeys
def record(starttime):
	actionDict = {}
	input("Input keys to control switch, press Esc to save macro")
	lastExec = time.time()-1
	while True:
		if (time.time() - lastExec) > 1/ticks:
			on_press(starttime, actionDict, True)()
			if keyboard.is_pressed("esc"):
				break
	input("press Enter to continue")
	saveAs = input("Which name should this file be saved under?")
	with open(saveAs+".macro", 'wb') as outp:
		pickle.dump(actionDict, outp, pickle.HIGHEST_PROTOCOL)
def pressKey(starttime, actionDict):
	filteredEntries = [(t, v) for t, v in actionDict.items() if t <time.time()+2 - starttime ]
	futureEntries = [(t, v) for t, v in actionDict.items() if t > time.time() - starttime ]
	if(futureEntries == []):
		return False

	for timestamp, key in filteredEntries:
		nxbtActions[key]()
		actionDict.pop(timestamp, key)
	return True
if(not macro):
	record(time.time())
if (not reconnect):
	print("pressing home twice")
	nx.macro(controller_idx, "HOME 0.1s \n 1s \n HOME 0.1s")
# Run a macro on the Pro Controller

if(macro):
	starttime = time.time()
	macroCopy = macro.copy()
	while True:
		if(not pressKey(starttime, macro)):
			macro = macroCopy.copy()
			starttime = time.time()
		if(keyboard.is_pressed("esc")):
			break
