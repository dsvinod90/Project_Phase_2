SELECT * 
FROM
	(SELECT
		playlist.playlist_id,
		playlist.name as playlist,
		ROUND(AVG(track.duration)/(1000*60), 2) as "average_track_duration(min)"
	FROM
		playlist
		JOIN track_playlist ON playlist.playlist_id = track_playlist.playlist_id
		JOIN track ON track.id = track_playlist.track_id
	GROUP BY(playlist.playlist_id)
	ORDER BY ("average_track_duration(min)") DESC
	LIMIT 5) as longest
UNION
SELECT *
FROM 
	(SELECT
		playlist.playlist_id,
		playlist.name as playlist,
		ROUND(AVG(track.duration)/(1000*60), 2) as "average_track_duration(min)"
	FROM
		playlist
		JOIN track_playlist ON playlist.playlist_id = track_playlist.playlist_id
		JOIN track ON track.id = track_playlist.track_id
	GROUP BY(playlist.playlist_id)
	ORDER BY ("average_track_duration(min)") ASC
	LIMIT 5) as shortest
 ORDER BY ("average_track_duration(min)") DESC;