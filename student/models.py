from django.db import models

# Create your models here.
class Student(models.Model):
    #定义name,age,gender(年级),email长度
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    # 检查合法性？
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name