import nxbt
import time
from random import randint

import nxbt
from nxbt import Buttons
from nxbt import Sticks


class Benchreset:
    macro = """
    A 0.1s
    """
    tiltDownAfter = 6

    def random_colour(self):

        return [
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
        ]

    nx = nxbt.Nxbt()

    def run(self):

        print("start nxbt")
        # Start the NXBT service
        print("reconnect ? y/n")
        reconnect = input() == "y"

        print("creating controller")
        # Get a list of all available Bluetooth adapters
        adapters = self.nx.get_available_adapters()
        print("Adapters: ", adapters)
        # Prepare a list to store the indexes of the
        # created controllers.
        controller_idxs = []
        # Loop over all Bluetooth adapters and create
        # Switch Pro Controllers
        print("Switch Addresses: ", self.nx.get_switch_addresses())
        for i in range(0, len(adapters)):
            if self.nx.get_switch_addresses() != [] or reconnect:
                index = self.nx.create_controller(nxbt.PRO_CONTROLLER,
                                                  adapter_path=adapters[i],
                                                  colour_body=self.random_colour(),
                                                  reconnect_address=self.nx.get_switch_addresses(),
                                                  colour_buttons=self.random_colour())
            else:
                index = self.nx.create_controller(
                    nxbt.PRO_CONTROLLER,
                    adapter_path=adapters[i],
                    colour_body=self.random_colour(),
                    colour_buttons=self.random_colour())
            controller_idxs.append(index)

            # Select the last controller for input
            controller_idx = controller_idxs[-1]

        print(controller_idx)
        print("connecting...")
        self.nx.wait_for_connection(controller_idx)
        print("connected.")
        lastTiltDown = time.time()
        if (not reconnect):
            print("pressing home twice")
            self.nx.macro(controller_idx, "HOME 0.1s \n 1s \n HOME 0.1s")
        # Run a macro on the Pro Controller
        while True:
            print("running macro")
            self.nx.macro(controller_idx, self.macro)
            # Tilt the right stick fully to the left.
            # tilt_stick defaults to tilting the stick for 0.1s and releasing for 0.1s
            if (time.time() - lastTiltDown > self.tiltDownAfter):
                lastTiltDown = time.time()
                self.nx.tilt_stick(controller_idx, Sticks.LEFT_STICK, 0, -100)
