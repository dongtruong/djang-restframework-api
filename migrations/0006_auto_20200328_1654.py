# Generated by Django 3.0.4 on 2020-03-28 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200328_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='doc_num',
            new_name='doc_number',
        ),
    ]