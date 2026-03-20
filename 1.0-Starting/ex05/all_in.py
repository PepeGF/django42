import sys

def states_and_acronyms():
    return {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }

def acronyms_and_capitals():
    return {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

def split_arguments():
    if len(sys.argv) != 2:
        sys.exit(1)
    arguments = sys.argv[1].split(",")
    arguments = [arg.strip().title() for arg in arguments]
    arguments = [arg for arg in arguments if arg]
    return arguments

def raw_arguments():
    raw_arguments = sys.argv[1].split(",")
    raw_arguments = [arg.strip() for arg in raw_arguments]
    raw_arguments = [arg for arg in raw_arguments if arg]
    return raw_arguments

def is_state(input):
    states = states_and_acronyms().keys()
    return input in states

def is_capital(input):
    capitals = acronyms_and_capitals().values()
    return input in capitals

def main():
    arguments = split_arguments()
    arguments_raw = raw_arguments()
    states_acronyms = states_and_acronyms()
    acronyms_capitals = acronyms_and_capitals()

    for i, arg in enumerate(arguments):
        if not is_state(arg) and not is_capital(arg):
            print(f"{arguments_raw[i]} is neither a capital city nor a state")
            continue
        capital = arg
        if is_capital(arg):
            for state, acronym in states_acronyms.items():
                if acronyms_capitals.get(acronym) == capital:
                    print(f"{capital} is the capital of {state}")
            continue
        if is_state(arg):
            acronym = states_acronyms.get(arg)
            if acronym is not None:
                capital = acronyms_capitals.get(acronym)
                print(f"{capital} is the capital of {arg}")
            continue

if __name__ == "__main__":
    main()