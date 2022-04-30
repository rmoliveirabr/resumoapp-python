# Generated by Django 3.0.8 on 2020-07-26 21:13

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('posts', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationgroup',
            name='small',
            field=models.CharField(default='', max_length=10, verbose_name='Grupos de Educação - Reduzido'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.IntegerField(blank=True, default=0, verbose_name='Avaliação (1-5)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
