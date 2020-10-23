from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Create your models here.
class UserProfile(models.Model):
    """ Model to store default user info to speed up future purchases """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User can have only one profile, delete profile if user is deleted
    image_url = models.URLField(max_length=1024, null=True, blank=True,
                                default="https://raw.githubusercontent.com/Voggastur/fsf-project/master/media/default.jpg")
    image = models.ImageField(null=True, blank=True)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_street_address = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_county = models.CharField(max_length=40, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
