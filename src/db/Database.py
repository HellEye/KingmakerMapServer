import sqlite3
from functools import wraps
from sqlite3 import Error

from utils.parser import getPostColumns, getFormattedData, getColumnString

tables = [
    """
    CREATE TABLE IF NOT EXISTS kingdom_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alignment TEXT,
    economy INTEGER,
    stability INTEGER,
    loyalty INTEGER,
    unrest INTEGER,
    consumption INTEGER,
    consumption_modifier INTEGER,
    rulerattributes INTEGER,
    spymasterattributes INTEGER,
    ruler INTEGER,
    consort INTEGER,
    councilor INTEGER,
    general INTEGER,
    granddiplomat INTEGER,
    heir INTEGER,
    highpriest INTEGER,
    magister INTEGER,
    marshal INTEGER,
    royalenforcer INTEGER,
    spymaster INTEGER,
    treasurer INTEGER,
    viceroy INTEGER,
    warden INTEGER,
    treasury INTEGER,
    kingdomId INTEGER REFERENCES kingdoms,
    controldcmod INTEGER NOT NULL,
    extrabp INTEGER NOT NULL,
    expansionedict INTEGER NOT NULL,
    holidayedict INTEGER NOT NULL,
    taxationedict INTEGER NOT NULL,
    recruitmentedict INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS kingdoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT UNIQUE NOT NULL, 
    color TEXT NOT NULL)
    """,
    """
    CREATE TABLE IF NOT EXISTS terrain_type(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL)
    """,
    """
    CREATE TABLE IF NOT EXISTS hex (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    xcoord INTEGER NOT NULL , 
    ycoord INTEGER NOT NULL , 
    owned_by INTEGER NOT NULL REFERENCES kingdoms,
    terrain_type INTEGER REFERENCES terrain_type,
    label TEXT
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS settlement(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hex INTEGER NOT NULL REFERENCES hex)
    """,

    """
    CREATE TABLE IF NOT EXISTS district(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement INTEGER REFERENCES settlement)
    """,
    """
    CREATE TABLE IF NOT EXISTS buildings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL)
    """,
    """
    CREATE TABLE IF NOT EXISTS district_buildings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district INTEGER NOT NULL REFERENCES district,
    building INTEGER NOT NULL REFERENCES buildings,
    xcoord INTEGER NOT NULL,
    ycoord INTEGER NOT NULL,
    rotation INTEGER NOT NULL)
    """,

    """
    CREATE TABLE IF NOT EXISTS improvement(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL )
    """,
    """
    CREATE TABLE IF NOT EXISTS hex_improvement(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    improvement INTEGER NOT NULL REFERENCES improvement,
    hex INTEGER NOT NULL REFERENCES hex)
    """,
    """
    CREATE TABLE IF NOT EXISTS building_discount(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement INTEGER NOT NULL REFERENCES settlement,
    building INTEGER NOT NULL REFERENCES buildings);
    """,
    """
    CREATE TABLE IF NOT EXISTS settlement_improvements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement INTEGER NOT NULL REFERENCES settlement,
    building INTEGER NOT NULL REFERENCES buildings);
    """
    """
    CREATE TABLE IF NOT EXISTS markers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    xcoord INTEGER NOT NULL, 
    ycoord INTEGER NOT NULL,
    color TEXT NOT NULL);
    """

]
startDataCheck = [
    """
    SELECT * FROM terrain_type;
    """,
    """
    SELECT * FROM improvement;
    """,
    """
    SELECT * FROM buildings;
    """,

]
startData = [
    """
    INSERT INTO terrain_type (name)
    VALUES ('Cavern'), ('Desert'), ('Forest'), ('Hills'), 
    ('Jungle'), ('Marsh'), ('Mountains'), ('Plains'), ('Water')
    """,
    """
    INSERT INTO improvement (name)
    VALUES ('Aqueduct'), ('Bridge'), ('Canal'), ('Farm'), ('Fishery'), ('Fort'), ('Highway'),
    ('Mine'), ('Quarry'), ('Road'), ('Sawmill'), ('Watchtower'), ('Lair'), ('Landmark'), ('Resource'), ('River')
    """,
    """
    INSERT INTO buildings (name)
    VALUES ('Academy'), ('Alchemist'), ('Arena'), ('Bank'), ('Bardic College'), ('Barracks'), ('Black Market'), 
    ('Brewery'), ('Bridge'), ('Brothel'), ('Bureau'), ('Casters Tower'), ('Castle'), ('Cathedral'), ('Cistern'),
    ('City Wall'), ('Dump'), ('Everflowing Spring'), ('Exotic Artisan'), ('Foreign Quarter'),
    ('Foundry'), ('Garrison'), ('Granary'), ('Graveyard'), ('GuildHall'), ('Herbalist'), ('Hospital'),
    ('House'), ('Inn'), ('Jail'), ('Library'), ('Luxury Store'), ('Magic Shop'), ('Magical Academy'),
    ('Magical Streetlamps'), ('Mansion'), ('Market'), ('Menagerie'), ('Military Academy'), ('Mill'),
    ('Mint'), ('Moat'), ('Monastery'), ('Monument'), ('Museum'), ('Noble Villa'), ('Observatory'),
    ('Orphanage'), ('Palace'), ('Park'), ('Paved Streets'), ('Pier'), ('Sewer System'), ('Shop'),
    ('Shrine'), ('Smithy'), ('Stable'), ('Stockyard'), ('Tannery'), ('Tavern'), ('Temple'),
    ('Tenement'), ('Theater'), ('Town Hall'), ('Trade Shop'), ('University'), ('Watchtower'),
    ('Watergate'), ('Waterfront'), ('Waterway')
    """
]
database = "src/db/Kingmaker.sqlite"


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
    return conn


def withConnection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['connection'] = create_connection()
        out = func(*args, **kwargs)
        kwargs['connection'].close()
        return out

    return wrapper


def commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        kwargs['connection'].commit()
        return out

    return wrapper



@withConnection
def createTables(connection):
    cursor = connection.cursor()
    for query in tables:
        cursor.execute(query)


@withConnection
def insertData(connection):
    tableEmpty = []
    cursor:sqlite3.Cursor = connection.cursor()
    for i in range(len(startDataCheck)):
        cursor.execute(startDataCheck[i])
        data = cursor.fetchall()
        tableEmpty.append(len(data) == 0)
    for i in range(len(startData)):
        if tableEmpty[i]:
            cursor.execute(startData[i])
            connection.commit()


@withConnection
def get(table: str, columns=None, query=None, connection=None):
    out:sqlite3.Row= connection \
        .execute(f"SELECT {getColumnString(columns)} FROM {table} {'' if query is None else 'WHERE ' + query}")\
        .fetchall()
    return out


@withConnection
@commit
def put(table, data, columns, connection: sqlite3.Connection = None):
    # print(f"INSERT INTO {table} {getColumnString(columns)} VALUES {getFormattedData(data)}")
    out=connection \
        .execute(f"INSERT INTO {table} {getColumnString(columns)} VALUES {getFormattedData(data)}")
    return out.lastrowid


@withConnection
@commit
def post(table, data, columns, query, connection=None):
    print(f"UPDATE {table} SET {getPostColumns(data, columns)} WHERE {query}")
    id=connection.execute(f"SELECT id FROM {table} WHERE {query}").fetchall()
    out=connection \
        .execute(f"UPDATE {table} SET {getPostColumns(data, columns)} WHERE {query}")
    return id[0][0]


@withConnection
@commit
def delete(table, query, connection=None):
    connection \
        .execute(f"DELETE FROM {table} WHERE {query}")
    return None


if __name__ == '__main__':
    database = "Kingmaker.sqlite"
    createTables()
    insertData()
    # print(get("improvement"))
    # print(connection.execute("SELECT * FROM auth_group").fetchall())
