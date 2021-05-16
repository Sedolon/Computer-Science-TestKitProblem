from Time_Table import WebTimeTableBot


# list of possible subjects for distribution
possible_subjects = ["Ma", "De", "En", "Verf", "Bi", "Ph", "Ch", "Ge", "Ek", "Pw"]

# list of all classes in main building
junior_classes = [
    "5a", "5b", "5c", "5d", "5e", "6a", "6b", "6c", "6d", "6e", "7a", "7b", "7c", "7d", "7e",
    "8a", "8b", "8c", "8d", "8e", "9a", "9b", "9c", "9d", "9e", "10a", "10b", "10c", "10d", "10e",
    "11a", "11b", "11c", "11d"
    ]


classes_done = []


# Simulates the distribution (only as example)
def distribute():
    # Let user choose the date
    date = ""
    try:
        date = str(input("\nType the date in English: "))
    except Exception as e:
        date = "2021-05-12"
        print(e)

    prepare_distribution(date)


# This function gives the teacher a plan when, who and where to deliver to
def prepare_distribution(date):
    # Create bot object
    bot = WebTimeTableBot("chromedriver.exe", date)

    # Get list to work with
    complete_school_matrix = []
    for class_ in junior_classes:
        subjects_rooms_matrix = bot.scraping_(class_, date)
        complete_school_matrix.append([class_, subjects_rooms_matrix])

    # Display the whole scraping work
    print("\nWhole scraping work:")
    for el in complete_school_matrix:
        print(el)

    updated_list = mark_subject_type(complete_school_matrix)

    possible_hours = [3, 4, 5, 6]
    teacher_schedule = []
    for i in possible_hours:
        teacher_schedule.append(get_distro_for_classes(updated_list, i))
    print("The hole teacher schedule")
    for e in teacher_schedule:
        print(e)

    return add_second_preferences_to_schedule(matrix=updated_list, done=classes_done, schedule=teacher_schedule)


# This function declares subjects as Course of FullClass -> becomes easier to read afterwards
def mark_subject_type(matrix):
    # Mark all subjects in matrix which are not possible subjects

    # First: Get how many classes there are in list
    for i in range(len(matrix)):
        inner_list_for_each_class = matrix[i][1]

        # Second: Go to only the subject string of each class
        for l in range(len(inner_list_for_each_class)):
            useless_counter = len(possible_subjects)

            # Third: Go through list of possible subjects and clean list
            for subject in possible_subjects:
                # Change name to: Useless
                if subject != inner_list_for_each_class[l][1]:
                    useless_counter -= 1
                    continue
                else:
                    break

            # Define as useless if no element in list matched
            if inner_list_for_each_class[l][1] == "Useless":
                pass
            elif useless_counter == 0:
                inner_list_for_each_class[l][1] = "Course"
            else:
                inner_list_for_each_class[l][1] = "FullClass"

    # Delete useless list elements
    for i in range(len(matrix)):

        # Useless time
        matrix[i][1] = [ele for ele in matrix[i][1] if ele[2] > 2 and ele[0] != "-"]

    print("\nMarked matrix:")
    for el in matrix:
        print(el)

    return matrix


# This function orders every FullClass into the most suitable hour
def get_distro_for_classes(matrix, hour):
    print("\nDistro: ")
    # First: Get how many classes there are in list
    classes = []
    teacher_schedule = []
    global classes_done

    for i in range(len(matrix)):
        class_ = matrix[i][0]
        schedule = matrix[i][1]

        # Adapt list with same layer
        for ele in schedule:
            # Hour, room, subject, class
            # All classes in this hour
            classes.append([ele[2], ele[0], ele[1], class_])

    # Sort so that the teacher can start with the nearest room
    classes.sort(key=lambda x: x[1])

    # Add to teacher schedule
    class_amount = 0
    for class_ in classes:
        # Cut list length to the optimum
        if class_amount != calc_room_amount_each_hour():
            # Condition for clever distribution
            if class_[0] == hour and class_[2] != "Course" and class_[2] != "Useless":
                # Check if class in list
                if len(classes_done) != 0:
                    counter = len(classes_done)
                    for class_done in classes_done:
                        if class_[3] != class_done:
                            counter -= 1
                        else:
                            break

                    if counter == 0:
                        teacher_schedule.append(class_)
                        classes_done.append(class_[3])
                        class_amount += 1
                else:
                    print("No classes done yet")
                    teacher_schedule.append(class_)
                    classes_done.append(class_[3])
                    class_amount += 1

    # Clear empty list elements if needed
    teacher_schedule = [ele for ele in teacher_schedule if len(ele) != 0]

    print("Schedule:")
    for i in range(len(teacher_schedule)):
        print(teacher_schedule[i])

    return teacher_schedule


# This function picks the smallest hour_list and fills it with Courses
# It will become larger than other hour_lists, however most Courses contains of multiple classes and are delivered
# at the same time
def add_second_preferences_to_schedule(matrix, done, schedule):
    possible_hours = [3, 4, 5, 6]

    filtered = filter(lambda x: x[0] not in done, matrix)
    # Get smallest list element from schedule
    min_pos = len(schedule[0])
    min_index = 0
    for i in schedule:
        if min_pos >= len(i):
            min_index = schedule.index(i)
    best_hour = possible_hours[min_index]

    print("\nThe best hour: " + str(best_hour))

    classes_in_hour = []
    # Get the classes from list
    for i in filtered:
        for m in i[1]:
            if m[2] == best_hour:
                classes_in_hour.append([m[2],m[0], m[1], i[0]])

    classes_in_hour.sort(key=lambda x: x[1])

    print("\nFor the  following classes it is not possible deliver their tests today")
    not_in_school = [ele[3] for ele in classes_in_hour if ele[1] == 0]
    for i in not_in_school:
        print(i)

    # Remove them from list
    classes_in_hour = [ele for ele in classes_in_hour if ele[1] != 0]

    print("\nClasses in hour:")
    for ele in classes_in_hour:
        print(ele)

    # Add classes to schedule
    for class_ in classes_in_hour:
        schedule[min_index].append(class_)

    # Display the final result
    print("\n\nFinal Result main building: ")
    for schedule_ele in schedule:
        print(schedule_ele)
    print("\nClasses for the next day: ")
    for not_in_school_ele in not_in_school:
        print(not_in_school_ele)


# This function returns the cleverest amount of classes in one hour (only for FullClass subjects)
def calc_room_amount_each_hour():
    amount = (len(junior_classes) / 4) + 1
    return int(amount)




