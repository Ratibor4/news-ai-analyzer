import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import logging

from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt

from news.ai_utils import analyze_news
from news.models import News


def parse_rbc():
    url = "https://www.rbc.ru/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("a[itemprop='url']")
    articles =[]

    for item in items [:5]:
        link = item.get("href")
        title = item.get_text(strip=True)
        content = "..."
        published_at = make_aware(datetime.now())
        articles.append({
            "title": title,
            "link": link,
            "content": content,
            "published_at": published_at,
        })

    return articles


logger = logging.getLogger(__name__)

@csrf_exempt
def fetch_latest_news(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        articles = parse_rbc()
        count = 0

        for article in articles:
            if News.objects.filter(link=article["link"]).exists():
                continue

            if article["published_at"] < timezone.now() - timedelta(hours=12):
                continue


            summary, category, sentiment = analyze_news(article.get("content", ""))

            if not article.get("title") or not summary.strip():
                logger.warning(f"Пропущена статья (нет title или summary): {article.get('link')}")
                continue


            News.objects.create(
                title=article["title"],
                link=article["link"],
                content=article["content"],
                summary=summary,
                category=category,
                sentiment=sentiment,
                published_at=article["published_at"]
            )
            count += 1


        latest = News.objects.filter(
            published_at__gte=timezone.now() - timedelta(hours=12)
        ).order_by("-published_at")

        news_data = [{
            "title": n.title,
            "category": n.category or "неизвестно",
            "sentiment": n.sentiment or "Neutral",
            "summary": n.summary or "",
            "link": n.link
        } for n in latest]

        return JsonResponse({"news": news_data, "count": count})

    except Exception as e:
        logger.error(f"Ошибка при загрузке новостей: {str(e)}")
        return JsonResponse({"error": "Ошибка при загрузке новостей."}, status=500)