from auto_address import autoAddress
from auto_flets import autoFlets
from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )

    TATEMONO_SEARCH_WORD = ""
    TATEMONO_NAME = ""
    ROOM_NAME = ""
    zipCode1, zipCode2, chome, banti, go = autoAddress(driver, TATEMONO_SEARCH_WORD)
    autoFlets(driver, zipCode1, zipCode2, chome, banti, go, True, TATEMONO_NAME, ROOM_NAME)