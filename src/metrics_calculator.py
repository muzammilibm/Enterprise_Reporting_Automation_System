"""
Metrics Calculator Module
Calculates daily and month-to-date metrics from processed data.
"""

import pandas as pd
from typing import Dict


def calculate_daily_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate daily metrics from the dataframe.
    
    Args:
        df: DataFrame containing 'count', 'processed', and 'errors' columns
        
    Returns:
        Dictionary containing:
        - total_count: Sum of all counts
        - total_processed: Sum of all processed items
        - total_errors: Sum of all errors
        - processing_rate: Percentage of items processed (0-100)
        - error_rate: Percentage of errors (0-100)
    """
    print("\nCalculating daily metrics...")
    
    # Calculate totals by summing each column
    total_count = df['count'].sum()
    total_processed = df['processed'].sum()
    total_errors = df['errors'].sum()
    
    # Calculate processing rate (percentage of processed items)
    # Handle division by zero: if no items, rate is 0%
    if total_count > 0:
        processing_rate = (total_processed / total_count) * 100
    else:
        processing_rate = 0.0
    
    # Calculate error rate (percentage of errors)
    # Handle division by zero: if no items, rate is 0%
    if total_count > 0:
        error_rate = (total_errors / total_count) * 100
    else:
        error_rate = 0.0
    
    # Create metrics dictionary
    metrics = {
        'total_count': total_count,
        'total_processed': total_processed,
        'total_errors': total_errors,
        'processing_rate': processing_rate,
        'error_rate': error_rate
    }
    
    print(f"[OK] Daily metrics calculated:")
    print(f"  Total Count: {total_count:,.0f}")
    print(f"  Total Processed: {total_processed:,.0f}")
    print(f"  Total Errors: {total_errors:,.0f}")
    print(f"  Processing Rate: {processing_rate:.1f}%")
    print(f"  Error Rate: {error_rate:.1f}%")
    
    return metrics


def calculate_mtd_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate month-to-date (MTD) metrics from the dataframe.
    
    Args:
        df: DataFrame containing 'date', 'count', 'processed', and 'errors' columns
        
    Returns:
        Dictionary containing:
        - mtd_total_count: Month-to-date sum of all counts
        - mtd_total_processed: Month-to-date sum of all processed items
        - mtd_total_errors: Month-to-date sum of all errors
        - num_days: Number of unique days in the dataset
        - daily_average: Average count per day
        - processing_rate: Percentage of items processed (0-100)
        - error_rate: Percentage of errors (0-100)
    """
    print("\nCalculating month-to-date (MTD) metrics...")
    
    # Calculate MTD totals (same as daily totals but labeled as MTD)
    mtd_total_count = df['count'].sum()
    mtd_total_processed = df['processed'].sum()
    mtd_total_errors = df['errors'].sum()
    
    # Calculate number of unique days in the dataset
    # Convert date column to datetime if it's not already
    if 'date' in df.columns:
        num_days = df['date'].nunique()
    else:
        # If no date column, assume single day
        num_days = 1
    
    # Calculate daily average (total divided by number of days)
    # Handle division by zero: if no days, average is 0
    if num_days > 0:
        daily_average = mtd_total_count / num_days
    else:
        daily_average = 0.0
    
    # Calculate processing rate (percentage of processed items)
    if mtd_total_count > 0:
        processing_rate = (mtd_total_processed / mtd_total_count) * 100
    else:
        processing_rate = 0.0
    
    # Calculate error rate (percentage of errors)
    if mtd_total_count > 0:
        error_rate = (mtd_total_errors / mtd_total_count) * 100
    else:
        error_rate = 0.0
    
    # Create MTD metrics dictionary
    metrics = {
        'mtd_total_count': mtd_total_count,
        'mtd_total_processed': mtd_total_processed,
        'mtd_total_errors': mtd_total_errors,
        'num_days': num_days,
        'daily_average': daily_average,
        'processing_rate': processing_rate,
        'error_rate': error_rate
    }
    
    print(f"[OK] MTD metrics calculated:")
    print(f"  MTD Total Count: {mtd_total_count:,.0f}")
    print(f"  MTD Total Processed: {mtd_total_processed:,.0f}")
    print(f"  MTD Total Errors: {mtd_total_errors:,.0f}")
    print(f"  Number of Days: {num_days}")
    print(f"  Daily Average: {daily_average:,.0f}")
    print(f"  Processing Rate: {processing_rate:.1f}%")
    print(f"  Error Rate: {error_rate:.1f}%")
    
    return metrics


def format_metrics_for_display(daily_metrics: Dict[str, float], mtd_metrics: Dict[str, float]) -> str:
    """
    Format metrics into a readable string for console display.
    
    Args:
        daily_metrics: Dictionary of daily metrics from calculate_daily_metrics()
        mtd_metrics: Dictionary of MTD metrics from calculate_mtd_metrics()
        
    Returns:
        Multi-line formatted string ready for printing
    """
    print("\nFormatting metrics for display...")
    
    # Create a visually clear formatted output
    output = []
    output.append("\n" + "="*60)
    output.append("DAILY METRICS REPORT")
    output.append("="*60)
    
    # Daily metrics section
    output.append("\n[DAILY SUMMARY]:")
    output.append(f"  Total Count:        {daily_metrics['total_count']:>12,.0f}")
    output.append(f"  Total Processed:    {daily_metrics['total_processed']:>12,.0f}")
    output.append(f"  Total Errors:       {daily_metrics['total_errors']:>12,.0f}")
    output.append(f"  Processing Rate:    {daily_metrics['processing_rate']:>11.1f}%")
    output.append(f"  Error Rate:         {daily_metrics['error_rate']:>11.1f}%")
    
    # MTD metrics section
    output.append("\n[MONTH-TO-DATE (MTD) SUMMARY]:")
    output.append(f"  MTD Total Count:    {mtd_metrics['mtd_total_count']:>12,.0f}")
    output.append(f"  MTD Processed:      {mtd_metrics['mtd_total_processed']:>12,.0f}")
    output.append(f"  MTD Errors:         {mtd_metrics['mtd_total_errors']:>12,.0f}")
    output.append(f"  Number of Days:     {mtd_metrics['num_days']:>12,.0f}")
    output.append(f"  Daily Average:      {mtd_metrics['daily_average']:>12,.0f}")
    output.append(f"  Processing Rate:    {mtd_metrics['processing_rate']:>11.1f}%")
    output.append(f"  Error Rate:         {mtd_metrics['error_rate']:>11.1f}%")
    
    output.append("\n" + "="*60)
    
    # Join all lines with newline characters
    formatted_output = "\n".join(output)
    
    print("[OK] Metrics formatted successfully.")
    
    return formatted_output

# Made with Bob
