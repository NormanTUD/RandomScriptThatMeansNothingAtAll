from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
import pathlib
import argparse
from time import sleep
import time
from pprint import pprint
import _thread
from pprint import pprint
import os.path
import subprocess
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument("--headless")

parser = argparse.ArgumentParser(description='Random script that has nothing to do with anything at all, especially not fixing annoying stuff.')

parser.add_argument('--username', type=str, help='Username')
parser.add_argument('--password', type=str, help='Password')
parser.add_argument('--home_network_name', type=str, help='Name of the home network (wlan)')
parser.add_argument('--abteilung', type=str, help='VDR')
parser.add_argument('--start_url', type=str, help='Any url to start from')

args = parser.parse_args()

timeout = 60  # seconds
short_timeout = 40  # seconds
kill_threads = False

username = args.username
password = args.password
home_network_name = args.home_network_name

random_data = ["IAK", "IMC", "NK", "OPS", "SD", "SDE", "VDR", "Verwaltung"]
random_index = random_data.index(args.abteilung)

def is_at_home ():
    command = "nmcli -t -f active,ssid dev wifi | egrep '(yes|ja):" + home_network_name + "' | wc -l"
    result = subprocess.check_output(command, shell=True).decode('ascii')

    print(result)

    if result == "1\n":
        return True
    else:
        return False

home_office = is_at_home()

basepath = pathlib.Path(__file__).parent.absolute()
path = None

if os.name == 'nt':
    path = str(basepath) + "/chromedriver.exe"
    if not os.path.isfile(path) :
        wd = sys._MEIPASS
        path = os.path.join(wd, "chromedriver.exe")
elif os.name == "posix":
    path = str(basepath) + "/chromedriver"
else:
    print("Unknown operating system " + os.name)
    sys.exit(1)

driver = webdriver.Chrome(path, options=chrome_options)
driver.get(args.start_url)

def countdown (t):
    global kill_threads
    while t:
        if kill_threads:
            kill_threads = False
            _thread.exit()
        mins, secs = divmod(t, 60)
        timeformat = 'This operation may take time. ETA: {:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

def check_exists_by_id(item_id):
    html = driver.page_source
    if item_id in html:
        return True
    return False

def get_element(locator):
    global kill_threads
    countdown_thread = _thread.start_new_thread(countdown,(timeout,))
    item = WebDriverWait(driver, short_timeout).until(expected_conditions.presence_of_element_located(locator))
    kill_threads = True
    return item

def main():
    # LOGIN
    username_input = get_element((By.ID, "username"))
    password_input = get_element((By.ID, "password"))

    username_input.send_keys(username)
    sleep(2)
    password_input.send_keys(password + "\n")

    # Click "new item"
    sleep(2)
    driver.find_elements_by_xpath("//*[contains(text(), 'new item')]")[0].click()

    # Find person field, enter id, press enter
    sleep(2)
    webElement = driver.find_element_by_id("Person_d3564cbf-5aaf-40f1-9e4b-e439df113db0_$ClientPeoplePicker_EditorInput");
    webElement.send_keys(username)

    actions = ActionChains(driver)

    # Choose Name
    actions = actions.send_keys(Keys.TAB)
    actions = actions.pause(1)

    # Select name
    actions = actions.send_keys(Keys.ENTER)

    # Accept current date
    for _ in range(4):
        actions = actions.send_keys(Keys.TAB)

    # Go to "Status" (HO or Office)
    actions = actions.send_keys(Keys.TAB)

    if home_office:
        # Select Home Office
        print("Using home office")
        actions = actions.send_keys(Keys.ARROW_DOWN)
        actions = actions.send_keys(Keys.ARROW_DOWN)
    else:
        # Select "Auf Arbeit"
        actions = actions.send_keys(" ")

    # Bemerkung
    actions = actions.send_keys(Keys.TAB)

    # Abteilung
    actions = actions.send_keys(Keys.TAB)
    
    global random_index
    for i in (range(0, random_index)):
        actions = actions.send_keys(Keys.ARROW_DOWN)

    actions = actions.send_keys(" ")

    # Go to save
    actions = actions.send_keys(Keys.TAB)

    actions = actions.send_keys(Keys.ENTER)
    actions = actions.pause(1)

    actions.perform()

    sleep(10)

    driver.close()
    driver.quit()

if __name__ == '__main__':
    main()
