from selenium import webdriver
from .models import Driver
import time
from selenium.webdriver.common.by import By


def get_driver(driver_name):
    dr = None
    driver = Driver.objects.filter(name=driver_name).first()
    if driver.name == "Chrome":
        dr = webdriver.Chrome(executable_path=driver.path)

    if driver.name == "Mozila":
        dr = webdriver.Firefox(executable_path=b'driver.path')
        
    return dr


class SetUpMain:

    def __init__(self):
        self.dr = None
        self.find = None
        self.element = None

    def main(self, **PARAMS):

        for key in PARAMS:
            print(key)
            if key == "open_browser":
                self.dr = get_driver(PARAMS[key])
                
            if key == "path":
                self.dr.get(PARAMS[key])
                continue

            if key == "find_element":
                self.element = self.dr.find_element(By.XPATH, PARAMS[key])
                continue

            if key == "send_keys":
                for k, v in PARAMS[key].items():
                    self.element.send_keys(v)
                    # time.sleep(3)
                continue

            if key == "click":
                self.element.click()
                continue

            if key == "time_sleep":
                time.sleep(PARAMS[key])
                continue

            if key == "close":
                self.dr.close()
                break


