from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    cat = models.ForeignKey(to='CategoryPost', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class CategoryPost(models.Model):
    cat_name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.cat_name

