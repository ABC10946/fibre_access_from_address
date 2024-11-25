from selenium import webdriver
from selenium.webdriver.common.by import By
import time



#############
# 対象住所  #
#############

# TEST_CASE1
# ROOM_NAME = "５０５号"

def autoFlets(driver, FIELD_ZIP1, FIELD_ZIP2, CHOME, BANTI, GO, IS_SHUGO, ROOM_NAME):
    try:
        driver.get("https://flets.com/application/sim")

        # input form name="FIELD_ZIP1"に入力
        driver.find_element(By.NAME, "FIELD_ZIP1").send_keys(FIELD_ZIP1)
        # input form name="FIELD_ZIP2"に入力
        driver.find_element(By.NAME, "FIELD_ZIP2").send_keys(FIELD_ZIP2)

        # ボタンをクリック class="btn_a_js_co_post_js_icon_blank"
        driver.find_element(By.CLASS_NAME, "btn_a").click()

        # 新しいタブが開くので、タブを切り替える
        driver.switch_to.window(driver.window_handles[1])

        # ３丁目が含まれてるテキストのボタン要素をクリック
        driver.find_element(By.XPATH, "//button[contains(text(), '" + CHOME +"')]").click()

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
            for li in li_list:
                print(li.text)

            # li class="build1"をクリック
            driver.find_element(By.CLASS_NAME, "build1").click()

            # 建物名が含まれてるテキストのボタン要素をクリック
            # driver.find_element(By.XPATH, "//button[contains(text(), '" + TATEMONO_NAME +"')]").click()

            # 部屋名が含まれてるテキストのボタン要素をクリック
            driver.find_element(By.XPATH, "//button[contains(text(), '" + ROOM_NAME +"')]").click()

        else:
            # 一戸建ての場合
            # ラジオボタン id="id_buildType_1"をクリック
            driver.find_element(By.ID, "id_buildType_1").click()

            # id_nextButtonをクリック
            driver.find_element(By.ID, "id_nextButton").click()

        # XPATH /html/body/main/div/div[3]/p[1] にあるテキストを取得
        print(driver.find_element(By.XPATH, "/html/body/main/div/div[3]/p[1]").text)

        time.sleep(5)
        driver.quit()
    except Exception as e:
        print("Error")
        print(e)
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
