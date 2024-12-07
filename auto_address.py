from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def autoAddress(driver: webdriver.Remote, TATEMONO_NAME: str):
    try:
        driver.get("https://www.google.com/maps")

        # input id="searchboxinput"に建物名を入力
        driver.find_element(By.ID, "searchboxinput").send_keys(TATEMONO_NAME)

        # textareaでエンターキーを押す
        driver.find_element(By.ID, "searchboxinput").send_keys(u'\ue007')

        retryCount = 10

        while retryCount > 0:
            address = driver.find_element(By.TAG_NAME, "body").text
            # 〒マークから始まる文字列を取得
            # address = re.search(r"〒[0-9]{3}-[0-9]{4}.*", address).group()
            if "〒" in address:
                logger.info("住所取得成功")
                break
            else:
                logger.info("住所取得失敗")
                retryCount -= 1
                time.sleep(3)

        # ページのテキストから住所を取得　正規表現で取得
        address = driver.find_element(By.TAG_NAME, "body").text
        # 〒マークから始まる文字列を取得
        addressSearch = re.search(r"〒[0-9]{3}-[0-9]{4}.*", address)
        if addressSearch is None:
            logger.error("住所取得失敗")
            driver.quit()
            return None, None, None, None, None

        address = addressSearch.group()

        logger.info(address)
        zipCode1 = address[1:4]
        zipCode2 = address[5:9]

        # # 住所の中から丁目を取得 数字は全角
        chomeBantiGoRaw = re.findall(r"[０-９]{0,2}", address)
        filtered = [x for x in chomeBantiGoRaw if x != '']
        chome = filtered[0]

        chome = chome.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # 全角数字を半角数字に変換

        # # 住所の中から番地を取得 〇丁目〇〇番―〇〇号の番地を取得
        chomeBantiGoRaw = re.findall(r"[０-９]{0,2}", address)
        filtered = [x for x in chomeBantiGoRaw if x != '']
        banti = filtered[1]
        # 全角数字を半角数字に変換
        banti = banti.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # 住所の中から号を取得
        go = filtered[2]
        # 全角数字を半角数字に変換
        go = go.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # time.sleep(60)
        driver.quit()

        return zipCode1, zipCode2, chome, banti, go

    except Exception as e:
        logger.error("Error")
        logger.error(e)
        driver.quit()

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
)
    TATEMONO_SEARCH_WORD = ""
    autoAddress(driver, TATEMONO_SEARCH_WORD)