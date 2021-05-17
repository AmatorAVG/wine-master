from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime, pandas
from pprint import pprint

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

event1 = datetime.datetime(year=1920, month=1, day=1, hour=0)
event2 = datetime.datetime.now()
delta = event2-event1

excel_data_df = pandas.read_excel('~/devman/wine3.xlsx', keep_default_na=False)
raw_dict = excel_data_df.to_dict(orient='records')

categories = excel_data_df.groupby('Категория').groups

for key in categories:
    new_val = []
    for el in categories[key]:
        new_val.append(raw_dict[el])
    categories[key] = new_val

pprint(categories)

rendered_page = template.render(
    time_text=(delta.days // 365),
    categories=categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

