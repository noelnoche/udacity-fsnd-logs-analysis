#!/usr/bin/env python

"""
This script makes queries to the PostgreSQL database 'news' and filters
results that answer the questions:
    1. What are the three most popular articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of request lead to errors?
"""

import sys
import psycopg2


class ReportLog(object):
    """Database interface.
    This class provides the interface for making and filtering SQL
    queries and displaying the formatted results.

    Args:
        queryarray (:obj:`list` of :obj: `str`): Array of SQL queries.
        viewssarray (:obj:`list` of :obj: `tuple`): Array of tuples,
        with each tuple containing a string for the question and a
        string to query the view tables.
    """

    def __init__(self, queryarray, viewsarray):
        self.queries_array = queryarray
        self.views_array = viewsarray
        self.data_ready = False


    def print_table(self, ques, data):
        """Displays the results in a table format.

        Args:
            ques (str): The question the results answer.
            data (:obj:`list` of :obj:`tuple`): Data retrieved from the
            views created from the PostgreSQL database.
        """
        print "\n"
        print ques
        print "{:_<35} | {:_>10}".format('', '')

        for row in data:
            print "{:<35} | {:>10}".format(row[0], row[1])


    def process_db(self, init):
        """Connects and makes queries to PostgreSQL database.
        It makes two sets queries. The first creates views that make the
        complex queries that grab the filtered data; the second then
        queries those views for printing out with print_table().

        Args:
            init (bool): If True, creates the views.
        """

        db_conn = None

        try:
            db_conn = psycopg2.connect("dbname=news")
            cur = db_conn.cursor()

            if init:

                # Create the views.
                # for qry in self.queries_array:
                #     cur.execute(qry)
                cur.execute(self.queries_array)
            else:

                # Extract data from the views.
                for qstn, ansr in self.views_array:
                    cur.execute(ansr)
                    data = cur.fetchall()
                    self.print_table(qstn, data)

                print "\nHave a nice day!\n"

            cur.close()
            db_conn.commit()
            db_conn.close()

            return True

        except psycopg2.Error as error:
            print error.pgerror
            sys.exit(1)

        finally:
            if db_conn is None:
                print "Could not connect to database!"
                db_conn.close()
                sys.exit(0)

    def initialize(self):
        """"Starts the database query process."""

        self.data_ready = self.process_db(True)

        while True:
            if self.data_ready:
                self.process_db(False)
                break


def run_main():
    """Executes the program using the global variables.
    The variables contain the SQL queries that are to be passed nto the
    ReportLog interface.
    """

    # Adds a view for the top 3 articles in the database.
    # qry1 = ("create or replace view top_articles as "
    #         "select articles.title, count(log.path) as views from articles, "
    #         "log where log.status = '200 OK' and log.path != '/' and "
    #         "log.path like concat('%', articles.slug) group by "
    #         "articles.title order by views desc limit 3;")

    # Adds a view for author viewer ranking.
    # qry2 = ("create or replace view top_authors as "
    #         "select authors.name, subsq.views from authors, "
    #         "(select articles.author, count(log.path) as views from articles, "
    #         "log where log.status = '200 OK' and log.path != '/' and "
    #         "log.path like concat('%', articles.slug) group by articles.author "
    #         "order by views desc) as subsq where authors.id = subsq.author;")

    # Creates views that are used in qry3.
    # q3v = ("create or replace view total_view as "
    #        "select to_char(time, 'YYYY-MM-DD') as date, count(log.status) "
    #        "as total_requests from log group by date order by date desc;"
    #        "create or replace view failed_view as "
    #        "select to_char(time, 'YYYY-MM-DD') as date, count(log.status) "
    #        "as failed_requests from log where log.status = '404 NOT FOUND' "
    #        "group by date order by date desc;")

    # Creates a view for dates when failed requests exceed 1 percent.
    # qry3 = ("create or replace view error_reporter as "
    #         "select f.date as date, "
    #         "round((f.failed_requests/t.total_requests::float * 100)::numeric,"
    #         "2) as percent_error from (select * from failed_view) as f, "
    #         "(select * from total_view) as t where f.date = t.date and "
    #         "f.failed_requests/t.total_requests::float * 100.00 > 1;")

    # tup1, tup2, tup3: Tuple data for questions and answers.
    tup1 = ("Here are the three top articles (total views): ",
            "select title, views from top_articles;")

    tup2 = ("Here are the most popular authors (total views): ",
            "select name, views from top_authors;")

    tup3 = ("Here are the dates when 404 errors exceeded 1%: ",
            "select date, percent_error from error_reporter;")

    # queries_array = [qry1, qry2, q3v, qry3]
    queries_array = open("views.sql", "r").read()
    views_array = [tup1, tup2, tup3]

    logsobj = ReportLog(queries_array, views_array)
    logsobj.initialize()


if __name__ == "__main__":
    run_main()
