from django.db import models


class Timestamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Category(Timestamp):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Tag(Timestamp):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Subscribe(Timestamp):
    email = models.EmailField(max_length=225, unique=True, db_index=True)

    def __str__(self):
        return f"{self.email}' subscription"


class Contact(Timestamp):
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, null=True, blank=True)
    subject = models.CharField(max_length=225, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.name}\'s contact'
