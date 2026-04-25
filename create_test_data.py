"""
Test Data Generator for Reporting Automation System

This script generates sample CSV data for testing the reporting system.
It creates realistic-looking data with dates, categories, counts, and error rates.

Usage:
    python create_test_data.py
    
Or import and use in code:
    from create_test_data import generate_test_data
    generate_test_data(num_days=15, output_file="./data/input/test.csv")
"""

import random
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path


def _generate_daily_records(date_str: str) -> list:
    """
    Generate 3-5 records for a single day.
    
    This helper function creates multiple records for different categories
    on the same day, with realistic count and error values.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        List of dictionaries containing record data
    """
    # Available categories for the records
    categories = ["API", "Batch", "Manual", "Automated"]
    
    # Randomly select 3-5 categories (some days might have all 4, some might have 3)
    num_records = random.randint(3, 5)
    selected_categories = random.sample(categories, min(num_records, len(categories)))
    
    # If we need more than 4 records, duplicate some categories
    if num_records > len(categories):
        selected_categories.extend(random.sample(categories, num_records - len(categories)))
    
    records = []
    
    # Generate a record for each selected category
    for category in selected_categories:
        # Generate random count between 50 and 150
        count = random.randint(50, 150)
        
        # Generate errors (0-10% error rate, so 0-15 errors)
        errors = random.randint(0, 15)
        
        # Ensure errors don't exceed count
        errors = min(errors, count)
        
        # Calculate processed (count minus errors)
        processed = count - errors
        
        # Create the record
        record = {
            'date': date_str,
            'category': category,
            'count': count,
            'processed': processed,
            'errors': errors
        }
        
        records.append(record)
    
    return records


def generate_test_data(num_days: int = 30, output_file: str = "./data/input/report.csv") -> None:
    """
    Generate sample CSV data for testing the reporting system.
    
    This function creates realistic test data with multiple records per day,
    covering different categories with varying counts and error rates.
    
    Args:
        num_days: Number of days of data to generate (default: 30)
        output_file: Path where the CSV file will be saved (default: ./data/input/report.csv)
        
    Returns:
        None
        
    Example:
        >>> generate_test_data(num_days=15, output_file="./data/input/test.csv")
        Generates 15 days of test data and saves to test.csv
    """
    print("=" * 50)
    print("Generating Test Data")
    print("=" * 50)
    print()
    
    # Start from today and go backwards
    end_date = datetime.now()
    
    print(f"Generating data for {num_days} days...")
    
    # List to store all records
    all_records = []
    
    # Generate data for each day
    for day_offset in range(num_days):
        # Calculate the date (going backwards from today)
        current_date = end_date - timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Generate 3-5 records for this day
        daily_records = _generate_daily_records(date_str)
        all_records.extend(daily_records)
    
    # Calculate average records per day
    avg_records = len(all_records) / num_days
    print(f"[OK] Generated {len(all_records)} records ({avg_records:.1f} per day average)")
    print()
    
    # Create DataFrame from all records
    df = pd.DataFrame(all_records)
    
    # Sort by date (most recent first)
    df = df.sort_values('date', ascending=False).reset_index(drop=True)
    
    # Ensure output directory exists
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving to: {output_file}")
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print("[OK] Test data saved successfully!")
        print()
        
        # Show sample data preview
        print("Sample data preview:")
        print(df.head().to_string())
        print()
        
        print("=" * 50)
        print("[OK] Test data generation complete!")
        print("=" * 50)
        print()
        print("You can now run: python main.py")
        
    except Exception as e:
        print(f"[ERROR] Error saving test data: {e}")
        print("Please check that the output directory is writable.")
        raise


if __name__ == "__main__":
    # When run as a script, generate 30 days of test data
    # to the default location
    generate_test_data()

# Made with Bob
