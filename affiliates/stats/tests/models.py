from django.db import models


class TestModelRel(models.Model):
    value = models.BooleanField()


class TestModel(models.Model):
    other = models.ForeignKey(TestModelRel)
    someflag = models.BooleanField()
    mychoice = models.CharField(max_length=5,
                                choices=[('test1', 'Test1'),
                                         ('test2', 'Test2')])
    unimportant = models.IntegerField()
    datetime = models.DateTimeField()
