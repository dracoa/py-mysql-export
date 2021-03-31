# This is a sample Python script.
import json

import click


@click.command()
@click.option('--config', default="./config.json", help='Path of config file')
@click.option('--args', default=[], help='Args in sql statement')
def main(config, args):
    # Use a breakpoint in the code line below to debug your script.
    print(args)
    with open(config, "r") as f:
        config = json.load(f)
        # db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")
        print(config["host"])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
