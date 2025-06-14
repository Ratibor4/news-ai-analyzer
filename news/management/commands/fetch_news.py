from django.core.management.base import BaseCommand
from news.parser import parse_rbc
from news.ai_utils import analyze_news
from news.models import News

class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        articles = parse_rbc()
        for article in articles:
            if News.objects.filter(link=article['link']).exists():
                continue
            summary,category,emotion =analyze_news(article['content'])
            News.objects.create(
                title=article['title'],
                link=article['link'],
                content=article['content'],
                summary=summary,
                category=category,
                sentiment=emotion,
                published_at=article['published_at']
            )