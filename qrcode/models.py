from django.db import models


# Create your models here

# Logo信息
class Logo(models.Model):
    logo_id = models.IntegerField(unique=True)
    logo_name = models.CharField(max_length=30, unique=True)
    logo_host = models.CharField(max_length=100, unique=True)


# 黑名单
class Black(models.Model):
    black_host = models.CharField(unique=True, max_length=100)
    black_level = models.ForeignKey('Level', on_delete=models.CASCADE)


# 网站安全等级
class Level(models.Model):
    level = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return u'%s' % self.level
