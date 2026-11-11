from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("products", "0003_alter_productvariant_color_hex")]
    operations = [migrations.AddField(model_name="product", name="audience", field=models.CharField(choices=[("all", "All"), ("men", "Men"), ("women", "Women"), ("kids", "Kids")], db_index=True, default="all", max_length=8))]
