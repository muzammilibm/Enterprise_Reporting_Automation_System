"""
Main Orchestration Script for Enterprise Reporting Automation System

This script coordinates all modules and provides the end-to-end workflow
from data reading to email delivery. This is the entry point that users will run.

Author: Intern Project - Day 5 Integration
"""

import sys
import logging
from pathlib import Path
import yaml
from dotenv import load_dotenv
import os

from src.file_handler import read_csv_file, validate_data
from src.metrics_calculator import calculate_daily_metrics, calculate_mtd_metrics, format_metrics_for_display
from src.report_generator import generate_excel_report
from src.email_sender import send_email_with_report


def _setup_logging() -> None:
    """
    Configure Python logging to write to logs/error.log
    
    Creates the logs directory if it doesn't exist and sets up
    logging format with timestamp.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        filename='logs/error.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def _load_config() -> dict:
    """
    Load and return configuration from config.yaml
    
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config.yaml is not found
        yaml.YAMLError: If config.yaml is invalid
    """
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        raise FileNotFoundError(
            "Configuration file 'config.yaml' not found. "
            "Please ensure config.yaml exists in the project root."
        )
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing config.yaml: {e}")


def _load_credentials() -> tuple:
    """
    Load email credentials from .env file
    
    Returns:
        tuple: (sender_email, sender_password)
        
    Raises:
        ValueError: If required credentials are missing
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    # Validate that credentials exist
    if not sender_email or not sender_password:
        raise ValueError(
            "Missing email credentials. Please ensure SENDER_EMAIL and "
            "SENDER_PASSWORD are set in your .env file."
        )
    
    return sender_email, sender_password


def main() -> int:
    """
    Main orchestration function that coordinates the entire reporting workflow
    
    This function:
    1. Loads configuration and credentials
    2. Reads input CSV file
    3. Calculates metrics (daily and MTD)
    4. Validates data
    5. Generates Excel report
    6. Sends email (if enabled)
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Setup logging
    _setup_logging()
    
    try:
        # Print welcome banner
        print("=" * 50)
        print("Starting Report Generation")
        print("=" * 50)
        print()
        
        # Load configuration
        try:
            config = _load_config()
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"[X] Configuration Error: {e}")
            logging.error(f"Configuration Error: {e}")
            return 1
        
        # Load credentials only if email is enabled
        sender_email = None
        sender_password = None
        if config['email']['enabled']:
            try:
                sender_email, sender_password = _load_credentials()
            except ValueError as e:
                print(f"[X] Credentials Error: {e}")
                logging.error(f"Credentials Error: {e}")
                return 1
        
        # Step 1: Read input file
        print("1. Reading input file...")
        try:
            # Get required columns from config
            required_columns = config['required_columns']
            
            # Call read_csv_file with required parameters
            success, df, error_msg = read_csv_file(
                config['input_file'],
                required_columns
            )
            
            if not success or df is None:
                print(f"   [X] Failed to read input file: {error_msg}")
                logging.error(f"Failed to read input file: {error_msg}")
                return 1
            
            print(f"   [OK] Loaded {len(df)} rows")
            print()
        except Exception as e:
            print(f"   [X] Failed to read input file: {e}")
            logging.error(f"Failed to read input file: {e}")
            return 1
        
        # Step 2: Calculate metrics
        print("2. Calculating metrics...")
        try:
            # Calculate daily metrics
            daily_metrics = calculate_daily_metrics(df)
            
            # Calculate MTD metrics
            mtd_metrics = calculate_mtd_metrics(df)
            
            # Format and display metrics
            formatted_metrics = format_metrics_for_display(daily_metrics, mtd_metrics)
            for line in formatted_metrics:
                print(f"   {line}")
            print()
        except Exception as e:
            print(f"   [X] Failed to calculate metrics: {e}")
            logging.error(f"Failed to calculate metrics: {e}")
            return 1
        
        # Step 3: Validate data
        print("3. Validating data...")
        try:
            # Get validation thresholds from config
            thresholds = config['thresholds']
            
            # Call validate_data with required parameters
            warnings = validate_data(df, thresholds)
            
            if warnings:
                # Print warnings if any exist
                for warning in warnings:
                    print(f"   {warning}")
            else:
                # All validation checks passed
                print("   [OK] All validation checks passed")
            print()
        except Exception as e:
            print(f"   [X] Failed to validate data: {e}")
            logging.error(f"Failed to validate data: {e}")
            return 1
        
        # Step 4: Generate Excel report
        print("4. Generating Excel report...")
        try:
            # Call generate_excel_report with correct parameters
            success, report_path, error_msg = generate_excel_report(
                daily_metrics=daily_metrics,
                mtd_metrics=mtd_metrics,
                output_dir=config['output_dir'],
                validation_warnings=warnings
            )
            
            if not success or report_path is None:
                print(f"   [X] Failed to generate Excel report: {error_msg}")
                logging.error(f"Failed to generate Excel report: {error_msg}")
                return 1
            
            # Extract just the filename for display
            report_filename = os.path.basename(report_path)
            print(f"   [OK] Saved: {report_filename}")
            print()
        except Exception as e:
            print(f"   [X] Failed to generate Excel report: {e}")
            logging.error(f"Failed to generate Excel report: {e}")
            return 1
        
        # Step 5: Send email (if enabled)
        if config['email']['enabled']:
            print("5. Sending email...")
            try:
                # Call send_email_with_report with correct parameters
                success, error_msg = send_email_with_report(
                    report_file_path=report_path,
                    daily_metrics=daily_metrics,
                    mtd_metrics=mtd_metrics,
                    config=config,
                    sender_email=sender_email,
                    sender_password=sender_password
                )
                
                if not success:
                    # Log warning but don't fail the whole process
                    print(f"   [!] Failed to send email: {error_msg}")
                    logging.warning(f"Failed to send email: {error_msg}")
                else:
                    recipient_count = len(config['email']['recipients'])
                    print(f"   [OK] Email sent to {recipient_count} recipient{'s' if recipient_count > 1 else ''}")
                print()
            except Exception as e:
                # Log warning but don't fail the whole process
                print(f"   [!] Failed to send email: {e}")
                logging.warning(f"Failed to send email: {e}")
                print()
        else:
            print("5. Email sending disabled (skipped)")
            print()
        
        # Print completion banner
        print("=" * 50)
        print("[OK] Report generation complete!")
        print("=" * 50)
        
        return 0
        
    except KeyboardInterrupt:
        # Handle user interruption gracefully
        print("\n\nInterrupted by user")
        logging.info("Process interrupted by user")
        return 1
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"\n[X] Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    # Run main function and exit with its return code
    sys.exit(main())

# Made with Bob
