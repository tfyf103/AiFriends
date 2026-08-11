from django.db import migrations, models
from django.db.models import Count


def merge_duplicate_friends(apps, schema_editor):
    """Preserve history before enforcing the new uniqueness invariant.

    Older project versions only enforced uniqueness in View code. If an existing
    database somehow contains duplicate (user, character) Friend rows, a plain
    AddConstraint migration would fail. This data migration:

    1. keeps the oldest Friend as the canonical row;
    2. moves every duplicate Message onto it;
    3. keeps the newest non-empty memory text;
    4. deletes the redundant Friend rows;
    5. then the following operation adds the database constraint.
    """
    Friend = apps.get_model('web', 'Friend')
    Message = apps.get_model('web', 'Message')

    duplicates = (
        Friend.objects
        .values('me_id', 'character_id')
        .annotate(row_count=Count('id'))
        .filter(row_count__gt=1)
    )

    for group in duplicates.iterator():
        rows = list(
            Friend.objects
            .filter(
                me_id=group['me_id'],
                character_id=group['character_id'],
            )
            .order_by('id')
        )

        primary = rows[0]
        redundant = rows[1:]
        redundant_ids = [row.id for row in redundant]

        Message.objects.filter(friend_id__in=redundant_ids).update(friend_id=primary.id)

        newest_memory = next(
            (row.memory for row in reversed(rows) if row.memory),
            primary.memory,
        )
        if newest_memory != primary.memory:
            primary.memory = newest_memory
            primary.save(update_fields=['memory'])

        Friend.objects.filter(id__in=redundant_ids).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0007_voice_character_voice'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_friends, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='friend',
            constraint=models.UniqueConstraint(
                fields=('me', 'character'),
                name='unique_friend_per_user_character',
            ),
        ),
    ]
