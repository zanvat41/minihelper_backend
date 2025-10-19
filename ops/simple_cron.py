"""
Simple Windows cron scheduler for report_by_mail
Runs every minute without complex logging to avoid Unicode issues
"""

import os
import sys
import time
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
    
    def run_job():
        """Run the report_by_mail job"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting report_by_mail...")
            report_by_mail()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Job completed successfully!")
            return True
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Job failed: {e}")
            return False
    
    def main():
        """Main scheduler - runs every minute"""
        print("=" * 60)
        print("Django Cron Scheduler Started")
        print("Running report_by_mail() every minute")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        job_count = 0
        success_count = 0
        
        try:
            while True:
                job_count += 1
                print(f"\n--- Job #{job_count} ---")
                
                if run_job():
                    success_count += 1
                
                print(f"Success rate: {success_count}/{job_count}")
                print("Waiting 60 seconds for next run...")
                
                # Countdown timer
                for i in range(60, 0, -10):
                    print(f"Next run in {i} seconds...", end='\r')
                    time.sleep(10)
                
        except KeyboardInterrupt:
            print(f"\n\nScheduler stopped!")
            print(f"Total jobs run: {job_count}")
            print(f"Successful jobs: {success_count}")
            print("Goodbye!")

    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure Django is properly installed and configured")
except Exception as e:
    print(f"Setup error: {e}")