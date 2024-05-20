import os

def database_exists(db_file):
    return os.path.exists(db_file)
