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

def main():
    if len(sys.argv) != 2:
        return(1)

    state = sys.argv[1]
    states_acronyms = states_and_acronyms()
    acronyms_capitals = acronyms_and_capitals()

    acronym = states_acronyms.get(state)
    if acronym is None:
        print("Unknown state")
        return(2)

    capital = acronyms_capitals.get(acronym)
    if capital is None:
        print("Capital not found")
        return(3)

    print(capital)

if __name__ == "__main__":
    main()