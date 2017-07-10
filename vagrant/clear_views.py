"""
This is a utility script that drops all the views created from running
the main.py script.
"""

import sys
import psycopg2


def clear_views(queries):
    """Executes the SQL commands to drop all views.

    Args:
        queries (:obj:`list` of :obj:`str`): List of SQL queries.
    """

    db_conn = None



    try:
        db_conn = psycopg2.connect("dbname=news")
        conn = db_conn.cursor()

        for qry in queries:
            conn.execute(qry)

        conn.close()
        db_conn.commit()
        db_conn.close()

    except psycopg2.Error as error:
        print error.pgerror
        sys.exit(1)

    finally:
        if db_conn is None:
            db_conn.close()
            sys.exit(0)


def run_clear_views():
    """Executes the program with the global variables."""

    queries = ["drop view top_articles;", "drop view top_authors;",
               "drop view error_reporter;", "drop view total_view;",
               "drop view failed_view;"]

    clear_views(queries)


if __name__ == "__main__":
    run_clear_views()
