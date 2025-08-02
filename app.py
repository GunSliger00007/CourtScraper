from flask import Flask, render_template, request
from scraper.scraper import fetch_case_data

app = Flask(__name__)

# Move this to a config file later
from utils.casetype import case_types

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        filing_year = request.form["filing_year"]
        data = fetch_case_data(case_type, case_number, filing_year)
        return render_template("result.html", data=data)
    
    return render_template("form.html", case_types=case_types)
