from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import datetime


class WebTimeTableBot:
    def __init__(self, driver_path, date):
        self.browser = webdriver.Chrome(driver_path)
        # open url
        self.browser.get(
            "https://neilo.webuntis.com/WebUntis/index.do?school=Wilhelm-Raabe-Schule%20Lueneburg#/basic/timetable")

        # choose correct week
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        german_date = date_obj.strftime('%d.%m.%Y')

        date_field = self.browser.find_element_by_xpath("//input[@class='un-datetime-picker__input form-control']")
        date_field.click()
        date_field.send_keys(german_date)
        date_field.send_keys(Keys.ENTER)

    def scraping_(self, class_, date):

        # choose correct class
        class_x_path = f"//a[normalize-space()='{class_}']"
        class_button = self.browser.find_element_by_xpath(class_x_path)
        class_button.click()
        WebDriverWait(self.browser, 30).until(
            ec.presence_of_element_located((By.CLASS_NAME, "grupetScrollContainerContent")))

        # Wait for site to be loaded
        time.sleep(2)

        # get subjects and rooms for monday
        return get_monday_subjects_and_rooms(self, date)


def get_monday_subjects_and_rooms(self, date):
    day_links = get_unsorted_subject_links(self, date)
    sorted_day_links_with_order = sort_subject_order(day_links)

    # Get subject and room from link object
    day_subjects_and_rooms = []

    for i in range(len(sorted_day_links_with_order)):

        # Sort out free lessons
        col_subject_web_element = sorted_day_links_with_order[i][1].find_element_by_xpath(
            "./div/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]")
        room_web_element = sorted_day_links_with_order[i][1].find_element_by_xpath(
            "./div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/span")

        if "text-decoration: line-through;" not in col_subject_web_element.get_attribute("style"):
            subject = col_subject_web_element.find_element_by_xpath("./span").text
            room = room_web_element.text

            char_to_replace = {'R': '', 'e': ''}

            # Replace key character with value character in string
            room = room.translate(str.maketrans(char_to_replace))
            room = room.replace("Aula", "115")

            # Define Homeschooling and sports hall as useless
            if room[0] == "H" or room[0] == "U":
                subject = "Useless"
                room = 0

        else:
            subject = "-"
            room = 0

        day_subjects_and_rooms.append([int(room), subject, sorted_day_links_with_order[i][0]])

    # Display ordered matrix of rooms and subjects
    print("Ordered matrix of rooms and subjects: ")
    for subject in day_subjects_and_rooms:
        print(subject)

    return day_subjects_and_rooms


def sort_subject_order(day_links):
    # Array which should be look like
    # list = [
    #   [order_on_day, WebElement]
    # ]
    sorted_day_links_with_order = []

    # Get right order
    print("\nUnsorted matrix: ")
    for i in range(len(day_links)):
        order_on_day = int(day_links[i].get_attribute("href")[138: 138 + 2])
        sorted_day_links_with_order.append([order_on_day-7, day_links[i]])
        print(sorted_day_links_with_order[i])

    # The actual sorting method
    sorted_day_links_with_order.sort(key=lambda x: x[0])

    # display sorted matrix
    print("\nThe sorted matrix: ")
    for item in sorted_day_links_with_order:
        print(item)
    print()

    return sorted_day_links_with_order


def get_unsorted_subject_links(self, date):
    # Gets every field lesson of the whole week (unsorted)
    week_links = self.browser.find_elements_by_xpath("//div[@class='entryLayer']/a")

    # sort unimportant lessons out -> only lessons of current date
    day_links = []
    print("\nEach subject link:")
    for link in week_links:
        if date in link.get_attribute("href"):
            day_links.append(link)
            print(link.get_attribute("href"))

    return day_links



