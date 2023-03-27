SELECT
	track.name as track,
	count(1) AS number_of_occurences
FROM
	playlist
	JOIN track_playlist ON track_playlist.track_id = playlist.playlist_id
	JOIN track ON track.id = track_playlist.track_id
GROUP BY (track.id, track.name)
ORDER BY (number_of_occurences) DESC
LIMIT 10;