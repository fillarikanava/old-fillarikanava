from django.conf import settings
from django.db import connection
from django.db.transaction import commit, commit_manually
from _mysql_exceptions import ProgrammingError
from logging import info
from os import listdir, path

import logging, re, subprocess, sys


def read_schema_version():
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT MAX(version) FROM schema_version WHERE site_id=%s',
                       [str(settings.SITE_ID)])
        return int((cursor.fetchone() or [-1])[0])
    except ProgrammingError, e:
        code, msg = e.args
        if code != 1146:
            raise
    return -1

@commit_manually
def handle_sql(version, schema, data):
    mysql_apply(schema)
    # update database version
    cursor = connection.cursor()
    cursor.execute('INSERT INTO schema_version (site_id, version) VALUES (%s, %s)',
                   [str(settings.SITE_ID), str(version)])
    commit()
    if data:
        info("%s: inserting test data" % path.basename(data))
        mysql_apply(data)

_handlers = {
    'sql': handle_sql,
}

def get_migration_files(schema_dir, test_dir):
    """Returns a generator of (ver, file ext, schema_file, data_file) tuples.

    File extension either 'sql' or 'py'.
    """
    schema_re = re.compile(r'(\d+)(?:\-.+)?\.((%s))' % ')|('.join(_handlers.keys()))
    migrations = \
        [(int(match.group(1)), match.group(2), schema_file)
         for (match, schema_file) in
            [(schema_re.match(file), path.join(schema_dir, file)) for file in listdir(schema_dir)]
         if match]
    def file_or_none(p):
        return path.isfile(p) and path.abspath(p) or None
    return \
        [(ver, ext, schema_file, file_or_none(path.join(test_dir, '%d.sql' % ver)))
         for ver, ext, schema_file in migrations]

def get_migrations_for(version, sqldir):
    migrations = get_migration_files(sqldir, path.join(sqldir, 'testdata'))

    # sort ascending
    migrations.sort(lambda m1, m2: m1[0] - m2[0])

    if migrations and migrations[-1][0] < version:
        raise Exception('Database schema is newer than migration files! (Db v.%d, latest migration file v.%d)' \
                        % (version, migrations[-1][0]))

    # filter out all but newer versions (after sorting because of that version consistency check)
    return [m for m in migrations if m[0] > version]

def mysql_apply(file):
    """Need to run migration files using the mysql command line client."""
    info("Applying file '%s'" % path.basename(file))
    errcode = subprocess.call(['mysql',
                               '--user=%s' % settings.DATABASE_USER,
                               '--password=%s' % settings.DATABASE_PASSWORD,
                               '--host=%s' % settings.DATABASE_HOST,
                               settings.DATABASE_NAME,
                               '-e \. %s' % file])
    if errcode:
        raise Exception("MySQL client error %i: Failed to apply file '%s'" \
                        % (errcode, file))

def apply_migrations(migrations, skip_test_data=False):
    for ver, ext, schema, data in migrations:
        def default_handler(*args):
            raise Exception("%s: Unsupported migration file type '%s'" % (schema, ext))
        _handlers.get(ext, default_handler)(ver, schema, not skip_test_data and data)

def do_migrations(sqldir, skip_test_data):
    version = read_schema_version()
    migrations = get_migrations_for(version, sqldir)
    if not migrations:
        info("Database is up to date at version %d" % version)
    else:
        info("Applying %i schema migration files, from %i to %i" \
             % (len(migrations), migrations[0][0], migrations[-1][0]))
        apply_migrations(migrations, skip_test_data)
        info("Migration successful")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    argv = sys.argv[1:]
    if not argv:
        print "Usage: %s sqldir" % path.basename(__file__)
        sys.exit(1)
    sqldir = path.abspath(argv.pop(0))
    info("Site id %i, using migrations directory '%s'" % (settings.SITE_ID, sqldir))
    if argv:
        logging.warn('Ignoring unrecognized parameters:', ', '.join(argv))
    do_migrations(sqldir, True)
