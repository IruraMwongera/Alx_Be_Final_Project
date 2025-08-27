# revenue/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import create_permit_types

@receiver(post_migrate)
def populate_permit_types(sender, **kwargs):
    create_permit_types()
