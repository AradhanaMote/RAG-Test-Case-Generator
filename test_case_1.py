from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

def add_tshirt_to_cart():
    service = Service(r"D:\VSCode\AutonomousQAAgent\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(r"D:\VSCode\AutonomousQAAgent\templates\checkout.html")
    
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-1"))
        )
        add_to_cart_button.click()

        # Since the page does NOT update qty automatically, do it manually
        qty = driver.find_element(By.ID, "qty-1")
        qty.clear()
        qty.send_keys("1")

        driver.execute_script("return calcTotal();")

        time.sleep(1)

        t_shirt_quantity = driver.find_element(By.ID, "qty-1")
        total = driver.find_element(By.ID, "total")

        assert t_shirt_quantity.get_attribute("value") == "1"
        assert total.text == "20.00"

        print("✅ Test Passed: T-shirt is added to the cart with a total of $20.00")
        time.sleep(5)

    except AssertionError as e:
        print(f"❌ Test Failed: {e}")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
    finally:
        driver.quit()

if __name__ == "__main__":
    add_tshirt_to_cart()
