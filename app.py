from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Submit AJAX Forms with jquery: https://www.youtube.com/watch?v=IZWtHsM3Y5A
# Flask: https://youtu.be/Z1RJmh_OqeA?t=1837


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
    except: 
        return 'There was an issue adding a job'

@app.route('/', methods=['POST', 'GET'])
def index():
    jobs = Jobs.query.order_by(Jobs.date_created).all()
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
    job_to_delete = Jobs.query.get_or_404(id)

    try: 
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


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
    # addJobs()
    app.run(debug=True)



