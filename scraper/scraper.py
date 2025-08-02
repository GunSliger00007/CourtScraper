# scraper/delhi_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_case(case_type: str, case_number: str, case_year: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    results = []

    try:
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status/")
        wait.until(EC.presence_of_element_located((By.ID, "case_type")))

        # Fill the form fields
        Select(driver.find_element(By.ID, "case_type")).select_by_value(case_type)
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        Select(driver.find_element(By.ID, "case_year")).select_by_value(case_year)

        # Captcha handling
        captcha = wait.until(EC.visibility_of_element_located((By.ID, "captcha-code"))).text.strip()
        captcha_input = next((el for el in driver.find_elements(By.ID, "captchaInput") if el.is_displayed()), None)
        if captcha_input:
            captcha_input.send_keys(captcha)
        else:
            raise Exception("Captcha input not found")

        # Submit form
        driver.find_element(By.ID, "search").click()
        wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))
        time.sleep(2)

        # Scrape results
        for row in driver.find_elements(By.CSS_SELECTOR, "#caseTable tbody tr"):
            sno = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
            diary_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            diary_text = diary_cell.text.strip()

            order_url = "No order URL found"
            for a in diary_cell.find_elements(By.TAG_NAME, "a"):
                if a.text.strip().lower() == "orders":
                    order_url = a.get_attribute("href")
                    break

            party = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
            listing = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()

            case_data = {
                "sno": sno,
                "case_no": diary_text,
                "party": party,
                "listing": listing,
                "order_url": order_url,
                "orders": []
            }

            # Scrape detailed orders if order_url exists
            if order_url != "No order URL found":
                driver.get(order_url)
                wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))
                time.sleep(2)

                for orow in driver.find_elements(By.CSS_SELECTOR, "#caseTable tbody tr"):
                    try:
                        s_no = orow.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
                        link_elem = orow.find_element(By.CSS_SELECTOR, "td:nth-child(2) a")
                        text = link_elem.text.strip()
                        link = link_elem.get_attribute("href")
                        date = orow.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()

                        corrigendum = orow.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                        corrigendum_link = corrigendum.find_element(By.TAG_NAME, "a").get_attribute("href") if corrigendum.find_elements(By.TAG_NAME, "a") else corrigendum.text.strip()

                        hindi = orow.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
                        hindi_link = hindi.find_element(By.TAG_NAME, "a").get_attribute("href") if hindi.find_elements(By.TAG_NAME, "a") else hindi.text.strip()

                        case_data["orders"].append({
                            "text": text,
                            "link": link,
                            "date": date,
                            "corrigendum": corrigendum_link or "No Corrigendum",
                            "hindi": hindi_link or "No Hindi Order"
                        })
                    except:
                        continue

                driver.back()
                wait.until(EC.visibility_of_element_located((By.ID, "caseTable")))
                time.sleep(1)

            results.append(case_data)

    finally:
        driver.quit()

    return results
