"""
Django management command to run cron jobs
Usage: python manage.py runcron
"""

from django.core.management.base import BaseCommand
import time
from datetime import datetime


class Command(BaseCommand):
    help = 'Run cron jobs - Windows compatible scheduler'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--daemon',
            action='store_true',
            help='Run scheduler in daemon mode (continuous)',
        )
        parser.add_argument(
            '--once',
            action='store_true', 
            help='Run job once and exit',
        )
        parser.add_argument(
            '--simple',
            action='store_true',
            help='Use simple scheduler (recommended for Windows)',
        )
    
    def handle(self, *args, **options):
        if options['once']:
            self.run_once()
        elif options['simple'] or options['daemon']:
            self.run_simple_scheduler()
        else:
            # Default: run once
            self.run_once()
    
    def run_once(self):
        """Run report_by_mail job once and exit"""
        try:
            self.stdout.write("Running report_by_mail job once...")
            
            from cron.jobs import report_by_mail
            
            start_time = datetime.now()
            self.stdout.write(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            report_by_mail()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Job completed successfully in {duration:.2f} seconds')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Job failed: {e}')
            )
    
    def run_simple_scheduler(self):
        """Run the simple scheduler in daemon mode"""
        try:
            self.stdout.write("Starting simple Windows scheduler...")
            self.stdout.write("This will run report_by_mail() every minute")
            self.stdout.write("Press Ctrl+C to stop")
            self.stdout.write("-" * 50)
            
            from cron.jobs import report_by_mail
            
            job_count = 0
            success_count = 0
            
            while True:
                job_count += 1
                current_time = datetime.now()
                time_str = current_time.strftime('%H:%M:%S')
                
                self.stdout.write(f"[{time_str}] Job #{job_count} starting...")
                
                try:
                    report_by_mail()
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Job completed successfully")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Job failed: {e}")
                    )
                
                # Show statistics
                success_rate = (success_count / job_count) * 100
                self.stdout.write(f"Stats: {success_count}/{job_count} successful ({success_rate:.1f}%)")
                
                # Wait 60 seconds with countdown
                self.stdout.write("Next run in 60 seconds...")
                for remaining in range(60, 0, -10):
                    self.stdout.write(f"  {remaining}s remaining...", ending='')
                    self.stdout.flush()
                    time.sleep(10)
                
                self.stdout.write("")  # New line
                self.stdout.write("-" * 30)
                
        except KeyboardInterrupt:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("Scheduler interrupted by user"))
            self.stdout.write(f"Final stats: {success_count}/{job_count} jobs successful")
            self.stdout.write("Goodbye!")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Scheduler error: {e}'))