# This is a sample Python script.
import json

import click
import pymysql


@click.command()
@click.option('--config', default="./config.json", help='Path of config file')
@click.option('--args', default=[], help='Args in sql statement')
def main(config, args):
    with open(config, "r") as f:
        config = json.load(f)

        if len(args) > 0:
            config['statement'] = config["sql"].format(*args)
        else:
            config['statement'] = config["sql"]

        for rec in fetch_rows(**config):
            print(rec)


def fetch_rows(**kwargs):
    db = pymysql.connect(host=kwargs['host'],
                         port=kwargs['port'],
                         user=kwargs['user'],
                         passwd=kwargs['password'],
                         db=kwargs['schema'],
                         charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute(kwargs['statement'])
        results = cursor.fetchall()

        for row in results:
            record = {}
            for i, n in enumerate(kwargs['columns']):
                record[n] = row[i]
            yield record
    finally:
        db.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
