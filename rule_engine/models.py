from django.db import models

class Rule(models.Model):
    name = models.CharField(max_length=100)
    rule_string = models.TextField()
