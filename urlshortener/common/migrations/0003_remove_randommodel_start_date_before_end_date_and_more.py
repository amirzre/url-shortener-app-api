# Generated by Django 4.1.2 on 2022-10-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_alter_randommodel_id"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="randommodel",
            name="start_date_before_end_date",
        ),
        migrations.AddConstraint(
            model_name="randommodel",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("start_date__lt", models.F("end_date")),
                    ("end_date__isnull", True),
                    _connector="OR",
                ),
                name="start_date_before_end_date",
            ),
        ),
    ]
