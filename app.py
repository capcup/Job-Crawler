from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(50), default='unknown')
    url = db.Column(db.String(2000), default='unknown')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Job %r>' % self.id 
    
def addJobs():
    title = 'Junior Softwareentwickler'
    new_jobs = Jobs(title=title)
    try:
        db.session.add(new_jobs)
        db.session.commit()
        return redirect('/')


@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)



