# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # slug = models.SlugField(default=False, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Database model for Chat Room
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def contains_user(self, id):
        if self.label == 'global':
            try:
                uname = User.objects.get(id=id)
                my_msgs = self.messages.filter(sender__username__iexact=uname.username)
                if my_msgs:
                    return True
                else:
                    return False
            except User.DoesNotExist:
                return False

        one, other = self.label.split('_')
        return str(one) == str(id) or str(other) == str(id)

    def get_room_name(self, user_id):
        """
        Returns the room name, usually the name of the other person.
        :return: Name
        """
        if self.label == 'global':
            return 'Global'

        other = self.get_other_participant(user_id)
        other_obj = User.objects.get(id=other)

        if len(other_obj.first_name) != 0 and len(other_obj.last_name) != 0:
            return other_obj.first_name + ' ' + other_obj.last_name
        else:
            return other_obj.username

    def get_other_participant(self, user_id):
        """
        Returns the other participant in the chat.
        It is assumed that the user_id is a number.
        :param user_id:
        :return:
        """
        one, other = self.label.split('_')
        one = str(one)
        other = str(other)
        user_id = str(user_id)

        if one == user_id:
            return other

        return one

    def get_room_link(self, user_id):
        """
        Returns the "room link". This basically means the method returns either the string 'all',
        or the ID of the other participant.
        :param user_id:
        :return:
        """

        if self.label == 'global':
            return 'all'

        return self.get_other_participant(user_id)


# Database model for Chat Message
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=DO_NOTHING)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=CASCADE, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now(), db_index=True)


# Database model for one User's music collection
class MusicPiece(models.Model):
    creator = models.ForeignKey(User, related_name='my_music', on_delete=CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=datetime.now(), db_index=True)