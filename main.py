import questionary

# Define all options with info and action functions
OPTIONS = {
    "Connect a Controller (This registers the controller so you don't have to start from the Change Grip Menu)": {
        "info": "In Order to connect a Switch go to Change Grip Menu. Pre connecting a Controller may not work on the Switch 2. After Execution the controller will be disconnected but registered",
        "action": lambda: print("Connecting Controller..")
    },
    "Pokemon Legends Z-A Bench Reset": {
        "info": "If no Controller has been connected yet please go to Change Grip Menu on the Switch. In order to Bench Reset properly stand in front of a bench with the camera facing away from the bench.",
        "action": lambda: print("Bench resetting..")
    },
    "Pokemon Legends Z-A Farm Restaurant Battles": {
        "info": "If no Controller has been connected yet please go to Change Grip Menu on the Switch. In order to Bench Reset properly stand in front of the Restaurant NPC with a Pokemon that has its important move on A",
        "action": lambda: print("Farming Restaurant Battles..")
    },
    "Record Nintendo Switch Macros or play them": {
        "info": "If no Controller has been connected yet please go to Change Grip Menu on the Switch. In order to record and play Macros properly please follow further prompts",
        "action": lambda: print("Going to recording of Macros")
    },
    "Exit": {
        "info": "Exit the program.",
        "action": lambda: print("Goodbye!")
    }
}

def show_info(option: str):
    """Display information about the selected option."""
    print("\n" + OPTIONS[option]["info"] + "\n")

def execute_option(option: str):
    """Execute the action associated with the selected option."""
    OPTIONS[option]["action"]()

def main():
    while True:
        # Display menu
        choice = questionary.select(
            "Please choose an option:",
            choices=list(OPTIONS.keys())
        ).ask()

        if not choice or choice == "Exit":
            execute_option("Exit")
            break

        # Show info about the choice
        show_info(choice)

        # Confirm execution
        confirm = questionary.confirm("Do you want to start execution?").ask()
        if confirm:
            execute_option(choice)
        else:
            print("Execution canceled.\n")

if __name__ == "__main__":
    main()
