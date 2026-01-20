# Job Alert Flask Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

A modern, open-source Flask web application that monitors Google Jobs RSS feeds and displays product manager and product marketing job opportunities. Originally converted from an n8n workflow, this application features a beautiful Tailwind CSS interface and automated job monitoring capabilities.

**Discover more AI tools at [AI KAPTAN](https://www.aikaptan.com/) - Your gateway to the best AI tools and resources.**

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## ✨ Features

- 🔄 **Automatic Job Fetching**: Fetches jobs from Google Jobs RSS feed every 5 minutes using APScheduler
- 🔍 **Smart Keyword Filtering**: Automatically filters jobs containing keywords like "Product manager", "product marketing", and "product"
- 🎯 **Intelligent Deduplication**: Prevents duplicate job listings using database URL checks
- 📱 **Modern Responsive UI**: Beautiful, mobile-friendly design with Tailwind CSS and smooth animations
- 📊 **Real-time Statistics**: Live job count and statistics displayed on the dashboard
- 🔄 **Manual Refresh**: One-click button to manually trigger job fetching
- 📄 **Pagination**: Easy navigation through job listings with 20 jobs per page
- 🗄️ **SQLite Database**: Lightweight, file-based database for easy setup and portability
- 🧹 **HTML Tag Cleaning**: Automatically strips HTML tags from job titles and company names
- 🔗 **Direct Apply Links**: Quick access to job application pages
- ⏰ **Timestamp Tracking**: Shows when each job was discovered

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **Git** - For cloning the repository (optional)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "job alert"
```

Or download and extract the ZIP file to your desired location.

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates the project dependencies:

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 - Web framework
- Flask-SQLAlchemy 3.1.1 - Database ORM
- APScheduler 3.10.4 - Background job scheduler
- feedparser 6.0.10 - RSS feed parser
- Werkzeug 3.0.1 - WSGI utilities

## ⚙️ Configuration

The application can be configured using environment variables. You can set these in your shell or create a `.env` file (requires `python-dotenv` package).

### Available Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `RSS_FEED_URL` | Google Jobs RSS feed URL | Pre-configured feed URL |
| `DATABASE_URL` | Database connection string | `sqlite:///jobs.db` |
| `PORT` | Port to run the application | `3000` |
| `SLACK_WEBHOOK_URL` | Optional Slack webhook for notifications | Empty (disabled) |

### Configuration Examples

**Using environment variables:**

```bash
# macOS/Linux
export RSS_FEED_URL="https://www.google.co.in/alerts/feeds/YOUR_FEED_ID"
export PORT=8080
export DATABASE_URL="sqlite:///custom_jobs.db"

# Windows (Command Prompt)
set RSS_FEED_URL=https://www.google.co.in/alerts/feeds/YOUR_FEED_ID
set PORT=8080

# Windows (PowerShell)
$env:RSS_FEED_URL="https://www.google.co.in/alerts/feeds/YOUR_FEED_ID"
$env:PORT=8080
```

**Getting Your Google Jobs RSS Feed URL:**

1. Go to [Google Alerts](https://www.google.com/alerts)
2. Create a new alert for job searches (e.g., "product manager jobs")
3. Set the delivery method to "RSS feed"
4. Copy the RSS feed URL from the feed settings

## 🏃 Running the Application

### Step 1: Check Port Availability

Before running, ensure the port is free:

```bash
# Check if port 3000 is in use
lsof -i :3000

# If a process is using the port, kill it (replace <PID> with the actual process ID)
kill -9 <PID>

# On Windows, use:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Step 2: Run the Application

```bash
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:3000
 * Debug mode: on
Processed X new jobs at YYYY-MM-DD HH:MM:SS
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:3000
```

The application will:
- Automatically create the database on first run
- Fetch jobs immediately on startup
- Start the background scheduler for automatic updates

## 💻 Usage

### Web Interface

1. **View Jobs**: Browse all available jobs on the main page
2. **Refresh Jobs**: Click the "Refresh Jobs" button to manually fetch new jobs
3. **View Statistics**: See total job count in the header
4. **Apply for Jobs**: Click "Apply Now" to open the job posting in a new tab
5. **Navigate Pages**: Use pagination controls at the bottom to browse through pages

### API Usage

The application provides RESTful API endpoints for programmatic access:

```bash
# Get all jobs (paginated)
curl http://localhost:3000/api/jobs?page=1&per_page=20

# Get statistics
curl http://localhost:3000/api/stats

# Manually refresh jobs
curl http://localhost:3000/refresh
```

## 🔌 API Endpoints

### `GET /`
Main page displaying all job listings with pagination.

**Query Parameters:**
- `page` (optional): Page number (default: 1)

**Example:** `http://localhost:3000/?page=2`

### `GET /api/jobs`
Returns jobs in JSON format.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20)

**Response:**
```json
{
  "jobs": [
    {
      "id": 1,
      "job_title": "Senior Product Manager",
      "company": "Tech Corp",
      "job_url": "https://...",
      "apply_link": "https://...",
      "source": "Google Jobs",
      "created_at": "2026-01-01T12:00:00"
    }
  ],
  "total": 150,
  "pages": 8,
  "current_page": 1
}
```

### `GET /api/stats`
Returns statistics about stored jobs.

**Response:**
```json
{
  "total_jobs": 150,
  "unique_companies": 45
}
```

### `GET /refresh`
Manually triggers job fetching from the RSS feed.

**Response:**
```json
{
  "status": "success",
  "message": "Jobs refreshed successfully"
}
```

### `GET /clean`
Cleans HTML tags from existing jobs in the database (useful for maintenance).

**Response:**
```json
{
  "status": "success",
  "message": "Jobs cleaned successfully"
}
```

## 📁 Project Structure

```
job alert/
├── app.py                    # Main Flask application and business logic
├── templates/
│   └── index.html           # Main HTML template with Tailwind CSS
├── requirements.txt          # Python dependencies
├── LICENSE                  # MIT License
├── README.md                # This file
├── Job_Alert.json           # Original n8n workflow configuration
├── .gitignore               # Git ignore rules
└── jobs.db                  # SQLite database (created automatically)
```

### File Descriptions

- **app.py**: Contains all Flask routes, database models, job fetching logic, and scheduler configuration
- **templates/index.html**: Frontend template with responsive design, JavaScript for stats updates, and job display
- **requirements.txt**: Lists all Python package dependencies with versions
- **Job_Alert.json**: Original n8n workflow export (for reference)

## 🔧 How It Works

### Architecture Overview

1. **Initialization**: On startup, the application:
   - Creates the SQLite database and tables if they don't exist
   - Cleans HTML tags from existing jobs
   - Fetches jobs immediately
   - Starts the background scheduler

2. **Scheduled Job Fetching** (Every 5 minutes):
   - Fetches RSS feed from Google Jobs
   - Parses feed entries using `feedparser`
   - Filters jobs by keywords
   - Normalizes job data (extracts title and company)
   - Checks for duplicates in database
   - Stores new jobs

3. **Job Processing Pipeline**:
   ```
   RSS Feed → Parse → Filter Keywords → Normalize → Deduplicate → Store → Display
   ```

4. **Data Flow**:
   - RSS entries are parsed and cleaned
   - Job titles are checked against keyword list
   - Titles are split to extract company names
   - URLs are checked against database for duplicates
   - New jobs are committed to database

5. **Web Interface**:
   - Flask renders jobs from database
   - Tailwind CSS provides modern styling
   - JavaScript updates statistics every 30 seconds
   - Pagination handles large job lists

## 🎨 Customization

### Change Keywords

Edit the `KEYWORDS` list in `app.py` (around line 18):

```python
KEYWORDS = [
    'Product manager',
    'product marketing',
    'product',
    'your custom keyword',
    'another keyword'
]
```

Keywords are case-insensitive and use substring matching.

### Change Fetch Interval

Modify the scheduler configuration in `app.py` (around line 158):

```python
scheduler.add_job(
    func=fetch_and_process_jobs,
    trigger="interval",
    minutes=10,  # Change from 5 to 10 minutes
    id='fetch_jobs',
    name='Fetch jobs from RSS feed every 10 minutes',
    replace_existing=True
)
```

### Change Jobs Per Page

Edit the pagination setting in the `index()` function (around line 172):

```python
per_page = 30  # Change from 20 to 30
```

### Customize UI Colors

Edit `templates/index.html` and modify Tailwind CSS classes. The current color scheme uses:
- Primary: Indigo (`indigo-600`, `indigo-700`)
- Background: Blue gradient (`from-blue-50 to-indigo-100`)
- Accents: Blue and green badges

### Add Slack Notifications

1. Set the `SLACK_WEBHOOK_URL` environment variable
2. Add Slack notification code in `fetch_and_process_jobs()` function
3. Send notifications when new jobs are found

## 🗄️ Database Management

### Database Schema

The `Job` model has the following structure:

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `job_title` | String(500) | Job title |
| `company` | String(200) | Company name |
| `job_url` | String(1000) | Unique job URL |
| `apply_link` | String(1000) | Application link |
| `source` | String(100) | Source (default: "Google Jobs") |
| `created_at` | DateTime | When job was added |

### Backup Database

```bash
# Copy the database file
cp jobs.db jobs_backup.db
```

### Reset Database

```bash
# Delete the database file (it will be recreated on next run)
rm jobs.db
```

### View Database

You can use SQLite command-line tool or a GUI like [DB Browser for SQLite](https://sqlitebrowser.org/):

```bash
sqlite3 jobs.db
.tables
SELECT * FROM job LIMIT 10;
```

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find the process using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=3001
python app.py
```

### No Jobs Appearing

1. **Check RSS Feed URL**: Verify the `RSS_FEED_URL` is correct and accessible
2. **Check Keywords**: Ensure your keywords match job titles in the feed
3. **Check Logs**: Look for error messages in the console
4. **Manual Refresh**: Try clicking the "Refresh Jobs" button
5. **Database**: Check if `jobs.db` exists and has data

### Database Errors

**Error:** `OperationalError: unable to open database file`

**Solution:**
- Check file permissions
- Ensure the directory is writable
- Try specifying an absolute path: `export DATABASE_URL="sqlite:////absolute/path/to/jobs.db"`

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Jobs Not Updating

1. Check if scheduler is running (look for periodic log messages)
2. Verify the RSS feed URL is still valid
3. Check network connectivity
4. Review console for error messages

## 🤝 Contributing

This is an open-source project, and contributions are welcome! Here's how you can help:

1. **Fork the Repository**: Create your own copy of the project
2. **Create a Branch**: Make a feature branch for your changes
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Ensure your changes work correctly
5. **Submit a Pull Request**: Share your improvements with the community

### Contribution Ideas

- Add support for multiple RSS feeds
- Implement email notifications
- Add job search/filter functionality
- Create Docker containerization
- Add unit tests
- Improve error handling
- Add job expiration/archival
- Implement user authentication
- Add job bookmarking/favorites

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## 🛠️ Technologies Used

- **[Flask 3.0.0](https://flask.palletsprojects.com/)** - Lightweight Python web framework
- **[Flask-SQLAlchemy 3.1.1](https://flask-sqlalchemy.palletsprojects.com/)** - SQL toolkit and ORM
- **[APScheduler 3.10.4](https://apscheduler.readthedocs.io/)** - Advanced Python Scheduler for background tasks
- **[feedparser 6.0.10](https://feedparser.readthedocs.io/)** - Universal feed parser for RSS and Atom feeds
- **[Werkzeug 3.0.1](https://werkzeug.palletsprojects.com/)** - WSGI utilities library
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework (via CDN)
- **[Font Awesome](https://fontawesome.com/)** - Icon library (via CDN)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive open-source license that allows you to:
- ✅ Use the software commercially
- ✅ Modify the software
- ✅ Distribute the software
- ✅ Use privately
- ✅ Sublicense

The only requirement is to include the original copyright and license notice.

## 🙏 Acknowledgments

- **Google Jobs** - For providing RSS feed functionality
- **n8n** - Original workflow inspiration
- **Flask Community** - For the excellent web framework
- **[AI KAPTAN](https://www.aikaptan.com/)** - For discovering and showcasing the best AI tools and resources

## 🔗 Related Resources

- [AI KAPTAN](https://www.aikaptan.com/) - Discover the best AI tools and resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Alerts](https://www.google.com/alerts) - Set up job alerts
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the code comments in `app.py`
3. Open an issue on the repository (if available)
4. Check the application logs for error messages

---

**Made with ❤️ for the open-source community**

*Discover more amazing AI tools at [AI KAPTAN](https://www.aikaptan.com/)*
