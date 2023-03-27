SELECT 
	track.name as track,
	count(1) as number_of_occurrences
FROM
	playlist
	JOIN track_playlist ON playlist.playlist_id = track_playlist.playlist_id
	JOIN track ON track.id = track_playlist.track_id
WHERE lower(playlist.name) LIKE '%christmas%'
GROUP BY (track.id, track.name)
ORDER BY (number_of_occurrences) DESC
LIMIT 10;