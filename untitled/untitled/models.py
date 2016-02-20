from django.db import models

# user db


class UserPage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    # TODO what's that for?
    def __unicode__(self):
        return self.title
