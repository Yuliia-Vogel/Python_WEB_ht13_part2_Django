from django.db import models

# моделі Author і Quote моєї бази даних в МонгоДБ:
class Author(models.Model):
    fullname = models.CharField(max_length=255, unique=True)  # унікальне поле
    born_date = models.DateField(null=True, blank=True)  #може бути порожньою
    born_location = models.TextField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Назва тегу, унікальна

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()  # Текст цитати
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quote')  # Зв'язок із автором
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)  # Теги, пов'язані з цитатою

    def __str__(self):
        return  f"'{self.quote}' \n by {self.author.name} (about) \n Tags: {self.tags}"



