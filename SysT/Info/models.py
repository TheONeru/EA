from django.db import models

# Create your models here.
#モデルはフィールドを指定するだけ
#SQLのクエリはdjango特有のものを使う
#変更後はmakemigrations, migrate sqlmigrateでテーブルを作成後にmigrateを使ってデータベースにデータフィールドを反映させる

class Stock(models.Model):
    name=models.CharField(max_length=8)
    amount=models.IntegerField(default=1)

    def __str__(self):
        return self.name
