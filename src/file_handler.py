"""
File Handler Module
Handles CSV file reading and data validation for the reporting system.
"""

import pandas as pd
from typing import Tuple, List, Optional


def read_csv_file(file_path: str, required_columns: list) -> Tuple[bool, Optional[pd.DataFrame], Optional[str]]:
    """
    Read a CSV file and validate that it contains all required columns.
    
    Args:
        file_path: Path to the CSV file to read
        required_columns: List of column names that must be present in the CSV
        
    Returns:
        Tuple containing:
        - success (bool): True if file was read successfully, False otherwise
        - data (DataFrame or None): The loaded data if successful, None if failed
        - error_message (str or None): Error description if failed, None if successful
    """
    print(f"Reading file: {file_path}")
    
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        print(f"[OK] File loaded successfully. Found {len(df)} rows.")
        
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            error_msg = f"Missing required columns: {', '.join(missing_columns)}"
            print(f"[X] Validation failed: {error_msg}")
            return False, None, error_msg
        
        print(f"[OK] All required columns found: {', '.join(required_columns)}")
        
        # Handle missing data by filling NaN values with 0
        if df.isnull().any().any():
            print("[!] Found missing values (NaN). Filling with 0...")
            df = df.fillna(0)
            print("[OK] Missing values handled.")
        
        print("[OK] Data validation complete.")
        return True, df, None
        
    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        print(f"[X] Error: {error_msg}")
        return False, None, error_msg
        
    except PermissionError:
        error_msg = f"Permission denied: Cannot read {file_path}"
        print(f"[X] Error: {error_msg}")
        return False, None, error_msg
        
    except pd.errors.EmptyDataError:
        error_msg = f"File is empty: {file_path}"
        print(f"[X] Error: {error_msg}")
        return False, None, error_msg
        
    except pd.errors.ParserError as e:
        error_msg = f"Invalid CSV format: {str(e)}"
        print(f"[X] Error: {error_msg}")
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error reading file: {str(e)}"
        print(f"[X] Error: {error_msg}")
        return False, None, error_msg


def validate_data(df: pd.DataFrame, thresholds: dict) -> List[str]:
    """
    Validate data against defined thresholds and return warning messages.
    
    Args:
        df: DataFrame containing 'count', 'processed', and 'errors' columns
        thresholds: Dictionary with 'max_error_rate' and 'min_processing_rate' keys
        
    Returns:
        List of warning messages (empty list if all validations pass)
    """
    print("\nValidating data against thresholds...")
    warnings = []
    
    # Calculate total counts from the dataframe
    total_count = df['count'].sum()
    total_processed = df['processed'].sum()
    total_errors = df['errors'].sum()
    
    # Calculate error rate (percentage of errors out of total count)
    if total_count > 0:
        error_rate = (total_errors / total_count) * 100
    else:
        error_rate = 0
    
    # Calculate processing rate (percentage of processed out of total count)
    if total_count > 0:
        processing_rate = (total_processed / total_count) * 100
    else:
        processing_rate = 0
    
    print(f"  Error Rate: {error_rate:.1f}%")
    print(f"  Processing Rate: {processing_rate:.1f}%")
    
    # Check if error rate exceeds maximum threshold
    max_error_rate = thresholds.get('max_error_rate', 100)
    if error_rate > max_error_rate:
        warning = f"[!] WARNING: Error rate ({error_rate:.1f}%) exceeds threshold ({max_error_rate:.1f}%)"
        warnings.append(warning)
        print(warning)
    
    # Check if processing rate is below minimum threshold
    min_processing_rate = thresholds.get('min_processing_rate', 0)
    if processing_rate < min_processing_rate:
        warning = f"[!] WARNING: Processing rate ({processing_rate:.1f}%) is below threshold ({min_processing_rate:.1f}%)"
        warnings.append(warning)
        print(warning)
    
    # If no warnings, data passed all validations
    if not warnings:
        print("[OK] All validation checks passed.")
    
    return warnings

# Made with Bob
