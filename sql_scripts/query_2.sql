SELECT
	artist.name as artist,
	count(1) total_number_of_tracks
FROM
	playlist
	JOIN track_playlist ON track_playlist.playlist_id = playlist.playlist_id
	JOIN track ON track.id = track_playlist.track_id
	JOIN track_artist ON track_artist.track_id = track.id
	JOIN artist ON artist.id = track_artist.artist_id
GROUP BY (artist.id, artist.name)
ORDER BY total_number_of_tracks DESC
LIMIT 10;
