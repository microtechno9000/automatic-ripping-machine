"""sessions tables

Revision ID: 352b86a5fb63
Revises: 2e0dc31fcb2e
Create Date: 2023-10-29 10:58:43.393375

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '352b86a5fb63'
down_revision = '2e0dc31fcb2e'
branch_labels = None
depends_on = None


def upgrade():
    """
    New Table for Sessions - Session Types
    data type holds the configuration detailing the various ripping methods

    ::structure
    id              [primary_key]
    type            [varchar]
        reference to the function to be called
    name            [varchar]
        Name as defined by the Devs for the specific functions
    description     [varchar]
        Description of what each of the Types do

    ::data
    id  type        name            description
    1   dvd         DVD             ARM will rip new media using handbrake (for DVDs)
    2   Blu-ray     Blu-ray         ARM will rip new media using makemkv (for Blur-ays)
    3   music       Music           ARM will rip new media using abcde (for Music)
    4   data        Data            ARM will rip new media by copying contents
    5   iso         ISO             ARM will rip new media using dd or ddrescue
    """
    new_db_session_type = op.create_table(
        'session_types',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False)
    )
    op.bulk_insert(new_db_session_type,
                   [
                       {
                           'id': 1,
                           'type': "dvd",
                           'name': "DVD",
                           'description': "ARM will rip new media using handbrake (for DVDs)"
                       },
                       {
                           'id': 2,
                           'type': "bluray",
                           'name': "Blu-ray",
                           'description': "ARM will rip new media using makemkv (for Blu-rays)"
                       },
                       {
                           'id': 3,
                           'type': "music",
                           'name': "Music",
                           'description': "ARM will rip new media using abcde (for Music)"
                       },
                       {
                           'id': 4,
                           'type': "data",
                           'name': "Data",
                           'description': "ARM will rip new media by copying contents"
                       },
                       {
                           'id': 5,
                           'type': "iso",
                           'name': "ISO",
                           'description': "ARM will rip new media using dd or ddrescue"
                       }
                   ])

    """
    :session_settings
    table to hold the configuration data foe each of the sessions
    
    ::structure
    id                  [primary_key]
    setting_01_id       [string]
        holds the name of the setting to configure
    setting_01_value    [string]
        holds the value of the setting
    
    ::data
    id                      [primary_key]
    setting_01_id           [varchar]
    setting_01_value        [varchar]
    ...
    setting_nn_value        [varchar]
    setting_nn_value        [varchar]
    """
    # TODO: define the settings config

    new_db_session_settings = op.create_table(
        'session_settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('setting_01_id', sa.String(length=100), nullable=True),
        sa.Column('setting_01_value', sa.String(length=200), nullable=True),
        sa.Column('setting_02_id', sa.String(length=100), nullable=True),
        sa.Column('setting_02_value', sa.String(length=200), nullable=True),
        sa.Column('setting_03_id', sa.String(length=100), nullable=True),
        sa.Column('setting_03_value', sa.String(length=200), nullable=True),
        sa.Column('setting_04_id', sa.String(length=100), nullable=True),
        sa.Column('setting_04_value', sa.String(length=200), nullable=True),
        sa.Column('setting_05_id', sa.String(length=100), nullable=True),
        sa.Column('setting_05_value', sa.String(length=200), nullable=True)
    )
    op.bulk_insert(new_db_session_settings,
                   [
                       {
                           'id': 1,
                           'setting_01_id': "id_01",
                           'setting_01_value': "value_01",
                           'setting_02_id': "id_02",
                           'setting_02_value': "value_02",
                           'setting_03_id': "id_03",
                           'setting_03_value': "value_03",
                           'setting_04_id': "id_04",
                           'setting_04_value': "value_04",
                           'setting_05_id': "id_05",
                           'setting_05_value': "value_05"
                       },
                       {
                           'id': 2,
                           'setting_01_id': "id_01",
                           'setting_01_value': "value_01",
                           'setting_02_id': "id_02",
                           'setting_02_value': "value_02",
                           'setting_03_id': "id_03",
                           'setting_03_value': "value_03",
                           'setting_04_id': "id_04",
                           'setting_04_value': "value_04",
                           'setting_05_id': "id_05",
                           'setting_05_value': "value_05"
                       },
                       {
                           'id': 3,
                           'setting_01_id': "id_01",
                           'setting_01_value': "value_01",
                           'setting_02_id': "id_02",
                           'setting_02_value': "value_02",
                           'setting_03_id': "id_03",
                           'setting_03_value': "value_03",
                           'setting_04_id': "id_04",
                           'setting_04_value': "value_04",
                           'setting_05_id': "id_05",
                           'setting_05_value': "value_05"
                       },
                       {
                           'id': 4,
                           'setting_01_id': "id_01",
                           'setting_01_value': "value_01",
                           'setting_02_id': "id_02",
                           'setting_02_value': "value_02",
                           'setting_03_id': "id_03",
                           'setting_03_value': "value_03",
                           'setting_04_id': "id_04",
                           'setting_04_value': "value_04",
                           'setting_05_id': "id_05",
                           'setting_05_value': "value_05"
                       },
                       {
                           'id': 5,
                           'setting_01_id': "id_01",
                           'setting_01_value': "value_01",
                           'setting_02_id': "id_02",
                           'setting_02_value': "value_02",
                           'setting_03_id': "id_03",
                           'setting_03_value': "value_03",
                           'setting_04_id': "id_04",
                           'setting_04_value': "value_04",
                           'setting_05_id': "id_05",
                           'setting_05_value': "value_05"
                       }
                   ])

    """
    New Table for Sessions - Session Types
    session type holds the user configured session against the data type
    
    ::structure
    id              [primary_key]
    data_type       [foreign_key:data_type->id]
    valid           [boolean]
        true - will execute against 'drive'
        false - normal ARM operation
    settings        [foreign_key:session_settings->id]
    name            [varchar]
    description     [varchar]
    type_settings   [foreign_key:session_settings->id]
        override ARM default settings for the media type and use here

    ::data
    id  data_type   valid   settings   name                description
    01   1           T/F     [x]        Movie - DVD         ARM session to rip DVD movies
    02   2           T/F     [x]        Movie - Blu-ray     ARM session to rip Blur-ay movies
    03   1           T/F     [x]        TV - DVD            ARM session to rip DVD TV Series
    04   2           T/F     [x]        TV - Blu-ray        ARM session to rip Blu-ray TV Series
    05   3           T/F     [x]        Music - MP3         ARM session to rip music as mp3
    06   3           T/F     [x]        Music - flac        ARM session to rip music as flac
    07   4           T/F     [x]        Data                ARM session to rip data disk
    08   1           T/F     [x]        HomeMovie - DVD     ARM session to rip dvd contents but with no title lookup
    09   2           T/F     [x]        HomeMovie - Blu-ray ARM session to rip dvd contents but with no title lookup
    10   5           T/F     [x]        ISO                 ARM session to create ISO using dd
    11   5           T/F     [x]        ISO - Rescue        ARM session to create ISO using ddrescue
    """
    # noinspection PyTypeChecker
    new_db_sessions = op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('type', sa.Integer(), nullable=False),
        sa.Column('valid', sa.Boolean(), nullable=False),
        sa.Column('settings', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.ForeignKeyConstraint(['type'], ['session_types.id']),
        sa.ForeignKeyConstraint(['settings'], ['session_settings.id'])
    )
    op.bulk_insert(new_db_sessions,
                   [
                       {
                           'id': 1,
                           'type': 1,
                           'valid': False,
                           'settings': 1,
                           'name': "Movie - DVD",
                           'description': "ARM session to rip DVD movies"
                       },
                       {
                           'id': 2,
                           'type': 2,
                           'valid': False,
                           'settings': 2,
                           'name': "Movie - Blu-ray",
                           'description': "ARM session to rip Blu-ray movies"
                       },
                       {
                           'id': 3,
                           'type': 1,
                           'valid': False,
                           'settings': 1,
                           'name': "TV - DVD",
                           'description': "ARM session to rip DVD TV Series"
                       },
                       {
                           'id': 4,
                           'type': 2,
                           'valid': False,
                           'settings': 2,
                           'name': "TV - Blu-ray",
                           'description': "ARM session to rip Blu-ray TV Series"
                       },
                       {
                           'id': 5,
                           'type': 3,
                           'valid': False,
                           'settings': 3,
                           'name': "Music - MP3",
                           'description': "ARM session to rip music as mp3"
                       },
                       {
                           'id': 6,
                           'type': 3,
                           'valid': False,
                           'settings': 3,
                           'name': "Music - flac",
                           'description': "ARM session to rip music as flac"
                       },
                       {
                           'id': 7,
                           'type': 4,
                           'valid': False,
                           'settings': 4,
                           'name': "Data",
                           'description': "ARM session to rip data disk"
                       },
                       {
                           'id': 8,
                           'type': 1,
                           'valid': False,
                           'settings': 1,
                           'name': "HomeMovie - DVD",
                           'description': "ARM session to rip dvd contents but with no title lookup"
                       },
                       {
                           'id': 9,
                           'type': 2,
                           'valid': False,
                           'settings': 2,
                           'name': "HomeMovie - Blu-ray",
                           'description': "ARM session to rip dvd contents but with no title lookup"
                       },
                       {
                           'id': 10,
                           'type': 5,
                           'valid': False,
                           'settings': 5,
                           'name': "ISO",
                           'description': "ARM session to create ISO using dd"
                       },
                       {
                           'id': 11,
                           'type': 5,
                           'valid': False,
                           'settings': 5,
                           'name': "ISO - Rescue",
                           'description': "ARM session to create ISO using ddrescue"
                       }]
                   )


def downgrade():
    op.drop_table('session_types')
    op.drop_table('session_settings')
    op.drop_table('sessions')
