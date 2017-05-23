#!/usr/local/bin/python3

import psycopg2
import datetime
import os

# create a path str to save report text files to the reports directory
cwd = os.getcwd().split("/")
cwd.remove("app")
report_dir = ''
for dir_name in cwd:
    report_dir = report_dir + dir_name + '/'
report_dir = report_dir + "reports/"


# a global list of all the valid reports available and the SQL to retrieve their data sets
report_names = {"1": ["Top_Authors", "SELECT name, article_views FROM author_rank"],
                "2": ["Most_Viewed_Articles", "SELECT title, views FROM article_top3"],
                "3": ["Server_Errors", "SELECT percentage_of_errors, request_date FROM high_error_dates"]}


def get_report_header(report_name):
    """ :return a list of str to create the report header with some simple information """
    header = []
    date = str(datetime.datetime.now().replace(microsecond=0))
    header.append("Report Name: {}{}".format(report_name, "\n"))
    header.append("Report Generated: {}{}".format(date, "\n\n"))
    return header


def get_file_name(report_name):
    """ :return a string formatted as 'report_name-yyyy-mm-dd' to use as a report file name"""
    return "{}{}{}{}".format(report_name, "-", str(datetime.datetime.now().date()), ".txt")


def query_db(conn, query):
    """ :return a list of results as determined by the query param """
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()


def format_rows(header, data):
    """ :return list of str formatted nicely for file writing. data param is a list of tupples. """
    report_lines = []

    # add the lines from the header list to our report lines list. Keep these at the front of the list
    for line in header:
        report_lines.append(line)

    # each report result only has 2 columns. format those column values as a string
    for item in data:
        report_line = "{}{}{}".format(item[0], item[1], "\n")
        report_lines.append(report_line)
    return report_lines


def write_file(file_name, report_lines):
    """  writes the report lines to a file. """
    file_path = "{}{}".format(report_dir, file_name)
    with open(file_path, 'w') as report:
        for line in report_lines:
            report.write(line)


def print_report(report_lines):
    """ prints the report lines to the terminal """
    for line in report_lines:
        print(str(line))


def make_report(report_number):
    """ call to create a report file and print to the terminal """
    data = query_db(connection, report_names.get(report_number)[1])
    header = get_report_header(report_names.get(report_number)[0])
    file_name = get_file_name(report_names.get(report_number)[0])
    report_lines = format_rows(header, data)
    print_report(report_lines)
    write_file(file_name, report_lines)

# Try connecting to the database. If we receive an exception, there is no point in continuing
# the program as nothing further can happen.
# Change the connection string as necessary to connect to your DB
try:
    connection = psycopg2.connect("dbname=news user=maitland password=password")
except psycopg2.OperationalError:
    print("Python was unable to connect to news database. The program has exited")
    exit(0)

# for user feedback that the DB is connected!
print("Successfully connected to news database! \n")


# loop runs the program continuously until the user types exit, or a keyboard interrupt has been received.
# It prompts the user to select a report to generate. The results are then fetched from the db, printed to the
# terminal and saved to a text file in the /reports directory.
while True:
    selection = input("Please choose a report or type exit to quit: \n"
                      "  1. Most Popular Authors\n"
                      "  2. Most Viewed Articles\n"
                      "  3. Server Errors\n")

    if selection == '1':
        make_report(selection)

    elif selection == '2':
        make_report(selection)

    elif selection == '3':
        make_report(selection)

    elif selection == 'exit':
        print("Thank you, come again")
        connection.close()
        exit(0)
    else:
        print("\nplease make a valid selection!\n")
