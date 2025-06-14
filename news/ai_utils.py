from transformers import pipeline


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")


def analyze_news(text):
    """
    Выполняет резюмирование текста, определение категории и эмоциональной окраски.

    Возвращает:
        summary (str): краткое содержание текста
        category (str): наиболее вероятная категория из списка
        emotion (str): эмоциональная окраска (Positive / Negative / Neutral)
    """
    try:
        max_input_length = 1024
        text = text[:max_input_length]
        tokens = len(text.split())

        if tokens < 5:
            print("[!] Короткий текст (менее 5 слов), пропуск:", text)
            return text, "неизвестно", "Neutral"


        max_len = min(60, int(tokens * 0.5))
        min_len = max(5, int(max_len * 0.3))


        try:
            summary_result = summarizer(
                text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )
            summary = summary_result[0].get('summary_text', "").strip()
        except Exception as e:
            print("❌ Ошибка в summarizer:", e)
            summary = ""


        try:
            candidate_labels = ["политика", "экономика", "технологии", "спорт"]
            classification = classifier(text, candidate_labels=candidate_labels)
            category = classification.get("labels", ["неизвестно"])[0]
        except Exception as e:
            print("❌ Ошибка в classifier:", e)
            category = "неизвестно"


        try:
            sentiment_result = sentiment(text)[0]
            emotion = sentiment_result.get("label", "Neutral")
        except Exception as e:
            print("❌ Ошибка в sentiment:", e)
            emotion = "Neutral"

        return summary, category, emotion

    except Exception as e:
        print("❌ Общая ошибка в analyze_news:", e)
        return "", "неизвестно", "Neutral"
