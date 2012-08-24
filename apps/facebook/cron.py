from django.db import connection, transaction

import cronjobs


@cronjobs.register
def update_facebook_leaderboard():
    """Updates the leaderboard rankings on the Facebook app."""
    print 'Updating Facebook Leaderboard...'
    cursor = connection.cursor()

    # Set ranking variable
    cursor.execute('SET @curRank := 0')

    # Populate with data
    cursor.execute("""
        UPDATE facebook_facebookuser AS user
        INNER JOIN (
            SELECT @curRank := @curRank + 1 AS rank, t2.user_id, t2.clicks
            FROM (
                SELECT user.id AS user_id,
                       COALESCE(SUM(instance.total_clicks), 0) AS clicks
                FROM facebook_facebookuser AS user
                LEFT JOIN facebook_facebookbannerinstance AS instance
                     ON instance.user_id = user.id
                GROUP BY user.id
                ORDER BY clicks DESC
            ) AS t2
        ) AS t
        SET user.leaderboard_position = t.rank, user.total_clicks = t.clicks
        WHERE t.user_id = user.id;
    """)

    transaction.commit_unless_managed()
    print 'Leaderboard updated successfully.'
