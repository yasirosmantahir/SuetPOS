# Generated by Django 4.2.11 on 2024-08-25 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_sizes_groupedsizes"),
    ]

    operations = [
        migrations.RemoveField(model_name="groupedsizes", name="category",),
        migrations.AddField(
            model_name="groupedsizes",
            name="name",
            field=models.CharField(default="", max_length=15),
            preserve_default=False,
        ),
    ]
