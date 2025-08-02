# Delhi High Court Case Scraper

A Selenium-based scraper to fetch case information from the Delhi High Court website, including case listings and detailed orders. Handles in-page CAPTCHA manually during runtime.

---

## Features

- Interactive lookup for case type, number, and year.
- Scrapes case details including petitioner/respondent, listing info, and order URLs.
- Handles manual CAPTCHA solving through user input.
- Navigates to detailed orders and extracts order info with download links.
- Shortens long URLs in the UI for better readability.
- Supports pagination for multiple orders (if implemented).
- Clean and minimal UI for displaying results.

---

## License

This project is released under the [MIT License](LICENSE).

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version
- `pip` package manager

### Installation

Clone the repository:

