# Generated by Django 4.2.6 on 2024-01-15 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0011_alter_product_percentage_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='percentage_discount',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_discount', to='Products.productdiscount', verbose_name='Discount (%)'),
        ),
    ]
