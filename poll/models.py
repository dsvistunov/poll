from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def get_absolute_url(self):
        return '/polls/%i/questions/' % self.id


class Question(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    type = models.CharField(max_length=14)
    text = models.CharField(max_length=120)
    votes = models.IntegerField(default=0)


class UserAgent(models.Model):
    data = models.TextField()
