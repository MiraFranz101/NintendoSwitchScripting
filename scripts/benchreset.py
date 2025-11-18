import nxbt
import time
from random import randint

import nxbt
from nxbt import Buttons
from nxbt import Sticks
macro = """
A 0.1s
"""
print("start nxbt")
# Start the NXBT service
print("reconnect ? y/n")
reconnect = input() == "y"
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
print("Adapters: ", adapters)
# Prepare a list to store the indexes of the
# created controllers.
controller_idxs = []
# Loop over all Bluetooth adapters and create
# Switch Pro Controllers
print("Switch Addresses: ", nx.get_switch_addresses())
for i in range(0, len(adapters)):
    if nx.get_switch_addresses() != [] or reconnect:
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
print("connecting...")
nx.wait_for_connection(controller_idx)
print("connected.")
tiltDownAfter=6
lastTiltDown = time.time()
if (not reconnect):
	print("pressing home twice")
	nx.macro(controller_idx, "HOME 0.1s \n 1s \n HOME 0.1s")
# Run a macro on the Pro Controller
while True:
	print("running macro")
	nx.macro(controller_idx, macro)
	# Tilt the right stick fully to the left.
        # tilt_stick defaults to tilting the stick for 0.1s and releasing for 0.1s
	if(time.time() - lastTiltDown > tiltDownAfter):
		lastTiltDown = time.time()
		nx.tilt_stick(controller_idx, Sticks.LEFT_STICK, 0, -100)

