from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

URL = "https://www.mobile.de/"
CAR_AGE_MIN = "2010"
KILOMETERS_MIN = "150000"
KILOMETERS_MAX = "300000"

PRICE_MIN = "3000"
PRICE_MAX = "10000"


def fill_search_field(curr_driver, data_test_id_value: str, field_value: str):
    try:
        input_field = WebDriverWait(curr_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@data-testid='{data_test_id_value}']"))
        )

        # Find the input field child element
        # input_field = parent_element.find_element(By.XPATH, ".//following::input[1]")

        # Fill the input field with the desired value
        input_field.send_keys(field_value)
        print(f"Input field {data_test_id_value} filled with value: {field_value}")
    except Exception as e:
        print(f"Error: {e}")


def click_button_by_text(curr_driver, text: str):
    try:
        # Adjust the wait time and condition as necessary
        button = WebDriverWait(curr_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
        )
        # Press the button
        button.click()
        print(f"Button {text} clicked successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # Set up the driver (this will automatically download the latest Chrome driver)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(URL)

    # Wait for up to 10 seconds for the button to become clickable

    click_button_by_text(curr_driver=driver, text="Einverstanden")

    # Cookies accepted
    time.sleep(1)

    try:
        # Locate the div with the data-testid attribute "qs-more-filter"
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='qs-more-filter']"))
        )

        # Click on the div element
        div_element.click()
        print("Div clicked successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Let's fill in some inputs

    fill_search_field(curr_driver=driver, data_test_id_value="price-filter-min-input", field_value=PRICE_MIN)
    fill_search_field(curr_driver=driver, data_test_id_value="price-filter-max-input", field_value=PRICE_MAX)
    fill_search_field(curr_driver=driver, data_test_id_value="first-registration-filter-min-input", field_value=CAR_AGE_MIN)
    fill_search_field(curr_driver=driver, data_test_id_value="mileage-filter-min-input", field_value=KILOMETERS_MIN)
    fill_search_field(curr_driver=driver, data_test_id_value="mileage-filter-max-input", field_value=KILOMETERS_MAX)

    try:
        # Locate the div with the data-testid attribute "qs-more-filter"
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='stickyBar-submit-search']"))
        )

        # Click on the div element
        div_element.click()
        print("Div clicked successfully.")
    except Exception as e:
        print(f"Error: {e}")


    time.sleep(120)

    driver.quit()
