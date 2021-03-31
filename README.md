# py-mysql-export

# Config File

path: ./config.json {
"connection_str": "mysql+pymysql://user:password@host:port/db",
"sql": "select cola, col2, col3 from table_a where cola = %(para)s",
"format": "h5"
}

Usage: main.py [OPTIONS] [ARGS]...

Options:
--config TEXT Path of config file, default "./config.json"
--name TEXT Output file name, without extension, default "./export.[format]"
--help Show this message and exit.

Example:

python main.py para=val

reading ./config.json and export the file "./export"