# Pre-requisites
- MongoDB (preferably version 16 and above)
- PostgreSQL (preferably version 15 and above)
- Previous PostgreSQL database of our Spotify Million Playlist

# Load Data to MongoDB
`python loader.py -H <hostname> -P <port_number>`

# Execute Queries on PostgreSQL
`python executor.py -H <hostname> -D <dbanme> -Q <query_number>`
## Help menu for queries to be executed: 
`python executor.py -h`
