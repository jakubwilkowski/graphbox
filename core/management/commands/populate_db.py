from django.core.management.base import BaseCommand

from crawler.crawler import GitCrawler


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Data gathering started.'))
        GitCrawler.populate_repos()
        self.stdout.write(self.style.SUCCESS('Data successfully gathered.'))
