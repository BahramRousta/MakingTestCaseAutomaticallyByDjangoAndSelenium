from selenium import webdriver
from .models import Driver
import time
from selenium.webdriver.common.by import By


def get_driver(driver_name):
    web_driver = None
    driver = Driver.objects.filter(name=driver_name).first()
    if driver.name == "Chrome":
        web_driver = webdriver.Chrome(executable_path=driver.path)

    if driver.name == "Mozila":
        web_driver = webdriver.Firefox(executable_path=b'driver.path')
        
    return web_driver


class SetUpMain:

    def __init__(self):
        self.element = None
        self.web_driver = None

    def main(self, **PARAMS):

        for key in PARAMS:

            if key == "web_driver":
                self.web_driver = get_driver(PARAMS[key])
                
            if key == "path":
                self.web_driver.get(PARAMS[key])
                continue

            if key == "find_element":
                self.element = self.web_driver.find_element(By.XPATH, PARAMS[key])
                continue

            if key == "send_keys":
                for k, v in PARAMS[key].items():
                    self.element.send_keys(v)
                continue

            if key == "click":
                self.element.click()
                continue

            if key == "time_sleep":
                self.web_driver.implicitly_wait(PARAMS[key])
                continue

            if key == "close":
                self.web_driver.close()
                break


