from configparser import ConfigParser


def config(
    filename="/Users/Knewt/myProjects/db_project/config/database.ini",
    section="postgres",
):
    # create a parser
    parser = ConfigParser(interpolation=None)
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file.".format(section, filename)
        )
    return db
