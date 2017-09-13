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


# tup1, tup2, tup3: Tuple data for questions and answers.
TUP1 = ("Here are the three top articles (total views): ",
        "select title, views from top_articles;")

TUP2 = ("Here are the most popular authors (total views): ",
        "select name, views from top_authors;")

TUP3 = ("Here are the dates when 404 errors exceeded 1%: ",
        "select date, percent_error from error_reporter;")

# Queries for creating views
VIEWS_SQL = open("views.sql", "r").read()
QUERIES_ARRAY = [TUP1, TUP2, TUP3]


def print_table(ques, data):
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


def process_db(init):
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
            cur.execute(VIEWS_SQL)
        else:

            # Extract data from the views.
            for qstn, ansr in QUERIES_ARRAY:
                cur.execute(ansr)
                data = cur.fetchall()
                print_table(qstn, data)

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


def initialize():
    """"Starts the database query process."""

    data_ready = process_db(True)

    while True:
        if data_ready:
            process_db(False)
            break


if __name__ == "__main__":
    initialize()
