from django.db import models

# Create your models here.

class Question(models.Model):
    sbject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.sbject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.question

class Hot_issue:
    def set_info(self, subject, url):
        self.subject = subject
        self.url = url

    def __str__(self):
        return self.subject