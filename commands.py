def setup(connection, cursor):

    commands = [
        """CREATE TABLE IF NOT EXISTS `songs` (
            `song_id` varchar(50) NOT NULL,
            `name` varchar(1000) NOT NULL,
            `album` varchar(1000) NOT NULL,
            `artist` varchar(1000) NOT NULL,
            PRIMARY KEY (`song_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;""",
        """CREATE TABLE IF NOT EXISTS `users` (
            `user_id` int(11) NOT NULL AUTO_INCREMENT,
            `login` varchar(32) NOT NULL,
            `password` varchar(32) NOT NULL,
            PRIMARY KEY (`user_id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;""",
        """CREATE TABLE IF NOT EXISTS`liked_music` (
            `item_id` int(11) NOT NULL AUTO_INCREMENT,
            `u_id` int(11) NOT NULL,
            `s_id` varchar(50) NOT NULL,
            PRIMARY KEY (`item_id`),
            KEY `u_id` (`u_id`),
            KEY `s_id` (`s_id`),
            CONSTRAINT `liked_music_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `liked_music_ibfk_2` FOREIGN KEY (`s_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"""
    ]
    
    for i in commands:
        cursor.execute(i)

    connection.commit()
    return