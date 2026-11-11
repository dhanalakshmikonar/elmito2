from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("products", "0005_collectionitem")]

    operations = [
        migrations.RemoveField(
            model_name="productvariant",
            name="color_hex",
        ),
        migrations.AlterField(
            model_name="productvariant",
            name="color",
            field=models.CharField(
                help_text="Enter a color name such as Navy Blue.", max_length=40, verbose_name="Color name"
            ),
        ),
    ]
