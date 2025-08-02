from flask import Flask, request, render_template
from scraper.scraper import scrape_case

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
def fetch():
    case_type = request.form["case_type"]
    case_number = request.form["case_number"]
    case_year = request.form["case_year"]

    try:
        results = scrape_case(case_type, case_number, case_year)
    except Exception as e:
        return render_template("index.html", results=[], error=str(e))

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
