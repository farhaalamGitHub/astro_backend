# Generated by Django 5.0.3 on 2024-07-21 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requestor', '0004_alter_quotation_requestor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='File',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='Geometry',
            new_name='geometry',
        ),
    ]
