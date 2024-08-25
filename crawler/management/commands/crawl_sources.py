from django.core.management.base import BaseCommand
from crawler.tasks import crawl_sources as crawl_sources_task


class Command(BaseCommand):
    help = "Trigger crawl sources Celery task"

    def handle(self, *args, **options):
        crawl_sources_task.delay()
        self.stdout.write(
            self.style.SUCCESS("Successfully triggered crawl sources task")
        )
