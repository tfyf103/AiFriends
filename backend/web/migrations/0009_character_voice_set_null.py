from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0008_friend_unique_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='voice',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=models.SET_NULL,
                to='web.voice',
            ),
        ),
    ]
