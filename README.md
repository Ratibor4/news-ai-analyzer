# News AI Analyzer

AI-парсер новостей с РБК на Django. Использует NLP-модели для анализа содержания, категоризации и определения тональности.

##  Функциональность
- Парсинг свежих новостей с РБК
- Резюмирование текста (facebook/bart-large-cnn)
- Категоризация (facebook/bart-large-mnli)
- Эмоциональная окраска (distilbert-base-uncased-finetuned-sst-2-english)
- Интерфейс на Django

## Интерфейс
http://localhost:8000/latest/ — загрузка свежих новостей

http://localhost:8000/news/ — список всех новостей

## Используемые модели
facebook/bart-large-cnn — резюме текста

facebook/bart-large-mnli — классификация

distilbert-base-uncased-finetuned-sst-2-english — анализ тональности


Превью

![image](https://github.com/user-attachments/assets/62607a88-5224-405a-96f2-49511109c980)
![image](https://github.com/user-attachments/assets/b2eb7f2c-ed02-4ce5-a1ef-e89da93fc95e)

