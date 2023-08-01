from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='cодержание')
    image = models.ImageField(verbose_name='изображение', upload_to='blog/', null=True, blank=True)
    views = models.IntegerField(verbose_name='количество просмотров', default=0, editable=False)
    published_date = models.DateTimeField(verbose_name='дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

