import nxbt
import time
from random import randint

import nxbt
from nxbt import Buttons
from nxbt import Sticks
aMacro = """
A 0.05s
"""
shoulderMacro = """
ZL 1s
"""
print("start nxbt")
# Start the NXBT service

def random_colour():

    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]



nx = nxbt.Nxbt()
print("creating controller")
# Get a list of all available Bluetooth adapters
adapters = nx.get_available_adapters()
# Prepare a list to store the indexes of the
# created controllers.
controller_idxs = []
# Loop over all Bluetooth adapters and create
# Switch Pro Controllers

for i in range(0, len(adapters)):
    if nx.get_switch_addresses != []:
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
print("connected")
last_time = time.time() - 5
zlFreq = 1.1
aFreq = 0.1
# Run a macro on the Pro Controller
while True:
	print("pressing A")
	time.sleep(0.05)
	nx.macro(controller_idx, aMacro, block = False)
	if (time.time() - last_time) > zlFreq:
		print(time.time() - last_time)
		last_time = time.time()
		print("pressing ZL")
		nx.macro(controller_idx, shoulderMacro, block= False)
