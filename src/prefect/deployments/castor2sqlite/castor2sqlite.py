import os
import logging

from prefect import flow, task
from pysqlite3 import dbapi2 as sqlite3
from datetime import datetime
from barbell2_castor.api import CastorApiClient
# from barbell2_castor import CastorToSqlite3

logging.basicConfig()
logger = logging.getLogger(__name__)


STUDY_DPCA = 'ESPRESSO_v2.0_DPCA'
STUDY_DHBA = 'ESPRESSO_v2.0_DHBA'
CLIENT_ID_FILE = os.path.join(os.environ['HOME'], 'castorclientid.txt')
if not os.path.isfile(CLIENT_ID_FILE):
    raise RuntimeError(f'Castor client ID file {CLIENT_ID_FILE} does not exist!')
CLIENT_ID = open(CLIENT_ID_FILE, 'r').readline().strip()
CLIENT_SECRET_FILE = os.path.join(os.environ['HOME'], 'castorclientsecret.txt')
if not os.path.isfile(CLIENT_SECRET_FILE):
    raise RuntimeError(f'Castor client secret file {CLIENT_SECRET_FILE} does not exist!')
CLIENT_SECRET = open(CLIENT_SECRET_FILE, 'r').readline().strip()
OUTPUT_DB_FILE_DPCA = '/tmp/castor/dpca.db'
OUTPUT_DB_FILE_DHBA = '/tmp/castor/dhba.db'
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class CastorToDict:

    def __init__(
            self,
            study_name, 
            client_id, 
            client_secret, 
            log_level=logging.INFO, 
            ):
        self.study_name = study_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.log_level = log_level
        logging.root.setLevel(self.log_level)
        self.data = {}

    def execute(self):
        client = CastorApiClient(self.client_id, self.client_secret)
        study = client.get_study(self.study_name)
        study_id = client.get_study_id(study)
        self.data = client.get_study_data(study_id)
        return self.data


class DictToSqlite3:

    CASTOR_TO_SQL_TYPES = {
        'string': 'TEXT',
        'textarea': 'TEXT',
        'radio': 'TINYINT',
        'dropdown': 'TINYINT',
        'numeric': 'FLOAT',
        'date': 'DATE',
        'year': 'TINYINT',
    }

    def __init__(
            self, 
            data,
            output_db_file='castor.db', 
            add_timestamp=False,
            log_level=logging.INFO, 
            ):
        self.data = data
        self.output_db_file = output_db_file
        if add_timestamp:
            items = os.path.splitext(self.output_db_file)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.output_db_file = f'{items[0]}-{timestamp}{items[1]}'
        self.log_level = log_level
        logging.root.setLevel(self.log_level)

    @staticmethod
    def get_sql_object_for_field_data(field_data, i):
        value = field_data['field_values'][i]
        if (field_data['field_type'] == 'radio' or field_data['field_type'] == 'dropdown' or field_data['field_type'] == 'year') and value != '':
            try:
                return int(value)
            except ValueError:
                print('ValueError (int): name={}, value={}'.format(field_data['field_variable_name'], value))
        if field_data['field_type'] == 'numeric' and value != '':
            try:                
                return float(value)
            except ValueError:
                print('ValueError (float): name={}, value={}'.format(field_data['field_variable_name'], value))
        if field_data['field_type'] == 'date' and value != '':
            try:
                return datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                print('ValueError (date): name={}, value={}'.format(field_data['field_variable_name'], value))
        return str(field_data['field_values'][i])

    def generate_list_of_sql_statements_for_inserting_records(self, data):
        nr_records = len(data[list(data.keys())[0]]['field_values'])
        logger.info(f'nr. records: {nr_records}')
        placeholders = []
        values = []
        for i in range(nr_records):
            placeholder = 'INSERT INTO data ('
            value = []
            for field_name in data.keys():
                placeholder += field_name + ', '
            placeholder = placeholder[:-2] + ') VALUES ('
            for field_name in data.keys():
                value.append(self.get_sql_object_for_field_data(data[field_name], i))
                placeholder += '?, '
            placeholder = placeholder[:-2] + ');'
            placeholders.append(placeholder)
            values.append(value)
        return placeholders, values
    
    def generate_sql_field_from_field_type_and_field_name(self, field_type, field_name):
        return '{} {}'.format(field_name, DictToSqlite3.CASTOR_TO_SQL_TYPES[field_type])

    def generate_sql_for_creating_table(self, data):
        logger.info(f'nr. columns: {len(data.keys())}')
        sql = 'CREATE TABLE data (id INTEGER PRIMARY KEY, '
        for field_name in data.keys():
            field_type = data[field_name]['field_type']
            field_type_sql = self.generate_sql_field_from_field_type_and_field_name(field_type, field_name)
            if field_type_sql is not None:
                sql += field_type_sql + ', '
        sql = sql[:-2] + ');'
        return sql

    @staticmethod
    def generate_sql_for_dropping_table():
        return 'DROP TABLE IF EXISTS data;'

    def create_sql_database(self, data):
        conn = None
        try:
            conn = sqlite3.connect(self.output_db_file)
            cursor = conn.cursor()
            cursor.execute(self.generate_sql_for_dropping_table())
            cursor.execute(self.generate_sql_for_creating_table(data))
            placeholders, values = self.generate_list_of_sql_statements_for_inserting_records(data)
            for i in range(len(placeholders)):
                cursor.execute(placeholders[i], values[i])
            conn.commit()
        except sqlite3.Error as e:
            logger.error(e)
        finally:
            if conn:
                conn.close()

    def execute(self):
        self.create_sql_database(self.data)
        return self.output_db_file
    

class CastorToSqlite3:

    def __init__(
            self,
            study_name,
            client_id,
            client_secret,
            output_db_file='castor.db',
            add_timestamp=False,
            log_level=logging.INFO, 
            ):
        self.castor2dict = CastorToDict(study_name, client_id, client_secret, log_level)        
        self.output_db_file = output_db_file
        self.add_timestamp = add_timestamp        
        self.log_level = log_level
        logging.root.setLevel(self.log_level)

    def execute(self):
        data = self.castor2dict.execute()
        dict2sqlite = DictToSqlite3(data, self.output_db_file, self.add_timestamp, self.log_level)
        return dict2sqlite.execute()


@task(name='extract_dpca')
def extract_dpca():
    extractor = CastorToSqlite3(
        STUDY_DPCA, 
        CLIENT_ID, 
        CLIENT_SECRET, 
        output_db_file=OUTPUT_DB_FILE_DPCA,
        add_timestamp=False,
    )
    extractor.execute()


@task(name='extract_dhba')
def extract_dhba():
    extractor = CastorToSqlite3(
        STUDY_DHBA, 
        CLIENT_ID, 
        CLIENT_SECRET, 
        output_db_file=OUTPUT_DB_FILE_DHBA,
        add_timestamp=False,
    )
    extractor.execute()


@flow(name='castor2sqlite')
def castor2sqlite():
    extract_dpca()
    extract_dhba()


if __name__ == '__main__':
    castor2sqlite()
