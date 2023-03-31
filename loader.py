import os
import sys
import json
import getopt
import pymongo
import helper.input_helper as helper
import helper.mapper as mapper

from typing import Dict
from time_logger import TimeLogger
from helper.exit_statuses import ExitStatuses

# optional and required flags for command line input to this program
flag_options = 'hH:P:'
# values that will be set for the above flags
menu_options = ['help', 'host=', 'port=']
# playlist attributes from raw json file not required for the document database
attributes_to_be_removed = ['modified_at', 
                            'num_tracks', 
                            'num_albums', 
                            'num_followers', 
                            'num_edits', 
                            'num_artists']

class Loader:
    def __init__(self, argv) -> None:
        """Constructor for this class
        Accepts the arguments passed from command line to this program, extracts hostname and port number on which
        mongodb is running for the user.
        Args:
            argv (List(str)): hostname and port number for mongodb running on host machine. Optionally accepts flag for 
            printing help menu.
        """
        self.argv = argv
        self.host, self.port = None, None
        self.options, _ = getopt.getopt(argv[1:],
                                        flag_options, menu_options)
        if not self.options:
            self._print_help_menu(argv[0], 'usage_error')
            sys.exit(ExitStatuses.USAGE_ERROR.value)
    
    def _handle_input_args(self) -> None:
        """Extract data from input params to the program.
        Sets the values for host and port and throws error if an invalid input has been provided to the program.
        """
        for option, arg in self.options:
            if option in ('-H', '--host'):
                self.host = arg
            elif option in ('-P', '--port'):
                if arg.isdigit():
                    self.port = int(arg)
                else:
                    self._print_help_menu(self.argv[0], 'invalid_port')
                    sys.exit(ExitStatuses.PORT_ERROR.value)
            else:
                self._print_help_menu(self.argv[0], 'usage_error')
                sys.exit(ExitStatuses.USAGE_ERROR.value)
        
    def _print_help_menu(arg: str, error: str):
        """Print the help menu related to this program when an error is encountered.
        Args:
            arg (str): typically the first argument to the program i.e. the name of the program
            error (str): error message to be displayed in STDOUT
        """
        helper.print_loader_help_menu(arg, mapper.errors[error])
    
    def _establish_connection(self) -> None:
        """Establish connection to mongodb based on the hostname and port number given as CLI arguments to the program
        """
        connector = pymongo.MongoClient(self.host, self.port)
        self.db = connector.project
        self.timer = TimeLogger()
        
    def _remove_attributes(self, playlist: Dict) -> Dict:
        """Remove attributes from the playlist dictionary as they are not to be included in the mongodb collection.
        Args:
            playlist (Dict): Dictionary object representing a playlist from the input json file
        Returns:
            Dict: Updated playlist object with the key-value pairs that are needed for the mongodb collection
        """
        for key in attributes_to_be_removed:
            del playlist[key]
        return playlist

    def _modify_playlist(self, playlist: Dict) -> None:
        """Modify uri to extract the unique alphanumeric characters
        Takes as input, the playlist and strips the text "spotify:uri:" from the attribute value
        Args:
            playlist (Dict): playlist data as a dictionary
        """
        playlist['_id'] = playlist.pop('pid')
        playlist = self._remove_attributes(playlist)
        for track in playlist['tracks']:
            track['track_uri'] = track['track_uri'][14:]
            track['artist_uri'] = track['artist_uri'][15:]
            track['album_uri'] = track['album_uri'][14:]

    def _load_data(self) -> None:
        """Load the playlist data into mongodb
        """
        print('Importing json files to mongodb')
        self.timer.start()
        for json_file in os.scandir('data'):
            with open(json_file) as file:
                data = json.load(file)
                for playlist in data['playlists']:
                    self._modify_playlist(playlist)
            self.db.Playlists.insert_many(data['playlists'])
        self.timer.end()
    
    def execute(self) -> None:
        """Public method that is called to load the data to mongodb
        """
        self._handle_input_args()
        self._establish_connection()
        self._load_data()
        sys.exit(ExitStatuses.OK.value)


if __name__ == '__main__':
    Loader(sys.argv).execute()