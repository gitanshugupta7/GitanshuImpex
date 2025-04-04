# Generated by Django 5.1.7 on 2025-03-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gipl_app", "0006_remove_heroimage_image_heroimage_desktop_image_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarouselItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.TextField()),
                ("cta_text", models.CharField(blank=True, max_length=50, null=True)),
                ("cta_link", models.URLField(blank=True, null=True)),
                ("desktop_image", models.ImageField(upload_to="carousel/desktop/")),
                ("mobile_image", models.ImageField(upload_to="carousel/mobile/")),
            ],
        ),
        migrations.DeleteModel(
            name="HeroImage",
        ),
    ]
