FastAPI-приложение для хранения и управления данными о шинах. Поддерживает добавление, удаление и массовую загрузку данных.

Установка
```
pip install -r requirements.txt
```

Запуск
```
uvicorn app:app --reload
```

Примеры запросов:
Добавить шину
```
curl -X POST "http://127.0.0.1:8000/tires?brand=Continental&diameter=16&pressure=2.5&status=normal"
```

Удалить шину
```
curl -X DELETE http://127.0.0.1:8000/tires/1
```

Получить список шин
```
curl http://127.0.0.1:8000/tires
```

Массовая загрузка из JSON
```
curl -X POST "http://127.0.0.1:8000/tires/upload_json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@tires.json"
```