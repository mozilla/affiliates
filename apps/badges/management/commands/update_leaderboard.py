from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Updates the leaderboard with the most up-to-date click stats.'

    def handle(self, *args, **options):
        cursor = connection.cursor()

        # Clear leaderboards
        cursor.execute('DELETE from badges_leaderboard')

        # Set ranking variable
        cursor.execute('SET @curRank := 0')

        # Populate with data
        cursor.execute("""
            INSERT INTO badges_leaderboard
            SELECT @curRank := @curRank + 1 AS rank, user_id, clicks
            FROM (
                SELECT user.id AS user_id,
                       COALESCE(SUM(stats.clicks), 0) AS clicks
                FROM auth_user AS user
                LEFT JOIN badges_badgeinstance AS instance
                     ON instance.user_id = user.id
                LEFT JOIN badges_clickstats as stats
                     ON stats.badge_instance_id = instance.id
                GROUP BY user.id
                ORDER BY clicks DESC
            ) AS t;
        """)

        # Commit
        transaction.commit_unless_managed()

        print 'Leaderboard updated successfully.'
