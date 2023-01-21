from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # we pass 2 arguments first one the signals we are interested in,
# we only interested in post save event of user model.
# this function should be called when a user model is saved for that we need a decorator
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])

# this code is not reachable unless we import it somewhere, we import this in app.py
