from flask import Flask, request, render_template
from scraper.scraper import scrape_case
from utils.casetype import case_types
from datetime import datetime
from models import db, CaseQuery
import json
# Generate list of years from current year to 1951
years = list(range(datetime.now().year, 1950, -1))

app = Flask(__name__)

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interaction_logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", case_types=case_types, years=years)
@app.route("/fetch", methods=["POST"])
def fetch():
    case_type = request.form["case_type"]
    case_number = request.form["case_number"]
    case_year = request.form["case_year"]

    try:
        results = scrape_case(case_type, case_number, case_year)

        # Serialize results to JSON (ensure all objects are serializable)
        raw_response = json.dumps(results, default=str)

        # Create and add log entry
        log_entry = CaseQuery(
            case_type=case_type,
            case_number=case_number,
            case_year=case_year,
            raw_response=raw_response
        )

        db.session.add(log_entry)
        db.session.commit()

    except Exception as e:
        return render_template("index.html", results=[], error=str(e), case_types=case_types, years=years)

    return render_template("index.html", results=results, case_types=case_types, years=years)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
