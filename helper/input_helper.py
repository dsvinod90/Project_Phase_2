def print_loader_help_menu(first_arg: str, prompt=None) -> None:
    arg_help = "{0} -H <hostname> -P <port_number>".format(first_arg)
    arg_desc = "-H: (Required) hostname of the machine running the postgresql server\n"\
    "-P: (Required) port on which mongodb is listening\n"\
    "Examples:\n"\
    "python3 {0} -H localhost -p 27017".format(first_arg) + " ---> Loads data to mongodb"
    print(f"[{prompt}]: {arg_help}") if prompt else print(arg_help)
    print(arg_desc)

def print_executor_help_menu(first_arg: str, prompt=None) -> None:
    arg_help = "{0} -H <hostname> -D <database_name> -Q <solution_number>".format(first_arg)
    arg_desc = "-h: prints the query help menu to STDOUT\n"\
    "-H: (Required) hostname of the machine running the postgresql server\n"\
    "-D: (Required) name of the database\n"\
    "-Q: (Required) Query number to be executed\n"\
    "Examples:\n"\
    "python3 {0} -h".format(first_arg) + " ---> Prints help menu\n"\
    "python3 {0} -H localhost -D imdb_assign2 -Q 3".format(first_arg) + " ---> Executes the query number 3"
    print(f"[{prompt}]: {arg_help}") if prompt else print(arg_help)
    print(arg_desc)

def print_query_menu() -> None:
    print(
        'Here are your options to query the spotify dataset consisting of 250k user created playlists:\n'\
        '1: Find common artists that appear in both happy and sad playlists\n'\
        '2: Find the 10 most popular artists across all playlists\n'\
        '3: 10 most common tracks shared across most of the playlists\n'\
        '4: Top 10 "Christmas" themed songs\n'\
        '5: Top 5 playlists with the maximum average track lengh and Top 5 playlists with the minimum average track length\n'
    )