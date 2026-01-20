from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import feedparser
import re
import atexit
import os
from html import unescape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Keywords to filter jobs
KEYWORDS = ['Product manager', 'product marketing', 'product']
RSS_FEED_URL = os.getenv('RSS_FEED_URL', 'https://www.google.co.in/alerts/feeds/04915236839896086991/5551691188256910506')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')  # Optional Slack integration


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(500), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    job_url = db.Column(db.String(1000), unique=True, nullable=False)
    apply_link = db.Column(db.String(1000), nullable=False)
    source = db.Column(db.String(100), default='Google Jobs')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company': self.company,
            'job_url': self.job_url,
            'apply_link': self.apply_link,
            'source': self.source,
            'created_at': self.created_at.isoformat()
        }


def strip_html_tags(text):
    """Remove HTML tags from text"""
    if not text:
        return text
    # First unescape HTML entities
    text = unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def normalize_job_data(title, link):
    """Extract job title and company from RSS title"""
    # Strip HTML tags from title
    title = strip_html_tags(title)
    
    if ' - ' in title:
        parts = title.split(' - ')
        job_title = ' - '.join(parts[:-1]).strip()
        company = parts[-1].replace(' Careers', '').strip()
    else:
        job_title = title
        company = 'Unknown'
    
    # Clean up company name as well
    company = strip_html_tags(company)
    
    return {
        'job_title': job_title,
        'company': company,
        'job_url': link,
        'apply_link': link,
        'source': 'Google Jobs'
    }


def filter_by_keywords(title):
    """Check if job title contains any of the keywords"""
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in KEYWORDS)


def clean_existing_jobs():
    """Clean HTML tags from existing jobs in the database"""
    try:
        jobs = Job.query.all()
        cleaned_count = 0
        for job in jobs:
            original_title = job.job_title
            original_company = job.company
            
            cleaned_title = strip_html_tags(job.job_title)
            cleaned_company = strip_html_tags(job.company)
            
            if original_title != cleaned_title or original_company != cleaned_company:
                job.job_title = cleaned_title
                job.company = cleaned_company
                cleaned_count += 1
        
        if cleaned_count > 0:
            db.session.commit()
            print(f"Cleaned HTML tags from {cleaned_count} existing jobs")
    except Exception as e:
        print(f"Error cleaning existing jobs: {str(e)}")
        db.session.rollback()


def fetch_and_process_jobs():
    """Fetch jobs from RSS feed, filter, and store in database"""
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        new_jobs_count = 0
        
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            
            # Strip HTML tags for keyword filtering
            clean_title = strip_html_tags(title)
            
            # Filter by keywords
            if not filter_by_keywords(clean_title):
                continue
            
            # Normalize job data
            job_data = normalize_job_data(title, link)
            
            # Deduplicate - check if job URL already exists
            existing_job = Job.query.filter_by(job_url=job_data['job_url']).first()
            if existing_job:
                continue
            
            # Create new job entry
            job = Job(
                job_title=job_data['job_title'],
                company=job_data['company'],
                job_url=job_data['job_url'],
                apply_link=job_data['apply_link'],
                source=job_data['source']
            )
            
            db.session.add(job)
            new_jobs_count += 1
        
        db.session.commit()
        print(f"Processed {new_jobs_count} new jobs at {datetime.utcnow()}")
        
    except Exception as e:
        print(f"Error fetching jobs: {str(e)}")
        db.session.rollback()


# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=fetch_and_process_jobs,
    trigger="interval",
    minutes=5,
    id='fetch_jobs',
    name='Fetch jobs from RSS feed every 5 minutes',
    replace_existing=True
)


@app.route('/')
def index():
    """Main page showing all jobs"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    jobs = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('index.html', jobs=jobs)


@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get jobs as JSON"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    jobs = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'jobs': [job.to_dict() for job in jobs.items],
        'total': jobs.total,
        'pages': jobs.pages,
        'current_page': page
    })


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    total_jobs = Job.query.count()
    unique_companies = db.session.query(Job.company).distinct().count()
    
    return jsonify({
        'total_jobs': total_jobs,
        'unique_companies': unique_companies
    })


@app.route('/refresh')
def refresh_jobs():
    """Manual trigger to fetch jobs"""
    fetch_and_process_jobs()
    return jsonify({'status': 'success', 'message': 'Jobs refreshed successfully'})


@app.route('/clean')
def clean_jobs():
    """Manual trigger to clean HTML tags from existing jobs"""
    clean_existing_jobs()
    return jsonify({'status': 'success', 'message': 'Jobs cleaned successfully'})


def main():
    """Main entry point for the application"""
    with app.app_context():
        db.create_all()
        # Clean existing jobs to remove HTML tags
        clean_existing_jobs()
        # Fetch jobs immediately on startup
        fetch_and_process_jobs()
    
    scheduler.start()
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    port = int(os.getenv('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)


if __name__ == '__main__':
    main()
    
