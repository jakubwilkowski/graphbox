from django.core.management.base import BaseCommand

from crawler.crawler import GitCrawler


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Populating graph started.'))
        GitCrawler.populate_graph()
        self.stdout.write(self.style.SUCCESS('Data successfully gathered.'))
