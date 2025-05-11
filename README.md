# Railway Audio Analysis Service

Сервис для подсчёта BPM, определения жанра и настроения аудиофайлов.

## Установка
1. Клонировать репозиторий.
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Подготовить модели (см. ниже).
4. Запустить локально:
   ```bash
   uvicorn main:app --reload
   ```

## Модели
Папки `models/genreClassifier` и `models/moodClassifier` должны содержать файлы `svmModel` (и опционально `svmModel.pkl`).

### Как получить модели
1. Установить pyAudioAnalysis:
   ```bash
   pip install pyAudioAnalysis
   ```
2. Подготовить датасет:
   - Для жанров: подпапки с аудио по жанрам.
   - Для настроения: подпапки с аудио по настроениям.
3. Запустить скрипты из `scripts/`:
   ```bash
   python scripts/train_genre.py --input_folder data/genres/ --model_folder models/genreClassifier
   python scripts/train_mood.py  --input_folder data/moods/  --model_folder models/moodClassifier
   ```

## Запуск на Railway
1. Загрузить в GitHub.
2. Подключить репозиторий к Railway.
3. Railway автоматически запустит через `Procfile`.
4. В Flutter-приложении делайте POST-запрос на `/analyze`.
