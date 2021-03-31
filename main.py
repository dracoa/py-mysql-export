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
            statement = config["sql"].format(*args)
        else:
            statement = config["sql"]

        for rec in fetch_rows(config["host"], config["port"], config["user"], config["password"],
                              config["schema"], statement, config["columns"]):
            print(rec)


def fetch_rows(host="127.0.0.1", port=3306, user="root", passwd="", db='mysql',
               statement="SELECT now() as server_time", columns=['server_time']):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        for row in results:
            record = {}
            for i, n in enumerate(columns):
                record[n] = row[i]
            yield record
    finally:
        db.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
