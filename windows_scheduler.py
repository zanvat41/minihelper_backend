"""
Windows-compatible task scheduler for Django
Simple solution using Python threading - no external dependencies required
"""

import threading
import time
import logging
import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minihelper_backend.settings')
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class WindowsScheduler:
    """Simple Windows task scheduler using threading"""
    
    def __init__(self):
        self.jobs = []
        self.running = False
        self.thread = None
    
    def add_interval_job(self, func, interval_minutes, job_name=None):
        """Add a job that runs every X minutes"""
        job = {
            'func': func,
            'interval': interval_minutes * 60,  # Convert to seconds
            'name': job_name or func.__name__,
            'last_run': None,
            'next_run': time.time()  # Run immediately first time
        }
        self.jobs.append(job)
        logger.info(f"Added job '{job['name']}' to run every {interval_minutes} minutes")
    
    def should_run_job(self, job):
        """Check if job should run based on interval"""
        current_time = time.time()
        return current_time >= job['next_run']
    
    def run_job(self, job):
        """Execute a job and schedule next run"""
        try:
            logger.info(f"Running job: {job['name']}")
            job['func']()
            
            # Update timing
            current_time = time.time()
            job['last_run'] = current_time
            job['next_run'] = current_time + job['interval']
            
            next_run_str = datetime.fromtimestamp(job['next_run']).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Job '{job['name']}' completed. Next run: {next_run_str}")
            
        except Exception as e:
            logger.error(f"Job '{job['name']}' failed: {e}")
            # Still schedule next run even if job failed
            current_time = time.time()
            job['next_run'] = current_time + job['interval']
    
    def scheduler_loop(self):
        """Main scheduler loop"""
        logger.info("Windows scheduler started")
        
        while self.running:
            try:
                for job in self.jobs:
                    if self.should_run_job(job):
                        self.run_job(job)
                
                # Sleep for 10 seconds before next check
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                time.sleep(10)
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.scheduler_loop, daemon=True)
        self.thread.start()
        logger.info("Windows scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Windows scheduler stopped")
    
    def list_jobs(self):
        """List all jobs with their status"""
        if not self.jobs:
            logger.info("No jobs scheduled")
            return
        
        logger.info("Scheduled jobs:")
        for job in self.jobs:
            interval_min = job['interval'] / 60
            if job['last_run']:
                last_run = datetime.fromtimestamp(job['last_run']).strftime('%Y-%m-%d %H:%M:%S')
                next_run = datetime.fromtimestamp(job['next_run']).strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"  • {job['name']} - Every {interval_min} min - Last: {last_run} - Next: {next_run}")
            else:
                next_run = datetime.fromtimestamp(job['next_run']).strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"  • {job['name']} - Every {interval_min} min - Next: {next_run}")


# Initialize scheduler
scheduler = WindowsScheduler()


def setup_scheduled_jobs():
    """Setup the cron jobs"""
    try:
        # Import the function from cron.jobs
        from cron.jobs import report_by_mail
        
        # Schedule report_by_mail to run every minute
        scheduler.add_interval_job(
            func=report_by_mail,
            interval_minutes=1,
            job_name='report_by_mail_every_minute'
        )
        
        logger.info("Scheduled jobs setup completed")
        
    except ImportError as e:
        logger.error(f"Failed to import cron jobs: {e}")
    except Exception as e:
        logger.error(f"Failed to setup scheduled jobs: {e}")


if __name__ == '__main__':
    """Run the scheduler as a standalone service"""
    try:
        print("Setting up scheduled jobs...")
        setup_scheduled_jobs()
        
        print("Starting scheduler...")
        scheduler.start()
        
        print("Scheduler is running. Press Ctrl+C to stop.")
        print("The report_by_mail job will run every minute.")
        
        # Show job status
        scheduler.list_jobs()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        scheduler.stop()
        print("Scheduler stopped.")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        scheduler.stop()