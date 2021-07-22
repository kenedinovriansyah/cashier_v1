# Generated by Django 3.2.5 on 2021-07-22 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(max_length=225, unique=True)),
                ('name', models.CharField(max_length=225)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(max_length=225, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sell', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(max_length=225, unique=True)),
                ('stock', models.IntegerField(default=0)),
                ('max_stock', models.IntegerField(default=0)),
                ('sold', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(max_length=225, unique=True)),
                ('type', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(max_length=225, unique=True)),
                ('name', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.accounts')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='database.category')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.currency')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.stock')),
                ('type', models.ManyToManyField(related_name='type_many_to_many', to='database.TypeProduct')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='product',
            field=models.ManyToManyField(related_name='product_many_to_many', to='database.Product'),
        ),
    ]