import psycopg2
import datetime

report_names = {"1": ["Top Authors", "SELECT name, article_views FROM author_rank"],
                "2": ["Most Viewed Articles", "SELECT title, views FROM article_top3"],
                "3": ["Server Errors", "SELECT percent_of_errors, request_date FROM high_error_dates"]}


def get_report_header(report_name):
    header = []
    date = str(datetime.datetime.now().replace(microsecond=0))
    header.append("Report Name: {}{}".format(report_name, "\n"))
    header.append("Report Generated: {}{}".format(date, "\n"))
    return header


def get_file_name(report_name):
    return "{}{}{}".format(report_name, "-", str(datetime.datetime.now().date()))


def query_db(conn, query):
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()


def format_rows(header, data):
    report_lines = []

    for line in header:
        report_lines.append(line)

    for item in data:
        for t in item:
            line = "{}{}{}{}".format(t[0],  "  Views --", t[1], "\n")
            report_lines.append(line)
    return report_lines


def write_file(file_name, report_lines):
    with open(file_name) as report:
        for line in report_lines:
            report.write(line)


def print_report(report_lines):
    for line in report_lines:
        print(str(line))

try:
    connection = psycopg2.connect("dbname=news user=maitland password=password")
except psycopg2.OperationalError:
    print("Python was unable to connect to news database. The program has exited")
    exit(0)


print("Successfully connected to news database")

while True:
    selection = input("Please choose a report or type exit to quit: \n"
                      "  1. Most Popular Authors\n"
                      "  2. Most Viewed Articles\n"
                      "  3. Server Errors\n")

    if selection == '1':
        data = query_db(connection, report_names.get('1')[1])
        header = get_report_header(report_names.get('1')[0])
        file_name = get_file_name(report_names.get('1')[0])
        report_lines = format_rows(header, data)
        print_report(report_lines)
        write_file(file_name, report_lines)

    elif selection == '2':
        print("selection 2")
    elif selection == '3':
        print("selection 3")
    elif selection == 'exit':
        print("Thank you, come again")
        connection.close()
        exit(0)
    else:
        print("\nplease make a valid selection!\n")