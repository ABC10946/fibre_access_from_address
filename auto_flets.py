from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from rapidfuzz.distance import Levenshtein
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#############
# 対象住所  #
#############

# TEST_CASE1
# ROOM_NAME = "５０５号"

def autoFlets(driver: webdriver.Remote, FIELD_ZIP1: str, FIELD_ZIP2: str, CHOME: str, BANTI: str, GO: str, IS_SHUGO: bool, CONSTRUCT_NAME: str, ROOM_NAME: str) -> str | None:
    try:
        driver.get("https://flets.com/flets-hikari/application/sim/")

        # input form name="FIELD_ZIP1"に入力
        driver.find_element(By.NAME, "FIELD_ZIP1").send_keys(FIELD_ZIP1)
        # input form name="FIELD_ZIP2"に入力
        driver.find_element(By.NAME, "FIELD_ZIP2").send_keys(FIELD_ZIP2)

        # ボタンをクリック class="btn_a_js_co_post_js_icon_blank"
        driver.find_element(By.CLASS_NAME, "search_btn").click()

        # 検索ボタンで新しいタブが開く場合がある -> 新しいウィンドウに切り替え
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[-1])
        except TimeoutException:
            # 新しいウィンドウが開かない場合はそのまま続行
            logger.info("新しいウィンドウが開きませんでした。現在のウィンドウを使用します。")

        # CHOME ボタンは <button> の直テキストではない場合があるため、text() ではなく . を使う
        # また要素が表示・クリック可能になるまで待つ
        chome_xpath = "//button[contains(., '" + CHOME + "')]"
        try:
            chome_el = wait.until(EC.element_to_be_clickable((By.XPATH, chome_xpath)))
            chome_el.click()
        except TimeoutException:
            logger.error(f"CHOME要素が見つかりませんでした: {CHOME}")
            # デバッグ用にページの一部をログ出力
            try:
                logger.debug(driver.page_source[:2000])
            except Exception:
                pass
            driver.quit()
            return None

        # input name="banchi1to3manualAddressNum1"に入力
        driver.find_element(By.NAME, "banchi1to3manualAddressNum1").send_keys(BANTI)

        # input name="banchi1to3manualAddressNum2"に入力
        driver.find_element(By.NAME, "banchi1to3manualAddressNum2").send_keys(GO)

        if IS_SHUGO:
            # 集合住宅の場合
            # ラジオボタン id="id_buildType_2"をクリック
            driver.find_element(By.ID, "id_buildType_2").click()

            # id_nextButtonをクリック
            driver.find_element(By.ID, "id_nextButton").click()

            # ul class="btn_list"の中にあるli要素の数を取得
            li_list = driver.find_elements(By.CLASS_NAME, "build1")
            # もし複数の建物がある場合名前を出力

            min_levenshtein = 100
            target_li = None

            for li in li_list:
                logger.info(li.text)
                # li.textのうちCONSTRUCT_NAMEとレーベンシュタイン距離が一番近いものをクリック
                levenshtein_distance = Levenshtein.distance(li.text, CONSTRUCT_NAME)
                if levenshtein_distance < min_levenshtein:
                    min_levenshtein = levenshtein_distance
                    target_li = li
            
            logger.info("最小レーベンシュタイン距離: " + str(min_levenshtein))

            if target_li is None:
                logger.error("建物名が見つかりませんでした")
                driver.quit()
                return "建物名が見つかりませんでした"

            target_li.click()


            # li class="build1"をクリック
            # driver.find_element(By.CLASS_NAME, "build1").click()

            # 建物名が含まれてるテキストのボタン要素をクリック
            # driver.find_element(By.XPATH, "//button[contains(text(), '" + TATEMONO_NAME +"')]").click()

            # 部屋名が含まれてるテキストのボタン要素をクリック
            ROOM_NAME_ZENKAKU = ROOM_NAME.translate(str.maketrans('0123456789', '０１２３４５６７８９'))
            logger.info("クリックする部屋名: " + ROOM_NAME_ZENKAKU)

            driver.find_element(By.XPATH, "//button[contains(text(), '" + ROOM_NAME_ZENKAKU +"')]").click()

        else:
            # 一戸建ての場合
            # ラジオボタン id="id_buildType_1"をクリック
            driver.find_element(By.ID, "id_buildType_1").click()

            # id_nextButtonをクリック
            driver.find_element(By.ID, "id_nextButton").click()

        # XPATH /html/body/main/div/div[3]/p[1] にあるテキストを取得
        fibreType = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/p[1]").text

        driver.quit()

        logger.info(fibreType)

        return fibreType

    except Exception as e:
        logger.info("Error")
        logger.error(e)
        driver.quit()


if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )

    FIELD_ZIP1 = ""
    FIELD_ZIP2 = ""
    CHOME = ""
    BANTI = ""
    GO = ""
    ROOM_NAME = ""
    IS_SHUGO = True
    TATEMONO_NAME = ""
    autoFlets(driver, FIELD_ZIP1, FIELD_ZIP2, CHOME, BANTI, GO, IS_SHUGO, TATEMONO_NAME, ROOM_NAME)
