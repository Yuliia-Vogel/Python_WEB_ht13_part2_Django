import os
import django # в мене не вийшло "подружити" моделі Джанго з SQLAlchemy,
# тому для роботи з Постгресом навіть тут використовую ОРМ від Джанго

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw10_project.settings')
django.setup()

from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv

from quotes.models import Author, Quote, Tag

load_dotenv() # завантажуються дані з файлу .env 
# # створюємо змінну для сікрета для Постгреса у файлі .env
# postgres_db_name = os.getenv("POSTGRES_DB_NAME")

# створюємо змінні для всіх сікретів для Монго у файлі .env
mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
cluster_name = os.getenv("MONGO_CLUSTER")
app_name = os.getenv("APP_NAME")
mongo_db_name = os.getenv("MONGO_DB_NAME")

URI = f"mongodb+srv://{mongo_user}:{mongo_pass}@{cluster_name}.iva9h8j.mongodb.net/?retryWrites=true&w=majority&appName={app_name}"

# Використовуємо pymongo для підключення до MongoDB
client = MongoClient(URI)
mongo_db = client[mongo_db_name]

if client:
    print("Mongo connected")
else:
    print("Not connected to Mongo")

# роблю функцію зміни формату дати, бо формат дати народження, записаний в Монго, Джанго не може прийняти
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()  # Перетворюємо дату у формат YYYY-MM-DD
    except (ValueError, TypeError):
        return None  # Якщо формат невірний або відсутній, повертаємо None


# data migration from MongoDB to PostgreSQL:

# Отримую авторів з монги:
authors_collection = mongo_db['author']
authors_dict ={}

for author in authors_collection.find():
    # Створюю нового автора в постгресі:
    born_date = parse_date(author.get('born_date'))  # Конвертація дати народження
    description = str(author.get('description')).lstrip()  # Видаляю зайві пробіли та ентери на початку
    new_author = Author(fullname=author['fullname'], 
                        born_date=born_date, 
                        born_location=author.get('born_location'), 
                        description=description) 
    new_author.save() # зберігаю нового автора в Постгресі з доп. Джанго ОРМ
    # Зберігаємо відповідність ObjectId автора з MongoDB і його ID у PostgreSQL
    authors_dict[str(author['_id'])] = new_author
print("Authors migrated successfully")

# отримання цитат і тегів з монги (через Pymongo - тщму що з Монгоенджін у мене виникли проблеми з повторними підключеннями-відключеннями протягом тестування цього скріпта)
quotes_collection = mongo_db['quote']
for quote in quotes_collection.find():
    # Знаходження автора за ObjectId
    # author_id = quote.get('author')
        # if author_id:
        # Знаходимо відповідного автора в колекції авторів
    #     author_document = authors_collection.find_one({'_id': author_id})
    #     if author_document:
    #         author_fullname = author_document['fullname']
    #         # Знаходимо або створюємо автора в PostgreSQL
    #         author = Author.objects.filter(fullname=author_fullname).first()
    #         if author:
    #             # Створення нової цитати в PostgreSQL
    #             new_quote = Quote(quote=quote['quote'], author=author)
    #             new_quote.save()  # Зберігання в PostgreSQL з допомогою Django ORM
    #     else:
    #         print(f"Author not found for quote: {quote}")
    # else:
    #     print(f"Quote without 'fullname': {quote}")
    
    # author = Author.objects.filter(fullname=quote['author']['fullname']).first()
    # if author:
    #     new_quote = Quote(text=quote['quote'], author=author)
    #     new_quote.save()

    #     # Обробка тегів
    #     for tag_name in quote['tags']:
    #         tag, created = Tag.objects.get_or_create(name=tag_name)
    #         new_quote.tags.add(tag)

    author_id = str(quote['author'])  # Отримуємо ObjectId автора як рядок
    author = authors_dict.get(author_id)  # Знаходимо автора за цим ID

    if author:
        new_quote = Quote(quote=quote['quote'], author=author)
        new_quote.save()

        # Обробка тегів
        for tag_name in quote['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            new_quote.tags.add(tag)

        new_quote.save()

print("Quotes and tags migrated successfully")

client.close()  # Закриваємо підключення до Монго
