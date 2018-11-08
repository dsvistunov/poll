from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def get_absolute_url(self):
        return '/polls/%i/' % self.id


class Question(models.Model):
    INPUT_TYPES = (
        ('TXT', 'text'),
        ('RAD', 'radio'),
        ('CHK', 'checkbox'),
        ('SLT', 'select'),
        ('MSL', 'multiselect'),
        ('NUM', 'number'),
        ('EMP', '')
    )
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=INPUT_TYPES, default='EMP', verbose_name='Answer type')
    size = models.IntegerField(default=1)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=120)
    votes = models.IntegerField(default=0)
    max_value = models.IntegerField(blank=True, null=True)
    min_value = models.IntegerField(blank=True, null=True)


class UserAgent(models.Model):
    data = models.TextField()
