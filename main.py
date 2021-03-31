# This is a sample Python script.
import json
import logging

import click
from pandas import read_sql_query
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


@click.command()
@click.option('--config', default='./config.json', help='Path of config file')
@click.option('--name', default='./export', help='Output file name, without extension')
@click.argument('args', nargs=-1)
def main(config, name, args):
    with open(config, 'r') as f:
        config = json.load(f)
        logging.info('Configuration loaded from: {}'.format(config))
        engine = create_engine(config['connection_str'])
        params = dict(arg.split('=') for arg in args)
        logging.info('Prepare to execute SQL: {}'.format(config['sql']))
        logging.info('Parameters: {}'.format(params))
        df = read_sql_query(config['sql'], engine, params=params)
        logging.info('{} records loaded into Dataframe'.format(len(df)))
        if config['format'] == 'h5':
            df.to_hdf(name + '.h5', key='mysql', mode='w')
        elif config['format'] == 'csv':
            df.to_csv(name + '.csv')
        else:
            d = df.to_dict('records')
            with open(name + '.json', 'w') as outfile:
                json.dump(d, outfile)

        logging.info('Exported in {} format with path {}'.format(config['format'], name))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
