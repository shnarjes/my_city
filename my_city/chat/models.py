from django.db import models
from user.models.user import User
from django.utils.translation import gettext_lazy as _

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermessage')
    message = models.TextField(verbose_name=_('message'))
    image = models.ImageField(upload_to='images/', verbose_name=_('image'))
    document = models.FileField(upload_to='document/', verbose_name=_('document'))
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userone')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usertwo')
    messages = models.ManyToManyField(Message)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user1


class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admingroup')
    members = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)
    image = models.ImageField(upload_to='images/', verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
 
