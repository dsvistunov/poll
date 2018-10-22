from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    type = models.CharField(max_length=14)
    text = models.CharField(max_length=120)
    votes = models.IntegerField(default=0)
