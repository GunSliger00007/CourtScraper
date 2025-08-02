from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100))
    case_number = db.Column(db.String(20))
    case_year = db.Column(db.String(4))
    raw_response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<CaseQuery {self.case_type} {self.case_number}/{self.case_year}>'
