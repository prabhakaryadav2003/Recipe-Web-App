# Generated by Django 5.1.4 on 2024-12-23 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_recipe_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['id']},
        ),
    ]