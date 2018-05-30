import psycopg2
from datetime import date
ques_1 = "What are the most popular articles of all time?"

p_articles = ("SELECT title, count(*) as views FROM articles \n"
              "join log\n"
              "on articles.slug = substring(log.path, 10)\n"
              "group by title ORDER BY views DESC LIMIT 3;")

ques_2 = "Who are the most popular article authors of all time?"

p_authors = ("select authors.name, count(*) as views\n"
             "from articles \n"
             "join authors\n"
             "on articles.author = authors.id \n"
             "join log \n"
             "on articles.slug = substring(log.path, 10)\n"
             "where log.status LIKE '200 OK'\n"
             "group by authors.name ORDER BY views DESC;")

ques_3 = "On which days more than 1% of the requests led to error?"


p_errors = """
           select * from (
           select a.day,
           round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
           as errp from
           (select date(time) as day, count(*) as hits
           from log group by day) as a
           inner join
           (select date(time) as day, count(*) as hits from log where status
           like '%404%' group by day) as b
           on a.day = b.day)
           as t where errp > 1.0
           """
# Connect to the database and feed query to extract results


def get_output(data):
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute(data)
    implement = c.fetchall()
    db.close()
    return implement

r1 = get_output(p_articles)
r2 = get_output(p_authors)
r3 = get_output(p_errors)


# Create a function to print query results


def print_solution(a):
    for i in range(len(a)):
        title = a[i][0]
        res = a[i][1]
        print("%s - %d" % (title, res) + " views")
    print("\n")

print(ques_1)
print_solution(r1)
print(ques_2)
print_solution(r2)
print(ques_3)


def errors_percentage():
    for i, j in r3:
        print("""{0: %B %d, %Y} -- {1: .2f} % errors""".format(i, j))
errors_percentage()
