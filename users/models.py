from django.db import models
from django.contrib.auth.models import User
import uuid

# Models definition


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username if self.user and hasattr(self.user, "username") else "No User"


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name or "Unnamed Skill"


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, related_name="sent_messages", on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(Profile, related_name="messages", on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=False)

    def __str__(self):
        return self.subject 
    
    class Meta:
        ordering = ['is_read', '-created']
 
        # sender_name = self.sender.name if self.sender and self.sender.name else "Unknown Sender"
        # recipient_name = self.recipient.name if self.recipient and self.recipient.name else "Unknown Recipient"
        # return f"Message from {sender_name} to {recipient_name} - {self.subject or 'No Subject'}"













































# from django.db import models
# from django.contrib.auth.models import User
# import uuid 




# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

# # Create your models here.


# class Message(models.Model):
#     # Your model fields here (sender, recipient, subject, body, etc.)
#     pass



# class Profile(models.Model):    
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE,null=True, blank=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     email = models.EmailField(max_length=500, null=True, blank=True)
#     username = models.CharField(max_length=200, null=True, blank=True)
#     location= models.CharField(max_length=200, null=True, blank=True)
#     short_intro = models.CharField(max_length=200, null=True, blank=True)
#     bio = models.TextField(null=True, blank=True)
#     profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
#     social_github = models.CharField(max_length=200, null=True, blank=True)
#     social_twitter = models.CharField(max_length=200, null=True, blank=True)    
#     social_linkedin = models.CharField(max_length=200, null=True, blank=True)
#     social_youtube = models.CharField(max_length=200, null=True, blank=True)
#     social_website = models.CharField(max_length=200, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     def __str__(self):
#         return str(self.user.username)
  


# class Skill(models.Model):
#     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.name)

    
















































