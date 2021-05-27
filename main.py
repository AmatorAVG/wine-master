from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime, pandas
import argparse, collections

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    parser = argparse.ArgumentParser(description='Программа наполнения сайта вин')
    parser.add_argument('--path', help='Путь к таблице вин', default='wine_example.xlsx')
    args = parser.parse_args()

    catalog = pandas.read_excel(args.path, keep_default_na=False, na_values=None).to_dict(orient='records')
    drinks_by_categories = collections.defaultdict(list)

    for product in catalog:
        drinks_by_categories[product['Категория']].append(product)

    rendered_page = template.render(
        age=(datetime.datetime.now().year - 1920),
        drinks_by_categories=drinks_by_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()