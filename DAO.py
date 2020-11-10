from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement
import pandas as pd
import numpy as np


class SensorsDAO:

    # Statements
    insert_stmt = None
    insert_stats_stmt = {}
    get_data_single_stmt = None
    get_data_single_stmt_spCol = None #specific columns
    get_data_range_stmt = None
    get_stats_stmt = {}

    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = 'sensors'
        self.create_session()


    def __del__(self):
        self.cluster.shutdown()

    def create_session(self):
        self.cluster = Cluster(protocol_version=4)
        self.session = self.cluster.connect(self.keyspace)
        self.session.row_factory = pandas_factory
        self.session.default_fetch_size = None
        self.prepare_stmts()
        
    def prepare_stmts(self):
        """
        Prepare CQL statements
        """
        SensorsDAO.insert_stmt = self.get_session().prepare(
            "INSERT INTO sensors_data (ip,name,date,datetime, temperature , relative_humidity , dew_point , co2_level ) values ( ?,?,?,?,?,?,?,?)")

        SensorsDAO.insert_stats_stmt = {
                "co2_level": self.get_session().prepare("INSERT INTO co2_level (date,ip,name,peak,mean,std ) values ( ?,?,?,?,?,?)"),
                "dew_point": self.get_session().prepare("INSERT INTO dew_point (date,ip,name,peak,mean,std ) values ( ?,?,?,?,?,?)"),
                "relative_humidity": self.get_session().prepare("INSERT INTO relative_humidity (date,ip,name,peak,mean,std ) values ( ?,?,?,?,?,?)"),
                "temperature": self.get_session().prepare("INSERT INTO temperature (date,ip,name,peak,mean,std ) values ( ?,?,?,?,?,?)") }

        SensorsDAO.get_data_single_stmt = self.get_session().prepare("select * from sensors_data where date = ?")

        SensorsDAO.get_data_single_stmt_spCol = self.get_session().prepare(
            "select ip,datetime,co2_level,dew_point,name,relative_humidity,temperature from sensors_data where date = ?")

        SensorsDAO.get_data_range_stmt = self.get_session().prepare(
            "select ip,datetime,co2_level,dew_point,name,relative_humidity,temperature from sensors_data where date >= ? AND date <= ? ALLOW FILTERING")
        
        SensorsDAO.get_stats_stmt = {
            "co2_level": "select * from sensors.co2_level",
            "dew_point": "select * from sensors.dew_point",
            "relative_humidity": "select * from sensors.relative_humidity",
            "temperature": "select * from sensors.temperature",
            }

    def get_session(self):
        return self.session

    def get_data_single_spCol(self, date):
        """
        retreive data from single date with specific columns
        """
        return self.get_session().execute(SensorsDAO.get_data_single_stmt_spCol, [date])._current_rows

    def get_data_single(self, date):
        """
        retreive data from single date with specific columns
        """
        return self.get_session().execute(SensorsDAO.get_data_single_stmt, [date])._current_rows
        
    def get_data_range(self, start_date, end_date):
        """
        retrieve data within date range
        """
        return self.get_session().execute(SensorsDAO.get_data_range_stmt, [start_date,end_date])._current_rows

    def get_stats(self,source):
        """
        Get statistics data
        """
        return self.get_session().execute(SensorsDAO.get_stats_stmt[source])._current_rows

    def insert_data(self,data):
        """
        Insert sensor data into DB
        """
        self.get_session().execute(SensorsDAO.insert_stmt,data)

    def insert_stats(self,df):
        """
        Insert statistics data into DB
        """
        for i in SensorsDAO.insert_stats_stmt:
            for key,grp in df.groupby(['ip','date','name']):
                self.get_session().execute(SensorsDAO.insert_stats_stmt[i],[key[1],key[0],key[2],np.max(grp[i]),np.mean(grp[i]),np.std(grp[i]) ] )

def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
