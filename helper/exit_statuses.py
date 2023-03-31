from enum import Enum

class ExitStatuses(Enum):
    """Enum for ExitStatuses for the program
    """
    OK = 0
    USAGE_ERROR = 1
    CONNECTION_ERROR = 2
    QUERY_ERROR = 3
    PORT_ERROR = 4
