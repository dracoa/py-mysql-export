# This is a sample Python script.
import json
import logging
from abc import ABC, abstractmethod

import click
import pymysql

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class Exporter(ABC):
    @abstractmethod
    def insert(self, rec):
        pass

    @abstractmethod
    def export(self):
        return


class JsonExporter(Exporter):
    def __init__(self):
        self.list = []

    def insert(self, rec):
        self.list.append(rec)

    def export(self):
        return json.dumps(self.list)


@click.command()
@click.option('--config', default="./config.json", help='Path of config file')
@click.option('--args', help='Args in sql statement')
def main(config, args):
    with open(config, "r") as f:
        config = json.load(f)
        if args is not None:
            config['args'] = args.split(",")
        else:
            config['args'] = []
        exporter = JsonExporter()
        for rec in fetch_rows(**config):
            exporter.insert(rec)
        done = exporter.export()
        print(done)


def fetch_rows(**kwargs):
    db = pymysql.connect(host=kwargs['host'],
                         port=kwargs['port'],
                         user=kwargs['user'],
                         passwd=kwargs['password'],
                         db=kwargs['schema'],
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = db.cursor()
        logging.info('connected to database...')
        logging.info('execute sql: {}'.format(kwargs['sql']))
        logging.info('sql args: {}'.format(kwargs['args']))
        num = cursor.execute(kwargs['sql'], kwargs['args'])
        results = cursor.fetchall()
        logging.info('fetched {} rows'.format(num))
        for row in results:
            yield row
    finally:
        db.close()
        logging.info('database disconnected')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
