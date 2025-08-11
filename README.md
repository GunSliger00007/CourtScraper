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



CAPTCHA Handling
The current scraper reads text-based CAPTCHA codes directly from the page and inputs them automatically.




Contributing
Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository.

License
MIT License — free to use and modify with attribution.