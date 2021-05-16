from Check_Test_Amount import check

# elements of kit which are delivered in huge box and have to be sorted
SWABS = 2000
CARDS = 1000
ANTIGENS = 2000

# Update the new value of the elements -> add the rest
swabs = SWABS
cards = CARDS
antigens = ANTIGENS


def sort():
    global swabs, cards, antigens

    # List of sorted tests
    test_kits = []

    # Get min value so that all elements are equal
    min_amount = min(swabs, cards, antigens)

    # Fill sorted lists with objects of test kits and print the rest amount
    for i in range(min_amount):
        test_kits.append(TestKit())
        print(
            "Swabs: " + str(swabs) +
            " Cards: " + str(cards) +
            " Antigens: " + str(antigens)
        )
    print("\nCheck if you have to distribute:")
    check(len(test_kits))


# Class which represents tests kits
class TestKit:
    def __init__(self):

        global swabs, cards, antigens
        # Add element to kit object
        self.swab = 1
        self.card = 1
        self.antigen = 1

        # Change values each time a new kit has been sorted
        swabs -= self.swab
        cards -= self.card
        antigens -= self.antigen



