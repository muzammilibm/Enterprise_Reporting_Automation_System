# Enterprise Reporting Automation System

A Python-based automation system designed to streamline daily and monthly reporting processes. This system reads CSV data, calculates key metrics, generates formatted Excel reports, and delivers them via email—all with minimal manual intervention. Built as a 5-day intern project to demonstrate practical automation skills.

## Features

- **Automated CSV Data Processing** - Reads and validates input data with configurable column requirements
- **Metric Calculations** - Computes daily and month-to-date (MTD) statistics automatically
- **Excel Report Generation** - Creates professional multi-sheet Excel reports with formatted tables
- **Email Delivery with Retry Logic** - Sends reports to multiple recipients with automatic retry on failure
- **Data Validation** - Validates data quality against configurable thresholds (error rates, processing rates)
- **Error Logging** - Comprehensive error tracking and logging for troubleshooting
- **Test Data Generation** - Built-in tool to create realistic sample data for testing

## Project Structure

```
Enterprise_Reporting_Automation_System/
├── main.py                      # Main orchestration script - run this!
├── create_test_data.py          # Test data generator
├── config.yaml                  # Configuration file (paths, thresholds, email settings)
├── .env                         # Email credentials (gitignored - create from template)
├── .env.template                # Template for credentials setup
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── src/
│   ├── __init__.py             # Package initialization
│   ├── file_handler.py         # CSV reading and data validation
│   ├── metrics_calculator.py   # Daily and MTD metric calculations
│   ├── report_generator.py     # Excel report generation with formatting
│   └── email_sender.py         # Email functionality with SMTP
├── data/
│   ├── input/                  # Place input CSV files here
│   └── output/                 # Generated Excel reports saved here
└── logs/
    └── error.log               # Error and warning logs
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Office365 email account** - Required for email functionality (or any SMTP-compatible email service)

## Installation

Follow these steps to set up the project on your local machine:

```bash
# 1. Clone or download the repository
# If using git:
git clone <repository-url>
# Or download and extract the ZIP file

# 2. Navigate to the project directory
cd Enterprise_Reporting_Automation_System

# 3. (Optional but Recommended) Create a virtual environment
python -m venv .venv

# Activate the virtual environment:
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# 4. Install required dependencies
pip install -r requirements.txt
```

## Configuration

### 6.1 Email Credentials Setup

The system requires email credentials to send reports. Follow these steps:

```bash
# 1. Copy the template file to create your .env file
# On Windows:
copy .env.template .env
# On Linux/Mac:
cp .env.template .env

# 2. Edit the .env file with your actual credentials
# Open .env in any text editor and update:
SENDER_EMAIL=your-email@company.com
SENDER_PASSWORD=your-app-password
```

**⚠️ Important Security Note:**

- For **Office365/Outlook**, you MUST use an **app password**, not your regular account password
- Generate an app password here: [Microsoft Account Security](https://account.microsoft.com/security)
- Never commit your `.env` file to version control (it's already in `.gitignore`)
- Keep your credentials secure and don't share them

### 6.2 Configuration File (config.yaml)

The `config.yaml` file controls system behavior. Here's what each setting does:

```yaml
# Input/Output Configuration
input_file: "./data/input/report.csv"    # Path to your input CSV file
output_dir: "./data/output"              # Where Excel reports will be saved

# Required CSV columns - system will validate these exist
required_columns:
  - date          # Date column (YYYY-MM-DD format)
  - category      # Category name
  - count         # Total count
  - processed     # Successfully processed items
  - errors        # Error count

# Email Configuration
email:
  enabled: true   # Set to false to skip email sending (useful for testing)
  recipients:
    - manager@company.com    # Add or remove email addresses as needed
    - team@company.com
  smtp_server: "smtp.office365.com"  # SMTP server (Office365 default)
  smtp_port: 587                      # SMTP port (587 for TLS)
  
# Validation Thresholds
thresholds:
  max_error_rate: 10.0        # Maximum acceptable error rate (%)
  min_processing_rate: 90.0   # Minimum acceptable processing rate (%)
```

**Configuration Tips:**
- Set `email.enabled: false` during testing to avoid sending emails
- Adjust thresholds based on your business requirements
- For Gmail, use `smtp.gmail.com` and port `587`
- For other email providers, check their SMTP settings

## Usage

### 7.1 Generate Test Data

Before running the report for the first time, generate sample data:

```bash
python create_test_data.py
```

This creates a file `data/input/report.csv` with 30 days of realistic test data.

**What it does:**
- Generates 3-5 records per day for the last 30 days
- Creates data across multiple categories (API, Batch, Manual, Automated)
- Includes realistic counts and error rates
- Saves to the location specified in `config.yaml`

### 7.2 Run the Report

Once you have input data (either test data or real data), run the main script:

```bash
python main.py
```

The system will execute all steps automatically and show progress in the console.

### 7.3 Expected Output

When you run `python main.py`, you should see output like this:

```
==================================================
Starting Report Generation
==================================================

1. Reading input file...
   ✓ Loaded 120 rows

2. Calculating metrics...
   Daily Metrics (Latest Date: 2024-04-25):
   - Total Count: 450
   - Processed: 432
   - Errors: 18
   - Error Rate: 4.00%
   - Processing Rate: 96.00%
   
   MTD Metrics (Month: 2024-04):
   - Total Count: 3,250
   - Processed: 3,120
   - Errors: 130
   - Error Rate: 4.00%
   - Processing Rate: 96.00%

3. Validating data...
   ✓ All validation checks passed

4. Generating Excel report...
   ✓ Saved: report_20240425_143022.xlsx

5. Sending email...
   ✓ Email sent to 2 recipients

==================================================
✓ Report generation complete!
==================================================
```

## Input Data Format

The system expects a CSV file with the following structure:

```csv
date,category,count,processed,errors
2024-04-25,API,120,115,5
2024-04-25,Batch,85,82,3
2024-04-25,Manual,45,43,2
2024-04-24,API,110,105,5
2024-04-24,Batch,90,88,2
```

**Column Descriptions:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date` | String | Date in YYYY-MM-DD format | 2024-04-25 |
| `category` | String | Category name (any string) | API, Batch, Manual |
| `count` | Integer | Total count of items | 120 |
| `processed` | Integer | Successfully processed items | 115 |
| `errors` | Integer | Error count (should equal count - processed) | 5 |

**Important Notes:**
- The `date` column must be in `YYYY-MM-DD` format
- `errors` should equal `count - processed` for data consistency
- Multiple records can exist for the same date (different categories)
- All columns listed in `config.yaml` under `required_columns` must be present

## Output

The system produces the following outputs:

### Excel Report
- **Location:** `data/output/report_YYYYMMDD_HHMMSS.xlsx`
- **Naming:** Timestamped to prevent overwrites (e.g., `report_20240425_143022.xlsx`)
- **Contents:**
  - **Sheet 1: Daily Summary** - Latest day's metrics by category
  - **Sheet 2: MTD Summary** - Month-to-date metrics by category
  - **Sheet 3: Warnings** - Data quality warnings (only if validation issues found)

### Email
- Sent to all recipients listed in `config.yaml`
- Subject: "Daily Report - [Date]"
- Body: Summary of key metrics (daily and MTD)
- Attachment: The generated Excel report

### Logs
- **Location:** `logs/error.log`
- **Contents:** Errors and warnings with timestamps
- **Format:** `2024-04-25 14:30:22 - ERROR - Error message here`

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Config file not found"
**Error Message:** `Configuration file 'config.yaml' not found`

**Solution:**
- Ensure `config.yaml` exists in the project root directory
- Check that you're running the script from the correct directory
- Verify the file name is exactly `config.yaml` (case-sensitive on Linux/Mac)

---

#### Issue: "Missing credentials"
**Error Message:** `Missing email credentials. Please ensure SENDER_EMAIL and SENDER_PASSWORD are set`

**Solution:**
1. Create `.env` file from template: `copy .env.template .env` (Windows) or `cp .env.template .env` (Linux/Mac)
2. Open `.env` in a text editor
3. Replace `your-email@company.com` with your actual email
4. Replace `your-app-password` with your actual app password
5. Save the file

---

#### Issue: "SMTP Authentication failed"
**Error Message:** `SMTP Authentication Error` or `535 Authentication failed`

**Solution:**
- **Use an app password**, not your regular email password
- For Office365: Generate app password at [Microsoft Account Security](https://account.microsoft.com/security)
- For Gmail: Enable 2FA, then generate app password in [Google Account Settings](https://myaccount.google.com/apppasswords)
- Verify your email address is correct in `.env`
- Check that SMTP server and port are correct in `config.yaml`

---

#### Issue: "Input file not found"
**Error Message:** `Failed to read input file: [Errno 2] No such file or directory`

**Solution:**
1. Run `python create_test_data.py` to generate sample data
2. Or place your own CSV file at the path specified in `config.yaml` (`input_file` setting)
3. Verify the file path is correct (use forward slashes `/` or double backslashes `\\`)
4. Check that the `data/input/` directory exists

---

#### Issue: "Permission denied" when saving report
**Error Message:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
- Check that you have write permissions on the `data/output/` directory
- Close any Excel files with the same name that might be open
- On Windows, ensure the directory isn't read-only
- Try running your terminal/command prompt as administrator

---

#### Issue: Email not sending
**Symptoms:** Report generates successfully but email doesn't arrive

**Solution:**
1. Check your internet connection
2. Verify SMTP settings in `config.yaml` match your email provider:
   - Office365: `smtp.office365.com`, port `587`
   - Gmail: `smtp.gmail.com`, port `587`
   - Outlook: `smtp-mail.outlook.com`, port `587`
3. Check spam/junk folder for the email
4. Verify recipient email addresses are correct in `config.yaml`
5. For testing, set `email.enabled: false` in `config.yaml` to skip email sending

---

#### Issue: "Module not found" errors
**Error Message:** `ModuleNotFoundError: No module named 'pandas'` (or other module)

**Solution:**
1. Ensure you've installed dependencies: `pip install -r requirements.txt`
2. If using a virtual environment, make sure it's activated
3. Try upgrading pip: `python -m pip install --upgrade pip`
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Development Notes

This project is designed with simplicity and clarity in mind, making it ideal for interns and junior developers:

### Code Design Principles
- **Modular Architecture** - Each module (`file_handler`, `metrics_calculator`, etc.) handles a specific responsibility
- **Independent Components** - Modules can be tested and used separately
- **Clear Error Handling** - All functions use try-except blocks with descriptive error messages
- **Type Hints** - All functions include type hints for better code clarity
- **Comprehensive Docstrings** - Every function has detailed documentation
- **Progress Visibility** - Uses `print()` statements to show real-time progress

### Code Organization
- **src/** - Core business logic (reusable modules)
- **main.py** - Orchestration layer (coordinates all modules)
- **create_test_data.py** - Utility script (standalone tool)
- **config.yaml** - Configuration (no hardcoded values)
- **.env** - Secrets (never committed to version control)

### Best Practices Demonstrated
- Configuration management (YAML)
- Environment variables for secrets
- Logging for debugging
- Input validation
- Error handling
- Code documentation

## Testing

You can test individual components without running the full pipeline:

### Test Data Reading
```python
from src.file_handler import read_csv_file

# Test reading a CSV file
success, df, error = read_csv_file(
    "data/input/report.csv", 
    ["date", "category", "count", "processed", "errors"]
)

if success:
    print(f"Loaded {len(df)} rows")
    print(df.head())
else:
    print(f"Error: {error}")
```

### Test Metric Calculation
```python
from src.file_handler import read_csv_file
from src.metrics_calculator import calculate_daily_metrics, calculate_mtd_metrics

# Read data
success, df, _ = read_csv_file("data/input/report.csv", ["date", "count"])

if success:
    # Calculate metrics
    daily = calculate_daily_metrics(df)
    mtd = calculate_mtd_metrics(df)
    
    print("Daily Metrics:", daily)
    print("MTD Metrics:", mtd)
```

### Test Data Validation
```python
from src.file_handler import read_csv_file, validate_data

# Read data
success, df, _ = read_csv_file("data/input/report.csv", ["date", "count"])

if success:
    # Validate with thresholds
    thresholds = {
        'max_error_rate': 10.0,
        'min_processing_rate': 90.0
    }
    warnings = validate_data(df, thresholds)
    
    if warnings:
        print("Warnings found:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("All validation checks passed!")
```

### Test Report Generation
```python
from src.report_generator import generate_excel_report

# Sample metrics (replace with actual data)
daily_metrics = {
    'date': '2024-04-25',
    'total_count': 450,
    'total_processed': 432,
    'total_errors': 18
}

mtd_metrics = {
    'month': '2024-04',
    'total_count': 3250,
    'total_processed': 3120,
    'total_errors': 130
}

# Generate report
success, path, error = generate_excel_report(
    daily_metrics=daily_metrics,
    mtd_metrics=mtd_metrics,
    output_dir="./data/output",
    validation_warnings=[]
)

if success:
    print(f"Report saved: {path}")
else:
    print(f"Error: {error}")
```

## Future Enhancements

Potential improvements for future versions:

### Integration & Storage
- **SharePoint Integration** - Automatically upload reports to SharePoint document library
- **Database Support** - Store historical data in SQL database for trend analysis
- **Cloud Storage** - Save reports to AWS S3, Azure Blob Storage, or Google Cloud Storage

### Automation & Scheduling
- **Scheduled Execution** - Use Windows Task Scheduler or cron jobs for automatic daily runs
- **Multiple Report Templates** - Support different report formats for different audiences
- **Dynamic Scheduling** - Configure different schedules for daily, weekly, and monthly reports

### Notifications & Monitoring
- **Slack/Teams Notifications** - Send alerts to team channels instead of/in addition to email
- **Dashboard Integration** - Push metrics to monitoring dashboards (Grafana, Tableau)
- **Alert System** - Proactive alerts when thresholds are exceeded

### Features & Functionality
- **Web Dashboard** - Interactive web interface for viewing reports and trends
- **Historical Comparison** - Compare current metrics against previous periods
- **Custom Metrics** - Allow users to define custom calculations
- **Multi-format Export** - Support PDF, CSV, and JSON output formats
- **Data Visualization** - Add charts and graphs to Excel reports

### Quality & Performance
- **Unit Tests** - Comprehensive test suite with pytest
- **Performance Optimization** - Handle larger datasets more efficiently
- **Parallel Processing** - Process multiple reports simultaneously
- **Data Caching** - Cache frequently accessed data for faster processing

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Enterprise Reporting Automation System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact & Support

### Getting Help

If you encounter issues or have questions:

1. **Check the Troubleshooting section** above for common issues and solutions
2. **Review the logs** in `logs/error.log` for detailed error messages
3. **Verify your configuration** in `config.yaml` and `.env` files
4. **Test with sample data** using `create_test_data.py` to isolate issues

### Reporting Issues

When reporting an issue, please include:
- Error message (from console or `logs/error.log`)
- Steps to reproduce the problem
- Your Python version (`python --version`)
- Operating system (Windows, Linux, Mac)
- Relevant configuration (without sensitive credentials)

### Project Information

- **Project Type:** Intern Training Project (5-Day Sprint)
- **Purpose:** Demonstrate automation, Python best practices, and system integration
- **Skill Level:** Beginner to Intermediate
- **Estimated Setup Time:** 15-30 minutes
- **Estimated Learning Time:** 2-4 hours to understand all components

### Contributing

This is an educational project, but contributions are welcome! If you'd like to improve the system:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes with clear comments
4. Test thoroughly
5. Submit a pull request with a description of changes

---

**Built with ❤️ as an intern learning project**

*Last Updated: April 2024*