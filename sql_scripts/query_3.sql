SELECT
	distinct_tracks.name as track,
	count(1) AS number_of_occurences
FROM
    (SELECT
        track.id, track.name, playlist.playlist_id
    FROM
        playlist
        JOIN track_playlist ON track_playlist.playlist_id = playlist.playlist_id
        JOIN track ON track.id = track_playlist.track_id
    GROUP BY (track.id, track.name, playlist.playlist_id)) as distinct_tracks
GROUP BY (distinct_tracks.id, distinct_tracks.name)
ORDER BY (number_of_occurences) DESC
LIMIT 10;