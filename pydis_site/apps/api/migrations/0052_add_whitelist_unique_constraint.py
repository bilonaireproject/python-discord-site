# Generated by Django 2.2.8 on 2020-01-13 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_import_whitelisted_items'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='whitelist',
            unique_together={('type', 'whitelisted_item')},
        ),
    ]
