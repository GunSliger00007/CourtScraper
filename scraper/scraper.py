from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options for headless mode (modern style)
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Use modern headless flag
chrome_options.add_argument("--disable-gpu")   # Optional, keep for compatibility
chrome_options.add_argument("--no-sandbox")    # Useful in restricted environments
chrome_options.add_argument("--window-size=1920,1080")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the Delhi High Court case status page
    driver.get("https://delhihighcourt.nic.in/app/get-case-type-status/")

    wait = WebDriverWait(driver, 15)

    # Wait for dropdown element for case type to appear
    wait.until(EC.presence_of_element_located((By.ID, "case_type")))

    # Select the case type
    case_type_dropdown = Select(driver.find_element(By.ID, "case_type"))
    case_type_dropdown.select_by_value("ARB.A.")  # Adjust as needed

    # Enter case number
    case_number_input = driver.find_element(By.ID, "case_number")
    case_number_input.clear()
    case_number_input.send_keys("1")               # Adjust as needed

    # Select the year
    year_dropdown = Select(driver.find_element(By.ID, "case_year"))
    year_dropdown.select_by_value("2023")          # Adjust as needed

    # Wait for captcha to show and extract the text
    captcha_element = wait.until(EC.visibility_of_element_located((By.ID, "captcha-code")))
    captcha_text = captcha_element.text.strip()
    print(f"Captcha displayed: {captcha_text}")

    # Find the interactable captcha input field
    captcha_inputs = driver.find_elements(By.ID, "captchaInput")
    captcha_input = None
    for elem in captcha_inputs:
        if elem.is_displayed() and elem.is_enabled():
            captcha_input = elem
            break

    if captcha_input:
        captcha_input.clear()
        try:
            captcha_input.send_keys(captcha_text)
            print("Captcha input filled via send_keys.")
        except Exception as e:
            print(f"send_keys failed: {e}, trying JS injection...")
            driver.execute_script("arguments[0].value = arguments[1];", captcha_input, captcha_text)
    else:
        print("Captcha input field not found or interactable.")
        driver.quit()
        exit(1)

    # Wait for the Search/Submit button to be clickable
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "search")))

    # Scroll to and click the submit button with fallback
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    try:
        submit_button.click()
        print("Submit button clicked normally.")
    except Exception as click_error:
        print(f"Normal click failed: {click_error}, trying JS click...")
        driver.execute_script("arguments[0].click();", submit_button)

    # Wait for results table to appear
    wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))

    # Short pause to ensure data loaded
    time.sleep(2)

    # Extract all rows from main results table
    rows = driver.find_elements(By.CSS_SELECTOR, "#caseTable tbody tr")

    for idx, row in enumerate(rows, 1):
        sno = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        diary_case_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
        diary_case_text = diary_case_cell.text.strip()

        # Find the Orders link explicitly by checking anchor text
        order_url = "No order URL found"
        anchors = diary_case_cell.find_elements(By.TAG_NAME, "a")
        for a in anchors:
            if a.text.strip().lower() == "orders":
                order_url = a.get_attribute("href")
                break

        petitioner_respondent = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
        listing_info = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()

        print(f"Result {idx}:")
        print(f"S.No.: {sno}")
        print(f"Diary No. / Case No. [STATUS]: {diary_case_text}")
        print(f"Petitioner Vs. Respondent: {petitioner_respondent}")
        print(f"Listing Date / Court No.: {listing_info}")
        print(f"Orders URL: {order_url}")
        print("-" * 40)

        # If Orders URL found, navigate and scrape detailed orders
        if order_url != "No order URL found":
            print("Navigating to Orders page to extract detailed order links...\n")
            driver.get(order_url)

            # Wait for detailed orders table to load
            wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))
            time.sleep(2)  # Extra wait to ensure table loads content

            order_rows = driver.find_elements(By.CSS_SELECTOR, "#caseTable tbody tr")

            print(f"Detailed Orders for Case {sno}:")
            for orow in order_rows:
                # Extract S.No.
                s_no = orow.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()

                # Extract Case No/Order Link text and URL
                case_link_elem = orow.find_element(By.CSS_SELECTOR, "td:nth-child(2) a")
                case_link_text = case_link_elem.text.strip()
                case_link_url = case_link_elem.get_attribute("href")

                # Date of order
                date_of_order = orow.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()

                # Corrigendum Link/Date (may be empty or link)
                corrigendum_cell = orow.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                try:
                    corrigendum_link = corrigendum_cell.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    corrigendum_link = corrigendum_cell.text.strip() or "No Corrigendum"

                # Hindi Order (may be empty or link)
                hindi_cell = orow.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
                try:
                    hindi_order_link = hindi_cell.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    hindi_order_link = hindi_cell.text.strip() or "No Hindi Order"

                print(f"  S.No.: {s_no}")
                print(f"  Case No/Order Link Text: {case_link_text}")
                print(f"  Case No/Order Link URL: {case_link_url}")
                print(f"  Date of Order: {date_of_order}")
                print(f"  Corrigendum Link or Date: {corrigendum_link}")
                print(f"  Hindi Order: {hindi_order_link}")
                print("-" * 30)
            print("=" * 60 + "\n")

            # After scraping orders, come back to the results page to continue if multiple
            driver.back()
            wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))
            time.sleep(1)

finally:
    driver.quit()
