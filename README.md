Court Data Fetcher
A web application to fetch and display case metadata and orders from the Delhi High Court website using Flask and Selenium.
Court Chosen
Delhi High Court: https://delhihighcourt.nic.in/Reason: The Delhi High Court provides a structured case status search interface, making it suitable for scraping case metadata and orders. It is a prominent court with publicly accessible data, though it includes CAPTCHA challenges that require careful handling.
Features

Search for case details using case number, party name, or other parameters.
Display case metadata and associated court orders.
Store query logs in an SQLite database.
Handle CAPTCHA challenges with manual input (third-party services optional).
Flask-based web interface for user interaction.

Setup Instructions
Prerequisites

Python: Version 3.9 or higher.
Chrome Browser: Required for Selenium automation.
ChromeDriver: Must match your Chrome browser version. Alternatively, use webdriver-manager for automatic management.
Docker: Optional for containerized deployment.

Installation Steps

Clone the Repository:
```
git clone https://github.com/GunSliger00007/CourtScraper.git
cd CourtScraper
```

Install Dependencies:Ensure Python 3.9+ is installed, then run:
```
pip install -r requirements.txt
```

Note: requirements.txt should include selenium, webdriver-manager, flask, and other necessary packages.

Initialize the Database:Create the SQLite database to store query logs:
python -c "from database import init_db; init_db()"


Run the Application:Start the Flask server:
```
python app.py
```

Access the Application:Open a browser and navigate to http://localhost:5000.

Optional: Run with Docker:Build and run the Docker container:
```
docker build -t my-flask-app .
docker run -it --rm -p 5000:5000 my-flask-app
```



CAPTCHA Handling Strategy
The Delhi High Court website uses image-based CAPTCHAs to prevent automated queries, posing a challenge for scraping. The current implementation in scraper.py is a placeholder and assumes manual or third-party CAPTCHA solving due to ethical and legal considerations.
Current Implementation

The scraper locates the CAPTCHA image (captcha-img) and raises an error, indicating that CAPTCHA solving is required.
Automatic text extraction from image-based CAPTCHAs is not feasible.

Proposed Solutions

Manual CAPTCHA Input:

Modify index.html to display the CAPTCHA image retrieved by the scraper.
Prompt the user to enter the CAPTCHA code in a text input field.
Send the user-provided code back to the scraper for form submission.


Third-Party CAPTCHA Solving:

Integrate services like 2Captcha or Anti-CAPTCHA for programmatic CAPTCHA solving.
Requires an API key and configuration in environment variables (e.g., .env).
Note: Use of such services must comply with the court's terms of service and applicable laws.


Audio CAPTCHA Fallback:

If available, use the website’s audio CAPTCHA option.
Process audio with speech-to-text libraries (e.g., speech_recognition), though this is complex and less reliable.



Limitations

The provided delhi_scraper.py assumes a text-based CAPTCHA, which is incompatible with the Delhi High Court’s image-based CAPTCHA.
Full automation without user intervention may violate the website’s terms or local regulations. Manual CAPTCHA input is recommended for compliance.

Future Improvements

Implement a WebSocket-based solution to stream CAPTCHA images to the frontend and collect user input dynamically.
Add pagination support in scraper.py to handle multi-page results by detecting and iterating through pagination controls (e.g., "Next" button).
Enable direct PDF downloads by adding a Flask route to fetch and serve PDFs using requests or Selenium.
Periodically test the scraper against website updates, as CAPTCHA mechanisms or form structures may change.

Additional Notes

License: MIT License.
Demo Video: A ≤5-minute screen-capture video demonstrating the end-to-end flow (form submission, case details display, PDF link) is recommended but not included.
Dependencies: Ensure selenium and webdriver-manager are included in requirements.txt.
Ethical Considerations: Automated scraping must respect the court’s terms of service and applicable laws. Manual CAPTCHA input is the safest approach for compliance.

Contributing
Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository.