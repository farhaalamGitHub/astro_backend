# Generated by Django 5.0.3 on 2024-07-22 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requestor', '0006_rename_quoteionobjectdimension_quotationobjectdimension_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotationtestparameter',
            old_name='quotetion_detail',
            new_name='quotation_detail',
        ),
    ]
