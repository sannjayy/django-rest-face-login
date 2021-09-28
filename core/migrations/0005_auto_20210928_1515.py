# Generated by Django 3.2.7 on 2021-09-28 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_loginattempt_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginattempt',
            name='blob_img',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loginattempt',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded_temp_images'),
        ),
    ]