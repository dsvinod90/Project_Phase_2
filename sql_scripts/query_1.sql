SELECT 
	happy_sad_tracks.artist_name as artist, 
	count(1) as number_of_tracks 
FROM (
	SELECT DISTINCT
		track_happy.id AS track_id,
		track_happy.name AS track_name,
		artist_happy.id AS artist_id,
		artist_happy.name AS artist_name
	FROM
		playlist AS playlist_happy
		JOIN track_playlist AS track_playlist_happy ON playlist_happy.playlist_id = track_playlist_happy.playlist_id
		JOIN track AS track_happy ON track_happy.id = track_playlist_happy.track_id
		JOIN track_artist AS track_artist_happy ON track_artist_happy.track_id = track_happy.id
		JOIN artist AS artist_happy ON artist_happy.id = track_artist_happy.artist_id
	WHERE
		lower(playlist_happy.name) LIKE '%happy%'
		AND EXISTS (
			SELECT
				track_sad.id AS track_id_sad,
				track_sad.name AS track_name_sad,
				artist_sad.id AS artist_id_sad,
				artist_sad.name AS artist_name_sad
			FROM
				playlist AS playlist_sad
				JOIN track_playlist AS track_playlist_sad ON playlist_sad.playlist_id = track_playlist_sad.playlist_id
				JOIN track AS track_sad ON track_sad.id = track_playlist_sad.track_id
				JOIN track_artist AS track_artist_sad ON track_artist_sad.track_id = track_sad.id
				JOIN artist AS artist_sad ON artist_sad.id = track_artist_sad.artist_id
	
			WHERE
				lower(playlist_sad.name) LIKE '%sad%'
				AND track_happy.id = track_sad.id
		)) happy_sad_tracks
GROUP BY (happy_sad_tracks.artist_id, happy_sad_tracks.artist_name)
ORDER BY count(1) DESC;