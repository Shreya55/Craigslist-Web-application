from django.db import models

class Search(models.Model):
    search = models.CharField(max_length=500)
    dated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return {}.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches' #for making 'searchs'(by default) to 'searches' in admin models
