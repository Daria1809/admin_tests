from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ADMIN_URL = "http://localhost/opencart/admin"   
STORE_URL = "http://localhost/opencart/"        
USERNAME = "admin"
PASSWORD = "admin"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Вход в админку
def admin_login():
    driver.get(ADMIN_URL)
    driver.find_element(By.ID, "input-username").send_keys(USERNAME)
    driver.find_element(By.ID, "input-password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-close"))).click()
    except:
        pass

# Создание категории
def create_category(name="Devices"):
    driver.get(ADMIN_URL + "#catalog/category")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Categories"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-original-title='Add New']"))).click()
    driver.find_element(By.ID, "input-name1").send_keys(name)
    driver.find_element(By.ID, "input-meta-title1").send_keys("Devices Meta")
    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()

# Добавление товара
def add_product(name, category="Devices", model="ModelX", desc="Описание товара"):
    driver.get(ADMIN_URL + "#catalog/product")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Products"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-original-title='Add New']"))).click()

    driver.find_element(By.ID, "input-name1").send_keys(name)
    driver.find_element(By.ID, "input-meta-title1").send_keys(name)

    driver.find_element(By.CSS_SELECTOR, "a[href='#tab-data']").click()
    driver.find_element(By.ID, "input-model").send_keys(model)

    driver.find_element(By.CSS_SELECTOR, "a[href='#tab-links']").click()
    cat_input = driver.find_element(By.ID, "input-category")
    cat_input.send_keys(category)
    time.sleep(1)
    cat_input.send_keys(Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()

# Поиск товара на витрине
def search_store(query):
    driver.get(STORE_URL)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    return [el.text for el in driver.find_elements(By.CSS_SELECTOR, ".product-thumb")]

# Удаление товара по имени
def delete_product(name):
    driver.get(ADMIN_URL + "#catalog/product")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Products"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "filter_name"))).clear()
    driver.find_element(By.NAME, "filter_name").send_keys(name)
    driver.find_element(By.ID, "button-filter").click()
    time.sleep(1)
    try:
        driver.find_element(By.NAME, "selected[]").click()
        driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Delete']").click()
        driver.switch_to.alert.accept()
    except:
        print(f"Продукт '{name}' не найден или уже удалён")

# Запуск всех шагов
if __name__ == "__main__":
    try:
        admin_login()

        print("Создаём категорию Devices...")
        create_category("Devices")

        print("🖱 Добавляем 2 мыши и 2 клавиатуры...")
        add_product("Mouse A", desc="Gaming Mouse")
        add_product("Mouse B", desc="Office Mouse")
        add_product("Keyboard A", desc="Mechanical Keyboard")
        add_product("Keyboard B", desc="Wireless Keyboard")

        print("Проверяем наличие всех товаров...")
        all_results = search_store("Mouse") + search_store("Keyboard")
        assert any("Mouse A" in r for r in all_results)
        assert any("Mouse B" in r for r in all_results)
        assert any("Keyboard A" in r for r in all_results)
        assert any("Keyboard B" in r for r in all_results)
        print("Все товары найдены!")

        print("Удаляем Mouse B и Keyboard A...")
        admin_login()
        delete_product("Mouse B")
        delete_product("Keyboard A")

        print("Проверяем, что остались только нужные товары...")
        remaining = search_store("Mouse") + search_store("Keyboard")
        assert any("Mouse A" in r for r in remaining)
        assert any("Keyboard B" in r for r in remaining)
        assert all("Mouse B" not in r for r in remaining)
        assert all("Keyboard A" not in r for r in remaining)
        print("Удаление подтверждено, тест завершён успешно!")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        driver.quit()
