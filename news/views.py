from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

from .ai_utils import analyze_news
from .models import News
import logging

from .parser import parse_rbc


def news_list(request):
    category = request.GET.get("category")
    news = News.objects.all().order_by('-published_at')
    if category:
        news = news.filter(category=category)
    return render(request, "news/news_list.html", {
        "news_list": news,
        "selected_category": category
    })


def latest_news_page(request):
    return render(request, "news/latest_news.html")


@csrf_exempt
def fetch_latest_news(request):
    if request.method == "POST":
        articles = parse_rbc()
        count = 0
        for article in articles:
            if News.objects.filter(link=article["link"]).exists():
                continue

            if article["published_at"] < timezone.now() - timedelta(hours=12):
                continue

            summary, category, sentiment = analyze_news(article["content"])
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

        latest = News.objects.filter(published_at__gte=timezone.now() - timedelta(hours=12)).order_by("-published_at")
        news_data = [{
            "title": n.title,
            "category": n.category,
            "sentiment": n.sentiment,
            "summary": n.summary,
            "link": n.link,
        } for n in latest]

        return JsonResponse({"news": news_data, "count": count})

    return JsonResponse({"error": "Invalid request"}, status=400)

