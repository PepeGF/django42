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
        return (1)

    capital = sys.argv[1]
    states_acronyms = states_and_acronyms()
    acronyms_capitals = acronyms_and_capitals()

    if capital not in acronyms_capitals.values():
        print("Unknown capital city")
        return (2)

    # Find the state corresponding to the capital
    for state, acronym in states_acronyms.items():
        if acronyms_capitals.get(acronym) == capital:
            print(state)
            return (0)

    print("Unknown capital city")
    return (2)

if __name__ == "__main__":
    main()