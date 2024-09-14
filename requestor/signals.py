from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Quotation
from director.models import Admin  






@receiver(post_save, sender=Quotation)
def notify_on_quotation_save(sender, instance, created, **kwargs):
    if created:
        # Notify the requestor
        send_mail(
            subject='Your Quotation Has Been Created',
            message=f'Dear {instance.requestor.user.email},\n\nYour quotation with ID {instance.id} has been created successfully.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.requestor.user.email],
        )
        
        # Notify all admins
        admins = Admin.objects.all()
        admin_emails = [admin.user.email for admin in admins]
        send_mail(
            subject='A New Quotation Has Been Created',
            message=f'A new quotation with ID {instance.id} has been created by {instance.requestor.user.email}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
        )
