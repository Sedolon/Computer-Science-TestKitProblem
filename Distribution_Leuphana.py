# This method is used for distribute every Kit in the
def distribute_leuphana():
    rooms = ["301", "302", "310", "307", "202", "09"]
    # Sort rooms cleverly
    rooms.sort()

    print("\nThe pseudo Leuphana distribution:")
    # Give student and tick him on the list of every student
    for room in rooms:
        print(f"Room {room} has been visited.")
