# Generated by Django 3.1.3 on 2023-04-28 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_guide', '0018_remove_place_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=250, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_guide.customer')),
                ('service_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_guide.service_man')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_text', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_guide.customer')),
                ('service_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_guide.service_man')),
            ],
        ),
    ]
