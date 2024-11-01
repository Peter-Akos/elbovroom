from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

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


def scroll_to_bottom(curr_driver):
    """Scroll to the bottom of the page."""
    curr_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolled to the bottom of the page.")
    time.sleep(2)  # Wait briefly to allow content to load


def get_listing_titles_and_details(curr_driver, div_class_prefix: str, title_class: str, details_test_id: str) -> tuple[
    list, list]:
    try:
        # Locate divs with class starting with the specified prefix
        div_elements = WebDriverWait(curr_driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//div[starts-with(@class, '{div_class_prefix}')]"))
        )
        print(f"Found {len(div_elements)} div elements with class starting with '{div_class_prefix}'.")

        titles = []
        details = []
        for i, div in enumerate(div_elements, start=1):
            try:
                # Extract title from h2 element with specific class
                title_element = div.find_element(By.XPATH, f".//h2[@class='{title_class}']")
                title = title_element.text

                # Extract listing details from div with data-testid attribute
                details_element = div.find_element(By.XPATH, f".//div[@data-testid='{details_test_id}']")
                detail = details_element.text

                # Store title and details in a dictionary
                titles.append(title)
                details.append(detail)
                print(f"Listing {i} - Title: {title}")
                print(f"Listing {i} - Detail: {detail}")
            except Exception as e:
                print(f"Error retrieving data for listing {i}: {e}")

        return titles, details
    except Exception as e:
        print(f"Error in get_listing_titles_and_details: {e}")
        return [], []


def scroll_hover_and_click_next_button(curr_driver, next_button_test_id: str):
    """Scroll to, hover over, and click the 'Next' pagination button."""
    try:
        # Locate the 'Next' button by its data-testid attribute
        next_button = WebDriverWait(curr_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//button[@data-testid='{next_button_test_id}']"))
        )

        # Scroll to the button to bring it into view
        curr_driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
        print("Scrolled to 'Next' button.")

        # Hover over the button
        ActionChains(curr_driver).move_to_element(next_button).perform()
        print("Mouse hovered over 'Next' button.")

        # Click the button
        next_button.click()
        print("Clicked on the 'Next' pagination button.")

        time.sleep(2)  # Wait briefly for the next page to load
    except Exception as e:
        print("No more pages or error in clicking next button:", e)
        return False
    return True

def save_data(data, filename):
    # current_df = pd.read_csv(filename)
    new_df = pd.DataFrame(data)
    # united = pd.concat([current_df, new_df], ignore_index=True)
    new_df.to_csv(filename, index=False)



def run_session(price_min, price_max, filename):
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

    fill_search_field(curr_driver=driver, data_test_id_value="price-filter-min-input", field_value=price_min)
    fill_search_field(curr_driver=driver, data_test_id_value="price-filter-max-input", field_value=price_max)
    fill_search_field(curr_driver=driver, data_test_id_value="first-registration-filter-min-input",
                      field_value=CAR_AGE_MIN)
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

    # Initialize an empty list to store data across pages
    all_listings_data = {
        "titles": [],
        "details": []
    }

    while True:
        # Extract listings on the current page
        titles, details = get_listing_titles_and_details(
            driver, div_class_prefix='mN_WC', title_class='QeGRL', details_test_id='listing-details-attributes'
        )
        all_listings_data['titles'] += titles
        all_listings_data['details'] += details

        # Attempt to scroll to, hover over, and click the 'Next' button
        if not scroll_hover_and_click_next_button(driver, next_button_test_id='pagination:next'):
            break  # Exit loop if there are no more pages or an error occurred

    save_data(all_listings_data, filename)

    driver.quit()


if __name__ == '__main__':
    CAR_AGE_MIN = "2010"
    KILOMETERS_MIN = "150000"
    KILOMETERS_MAX = "300000"

    PRICE_MIN = 3000
    PRICE_MAX = 10000

    for price_min in range(PRICE_MIN, PRICE_MAX, 200):
        price_max = price_min + 199
        run_session(str(price_min), str(price_max), f"vigyazz-{price_min}-{price_max}.csv")



