from auto_address import autoAddress
from auto_flets import autoFlets
from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Remote(
        command_executor='http://selenium.k8s.local/wd/hub',
        options=chrome_options
    )

    TATEMONO_SEARCH_WORD = ""
    ROOM_NAME = ""

    zipCode1, zipCode2, chome, banti, go = autoAddress(driver, TATEMONO_SEARCH_WORD)

    driver = webdriver.Remote(
        command_executor='http://selenium.k8s.local/wd/hub',
        options=chrome_options
    )

    chome = chome.translate(str.maketrans('0123456789', '０１２３４５６７８９'))
    chome = chome + "丁目"

    autoFlets(driver, zipCode1, zipCode2, chome, banti, go, True, TATEMONO_SEARCH_WORD, ROOM_NAME)
