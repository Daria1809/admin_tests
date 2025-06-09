from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
base_url = "https://the-internet.herokuapp.com"


def test_login_success():
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()
    assert "You logged into a secure area!" in driver.page_source


def test_login_failure():
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "username").send_keys("wrong")
    driver.find_element(By.ID, "password").send_keys("wrong")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()
    assert "Your username is invalid!" in driver.page_source


def test_checkboxes():
    driver.get(f"{base_url}/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    checkboxes[0].click()
    assert checkboxes[0].is_selected()


def test_dropdown():
    driver.get(f"{base_url}/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 2")
    assert dropdown.first_selected_option.text == "Option 2"


def test_dynamic_loading():
    driver.get(f"{base_url}/dynamic_loading/1")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    text = wait.until(EC.visibility_of_element_located((By.ID, "finish"))).text
    assert text == "Hello World!"


def test_file_upload():
    driver.get(f"{base_url}/upload")
    file_path = os.path.abspath(__file__)  # загрузим сам файл скрипта
    driver.find_element(By.ID, "file-upload").send_keys(file_path)
    driver.find_element(By.ID, "file-submit").click()
    assert "File Uploaded!" in driver.page_source


def test_js_alert():
    driver.get(f"{base_url}/javascript_alerts")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    alert = driver.switch_to.alert
    alert.accept()
    result = driver.find_element(By.ID, "result").text
    assert "You successfully clicked an alert" in result


def test_hover():
    driver.get(f"{base_url}/hovers")
    from selenium.webdriver import ActionChains
    avatar = driver.find_element(By.CSS_SELECTOR, ".figure")
    ActionChains(driver).move_to_element(avatar).perform()
    caption = driver.find_element(By.CSS_SELECTOR, ".figcaption h5")
    assert "name: user1" in caption.text.lower()


def test_broken_images():
    driver.get(f"{base_url}/broken_images")
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        if img.get_attribute("naturalWidth") == '0':
            print("Broken image found")
            assert True
            return
    assert False, "No broken images found (unexpected)"


def test_infinite_scroll():
    driver.get(f"{base_url}/infinite_scroll")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    paragraphs = driver.find_elements(By.CLASS_NAME, "jscroll-added")
    assert len(paragraphs) > 0


# 🧪 Run all tests
if __name__ == "__main__":
    tests = [
        test_login_success,
        test_login_failure,
        test_checkboxes,
        test_dropdown,
        test_dynamic_loading,
        test_file_upload,
        test_js_alert,
        test_hover,
        test_broken_images,
        test_infinite_scroll,
    ]

    for test in tests:
        try:
            test()
            print(f"{test.__name__} passed")
        except Exception as e:
            print(f"{test.__name__} failed: {e}")

    driver.quit()
