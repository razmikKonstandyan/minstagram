import os

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User


# user db


class UserPageData(models.Model):
    class Meta:
        db_table = 'user_page_data'

    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class UserProfileData(models.Model):
    class Meta:
        db_table = 'user_profile_data'

    status = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, related_name="followed", blank=True)


@receiver(models.signals.post_delete, sender=UserPageData)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=UserPageData)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = UserPageData.objects.get(pk=instance.pk).image
    except UserPageData.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
