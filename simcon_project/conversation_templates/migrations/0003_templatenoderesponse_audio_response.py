# Generated by Django 3.1.3 on 2021-01-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation_templates', '0002_auto_20201231_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatenoderesponse',
            name='audio_response',
            field=models.FileField(default=None, upload_to='audio/%Y/%m/%d'),
        ),
    ]
