# Quick Start Guide

Get the Enterprise Reporting Automation System running in 5 minutes!

This guide will help you generate your first automated report with minimal setup. Perfect for absolute beginners who want to see the system in action quickly.

---

## Step 1: Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

**What this does:** Installs all required Python packages (pandas, openpyxl, pyyaml, python-dotenv)

**Expected output:** You should see packages being downloaded and installed successfully.

---

## Step 2: Generate Test Data

Run the test data generator to create sample CSV data:

```bash
python create_test_data.py
```

**What this does:** Creates a file `data/input/report.csv` with 30 days of realistic test data

**Expected output:**
```
==================================================
Generating Test Data
==================================================

Generating data for 30 days...
[OK] Generated 118 records (3.9 per day average)

Saving to: ./data/input/report.csv
[OK] Test data saved successfully!
```

---

## Step 3: Configure Email (Optional)

**For testing, you can skip this step!** Email is disabled by default in `config.yaml`.

If you want to enable email sending later:

1. Copy the template file:
   ```bash
   # Windows:
   copy .env.template .env
   
   # Linux/Mac:
   cp .env.template .env
   ```

2. Edit `.env` file with your email credentials:
   ```
   SENDER_EMAIL=your-email@company.com
   SENDER_PASSWORD=your-app-password
   ```

3. Enable email in `config.yaml`:
   ```yaml
   email:
     enabled: true  # Change from false to true
   ```

**Note:** For Office365/Outlook, you must use an app password, not your regular password.

---

## Step 4: Run the Report

Execute the main script to generate your first report:

```bash
python main.py
```

**What this does:** 
- Reads the CSV data
- Calculates daily and month-to-date metrics
- Validates data quality
- Generates a formatted Excel report
- (Optionally) Sends email with the report

**Expected output:**
```
==================================================
Starting Report Generation
==================================================

1. Reading input file...
   [OK] Loaded 118 rows

2. Calculating metrics...
   [OK] Daily metrics calculated
   [OK] MTD metrics calculated

3. Validating data...
   [OK] All validation checks passed

4. Generating Excel report...
   [OK] Saved: report_20260425_170128.xlsx

5. Email sending disabled (skipped)

==================================================
[OK] Report generation complete!
==================================================
```

---

## Step 5: View Your Report

Your Excel report is saved in the `data/output/` directory!

**To find it:**

1. Navigate to the `data/output/` folder in your project directory
2. Look for a file named `report_YYYYMMDD_HHMMSS.xlsx` (with today's date and time)
3. Open it in Microsoft Excel or any spreadsheet application

**What's inside:**
- **Sheet 1: Daily Summary** - Today's metrics breakdown
- **Sheet 2: MTD Summary** - Month-to-date aggregated metrics
- **Sheet 3: Warnings** - Data quality warnings (if any)

---

## 🎉 Congratulations!

You've successfully generated your first automated report! The system:
- ✅ Read and validated CSV data
- ✅ Calculated key metrics automatically
- ✅ Generated a professional Excel report
- ✅ Completed without errors

---

## Next Steps

Now that you have the basics working, explore more features:

1. **Use Your Own Data**
   - Replace `data/input/report.csv` with your own CSV file
   - Ensure it has the required columns: date, category, count, processed, errors

2. **Customize Settings**
   - Edit `config.yaml` to adjust validation thresholds
   - Change input/output file paths
   - Add more email recipients

3. **Enable Email Delivery**
   - Follow Step 3 above to configure email credentials
   - Test email sending with real SMTP settings

4. **Schedule Automation**
   - Set up Windows Task Scheduler (Windows) or cron (Linux/Mac)
   - Run the report automatically every day

5. **Learn More**
   - Read the full [README.md](README.md) for detailed documentation
   - Check [TEST_RESULTS.md](TEST_RESULTS.md) for testing details
   - Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical overview

---

## Troubleshooting

**Problem: "Module not found" error**
- Solution: Run `pip install -r requirements.txt` again

**Problem: "File not found" error**
- Solution: Make sure you ran `python create_test_data.py` first

**Problem: Report not generating**
- Solution: Check `logs/error.log` for detailed error messages

**Problem: Need help**
- Solution: See the full troubleshooting section in [README.md](README.md)

---

## Quick Reference Commands

```bash
# Generate test data
python create_test_data.py

# Run the report
python main.py

# View generated reports (Windows)
dir data\output

# View generated reports (Linux/Mac)
ls data/output

# Check error logs
type logs\error.log    # Windows
cat logs/error.log     # Linux/Mac
```

---

**Ready for more?** Check out the complete [README.md](README.md) for advanced features and configuration options!