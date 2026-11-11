from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("products", "0004_product_audience")]

    operations = [
        migrations.CreateModel(
            name="CollectionItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("image", models.ImageField(upload_to="collection/")),
                ("position", models.PositiveSmallIntegerField(default=0, help_text="Display order (0–9).")),
                ("is_active", models.BooleanField(default=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="collection_items", to="products.product")),
            ],
            options={
                "verbose_name": "Homepage Collection image",
                "verbose_name_plural": "Homepage Collection images",
                "ordering": ["position", "id"],
            },
        ),
    ]
