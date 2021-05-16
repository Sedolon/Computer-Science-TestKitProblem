

# The defined students of each category and the total amount
JUNIOR_STUDENTS = 800
SENIOR_STUDENTS = 200

TOTAL_STUDENT_AMOUNT = JUNIOR_STUDENTS + SENIOR_STUDENTS


# check if and how many tests the teacher must distribute
def check(test_amount):
    if test_amount >= TOTAL_STUDENT_AMOUNT:
        print("Everyone gets tests")

        # Get giving rate (only integer)
        rate = test_amount // TOTAL_STUDENT_AMOUNT

    else:
        # Due to fairness nobody gets a test kit and the teachers have to wait
        print("Wait for the next day and start program again")
