# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import random
import string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # slug = models.SlugField(default=False, null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# def prof_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
# pre_save.connect(prof_pre_save, sender=Profile)

# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance
#     has a model with a slug field and a title character (char) field.
#     """
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.title)
#
#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#                     slug=slug,
#                     randstr=random_string_generator(size=4)
#                 )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug
#
#
# def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))