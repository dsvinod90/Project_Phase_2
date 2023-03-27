import sys
import getopt
import psycopg2
import helper.input_helper as helper
import helper.mapper as mapper

from time_logger import TimeLogger
from psycopg2.extras import RealDictCursor
from helper.exit_statuses import ExitStatuses

result_limit = 10
script_path = 'sql_scripts/query_'
menu_options = ['help', 'host=', 'dbname=', 'query=']
flag_options = 'hH:D:Q:'

class Executor:
    def __init__(self, argv) -> None:
        self.argv = argv
        self.query_number = None
        self.timer = TimeLogger()
        self.host, self.dbname = None, None
        self.options, _ = getopt.getopt(argv[1:],
                                        flag_options, menu_options)
        if not self.options:
            self._print_help_menu(argv[0], 'usage_error')
            sys.exit(ExitStatuses.USAGE_ERROR.value)
    
    def _handle_input_args(self) -> None:
        for option, arg in self.options:
            if option in ('-h', '--help'):
                helper.print_query_menu()
                sys.exit(0)
            elif option in ('-H', '--host'):
                self.host = arg
            elif option in ('-D', '--dbname'):
                self.dbname = arg
            elif option in ('-Q', '--query'):
                if arg.isdigit():
                    self.query_number = int(arg)
                else:
                    self._print_help_menu(self.argv[0], 'invalid_query')
                    sys.exit(ExitStatuses.QUERY_ERROR.value)
            else:
                self._print_help_menu(self.argv[0], 'usage_error')
                sys.exit(ExitStatuses.USAGE_ERROR.value)
    
    def _print_help_menu(self, arg: str, error: str) -> None:
        helper.print_executor_help_menu(arg, mapper.errors[error])
        
    def _establish_connection(self) -> None:
        try:
            connection = psycopg2.connect(host=self.host, dbname=self.dbname)
            connection.set_session(autocommit=True)
            self.cursor = connection.cursor(cursor_factory=RealDictCursor)
        except(psycopg2.OperationalError) as connection_error:
            print(connection_error)
            print('Exiting program...')
            sys.exit(ExitStatuses.CONNECTION_ERROR.value)
        
    def _execute_query(self) -> None:
        if not self.query_number:
            self._print_help_menu(self.argv[0], 'usage_error')
            sys.exit(ExitStatuses.USAGE_ERROR.value)
        if self.query_number not in mapper.queries.keys():
            self._print_help_menu(self.argv[0], 'invalid_query')
            sys.exit(ExitStatuses.QUERY_ERROR.value)
        print(f"Executing query#{self.query_number}...")
        print(f"{mapper.queries[self.query_number]}\n")
        self.timer.start()
        self.cursor.execute(open(f"{script_path}{self.query_number}.sql").read())
        self.timer.end()
        results = self.cursor.fetchall()
        for index, row in enumerate(results):
            if index >= result_limit: break
            print(dict(row))
        print(f"TOTAL ROWS = {len(results)}\n")
        
    def execute(self):
        self._handle_input_args()
        self._establish_connection()
        self._execute_query()
        sys.exit(ExitStatuses.OK.value)


if __name__ == '__main__':
    Executor(sys.argv).execute()