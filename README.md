Court Data Fetcher
A web application to fetch and display case metadata and orders from the Delhi High Court website.
Court Chosen

Delhi High Court: https://delhihighcourt.nic.in/
Reason: The Delhi High Court website provides a structured case status search interface, making it a suitable target for scraping case metadata and orders. It is a prominent court with accessible public data, though it includes CAPTCHA challenges.

Setup Steps

Clone the Repository:
```git clone https://github.com/GunSliger00007/CourtScraper.git
```
cd court_data_fetcher


Install Dependencies:Ensure Python 3.9+ is installed, then install required packages:pip install -r requirements.txt

Note: The project requires selenium and ChromeDriver. Install ChromeDriver compatible with your system or use webdriver-manager for automatic management.
Initialize the Database:Create the SQLite database for storing query logs:python -c "from database import init_db; init_db()"


Run the Application:Start the Flask server:python app.py


Access the App:Open a browser and navigate to http://localhost:5000.
Optional: Run with Docker:Build and run the Docker container:

```docker run -it --rm -p 5000:5000 my-flask-app
```




CAPTCHA Strategy
The Delhi High Court website employs image-based CAPTCHAs to prevent automated queries, which poses a significant challenge for scraping. The current scraper implementation (scraper.py) is a placeholder and assumes manual or third-party CAPTCHA solving due to ethical and legal considerations. Below is the strategy:

Current Implementation:
The scraper attempts to locate the CAPTCHA image (captcha-img) and raises an error, indicating that CAPTCHA solving is required.
Automatic text extraction (e.g., reading CAPTCHA text directly) is not feasible for image-based CAPTCHAs.


Proposed Solutions:
Manual CAPTCHA Input:
Modify the frontend (index.html) to display the CAPTCHA image retrieved from the scraper.
Prompt the user to enter the CAPTCHA code in a text input field.
Send the user-provided CAPTCHA code back to the scraper for form submission.


Third-Party CAPTCHA Solving:
Integrate a service like 2Captcha or Anti-CAPTCHA to programmatically solve CAPTCHAs.
Requires an API key and additional configuration (see environment variables below).
Note: Use of such services must comply with legal and ethical guidelines, and users should verify compliance with the court's terms of service.


Audio CAPTCHA Fallback:
If available, leverage the audio CAPTCHA option provided by the website.
Use speech-to-text libraries (e.g., speech_recognition) to process audio, though this is complex and less reliable.




Limitations:
The provided delhi_scraper.py assumes a text-based CAPTCHA, which does not work for the Delhi High Court’s image-based CAPTCHA.
Full automation without user intervention may violate the website’s terms or local regulations. Manual input is recommended for compliance.


Future Improvements:
Implement a WebSocket-based solution to stream the CAPTCHA image to the frontend and collect user input.
Periodically test the scraper against website updates, as CAPTCHA mechanisms or form structures may change.



Additional Notes

License: MIT License
Demo Video: A ≤5-minute screen-capture video demonstrating the end-to-end flow (form submission, case details display, PDF link) is recommended but not included in this repository.
Pagination: Not implemented in the current scraper. To add pagination, modify scraper.py to detect and iterate through pagination controls (e.g., "Next" button) on the results page.
PDF Downloads: The app currently returns PDF URLs. To enable direct downloads, implement a route to fetch and serve PDFs using requests or Selenium.
Dependencies: Ensure selenium and webdriver-manager are added to requirements.txt for the scraper to work.
Ethical Considerations: Automated scraping must respect the court’s terms of service and applicable laws. Manual CAPTCHA input is the safest approach for compliance.
