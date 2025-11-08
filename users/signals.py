# from django.contrib.auth.models import User
 
 
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Profile




# @receiver(post_save, sender=User)
# def createProfile(sender, instance, created, **kwargs):
#     print('Profile signal triggered')
#     if created:
#         user = instance
#         profile = Profile.objects.create(
#             user=user,
#             username=user.username,
#             email=user.email,
#         )
# post_save.connect(createProfile, sender=User)

# post_delete.connect (createProfile, sender=User)













from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
        # except:
        #     print('Email failed to send...')


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the user was just created
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This ensures the profile is also saved when the user is updated
    instance.profile.save()
    


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
