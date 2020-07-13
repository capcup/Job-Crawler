from flask import Flask, render_template, request, redirect
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
    filtered = db.Column(db.Boolean, default=True)
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
    except: 
        return 'There was an issue adding a job'

@app.route('/', methods=['POST', 'GET'])
def index():
    jobs = Jobs.query.filter_by(filtered=True).order_by(Jobs.date_created).all()
    # jobs = Jobs.query.order_by(Jobs.date_created).all()
    
    if request.method == 'POST':
        job_title = request.form['title']
        job_company = request.form['company']
        job_url = request.form['url']

        if job_title or job_company or job_url: 
            new_job = Jobs(title=job_title, company=job_company, url=job_url)
            try: 
                db.session.add(new_job)
                db.session.commit()
                return redirect('/')

            except:
                return 'There was an issue adding a new job'
        else: 
            return render_template('index.html', jobs = jobs)
    else:
        return render_template('index.html', jobs = jobs)

@app.route('/delete/<int:id>')
def delete(id):
    deleted_job = Jobs.query.get_or_404(id)

    try: 
        db.session.delete(deleted_job)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that job'

@app.route('/filter/<int:id>')
def filter(id):
    filtered_job = Jobs.query.get_or_404(id)
    try: 
        filtered_job.filtered = not filtered_job.filtered
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem filtering that job'



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    job = Jobs.query.get_or_404(id)

    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']        
        job.url = request.form['url']       

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the job'
    else:
        return render_template('update.html', job=job)


if __name__=="__main__":
    app.run(debug=True)



