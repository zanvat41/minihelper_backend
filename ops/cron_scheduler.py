"""
Simple Windows-compatible cron scheduler
Runs the report_by_mail job every minute
"""

import os
import sys
import time
import logging
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minihelper_backend.settings')

try:
    import django
    django.setup()
    
    # Import the cron job
    from cron.jobs import report_by_mail
    
    # Setup logging with UTF-8 encoding for Windows
    import sys
    
    # Create file handler with UTF-8 encoding
    file_handler = logging.FileHandler('cron_scheduler.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Create console handler that handles Unicode properly
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Set formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )
    logger = logging.getLogger(__name__)
    
    def run_cron_job():
        """Run the report_by_mail job"""
        try:
            print("Starting report_by_mail job...")  # Use print to avoid encoding issues
            logger.info("Starting report_by_mail job...")
            report_by_mail()
            print("report_by_mail job completed successfully")
            logger.info("report_by_mail job completed successfully")
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error in logging: {e}")
            print("Job may have completed but logging failed")
        except Exception as e:
            print(f"report_by_mail job failed: {e}")
            logger.error(f"report_by_mail job failed: {str(e)}")
    
    def main():
        """Main scheduler loop - runs every minute"""
        print("Cron scheduler started - running report_by_mail every minute")
        print("Press Ctrl+C to stop")
        
        try:
            logger.info("Cron scheduler started")
        except:
            pass  # Ignore logging errors during startup
        
        try:
            while True:
                current_time = datetime.now()
                time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"Running job at {time_str}")
                
                run_cron_job()
                
                # Wait for 60 seconds (1 minute)
                print("Waiting 60 seconds until next run...")
                print("-" * 50)
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
            try:
                logger.info("Scheduler stopped by user")
            except:
                pass
        except Exception as e:
            print(f"Scheduler error: {e}")
            try:
                logger.error(f"Scheduler error: {str(e)}")
            except:
                pass
    
    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the correct directory and Django is properly configured")
except Exception as e:
    print(f"Setup error: {e}")