import os
import joblib
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.exc import IntegrityError
from API_call import API_call

class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    """
    Custom class for instantiating a SQL Alchemy connection. Configured here for SQLite, but intended to be flexible.
    Credit to Medium user Mahmud Ahsan:
    https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32
    """
    DB_ENGINE = {
       'sqlite': 'sqlite:////{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype, 
                 username='', password='', 
                 dbname='',path=os.getcwd()+'/'):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=path+dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
            
            self.Base = declarative_base(bind=self.db_engine)
            self.meta = self.Base.metadata
        else:
            print("DBType is not found in DB_ENGINE")
            
    def delete_game(self,gamePk):
        tables = [ 
            table.name for table in self.meta.tables.values()
            if 'gamePk' in table.c
        ]
        
        [ self.db_engine.execute(
            f"delete from {table} where gamePk={gamePk}"
        ) for table in tables ]
        
        self.db_engine.execute(f"delete from games where pk = {gamePk}")  
    
    def insert_game(self,gamePk,replace=False,return_status=False):
        gamePk = int(gamePk)
        
        status_report = []
        conn = self.db_engine.connect()
        
        if replace:
            self.delete_game(gamePk)

        q = self.db_engine.execute('select pk from games').fetchall()
        existing_pks = [x[0] for x in q]

        if gamePk in existing_pks:
            status_report.append( 
                {'game':gamePk,
                 'insert_status':'pass',
                 'reason':'already exists'}
            )
        else:
            try:
                call = API_call(gamePk)
            except:
                status_report.append(
                    {'game':gamePk,
                     'insert_status':'fail',
                     'reason':'API call failed'}
                )

                return status_report

            for table in self.meta.tables.values():
                #table = self.meta.tables[table_name]
                cols = [x.name for x in table.c]


                records = call.__dict__[table.name]

                insert_values = []
                for record in records:
                    insert_value = {}
                    for k in cols:
                        try:
                            insert_value[k]=record[k]
                        except KeyError:
                            insert_value[k]=None
                    insert_values.append(insert_value)

                initial_count = (
                    conn.execute(
                        f'select count(*) from {table.name}'
                    ).fetchall()[0][0]
                )

                try:
                    conn.execute(table.insert(),insert_values)

                    after_count = (
                        conn.execute(
                            f'select count(*) from {table.name}'
                        ).fetchall()[0][0]
                    )

                    status_report.append( 
                        {'game':gamePk,
                         'table':table.name,
                         'insert_status':'success',
                         'records_count':len(records),
                         'records_added':after_count-initial_count,
                         'reason':'None'})

                except IntegrityError:
                    status_report.append( 
                        {'game':gamePk,
                         'table':table.name,
                         'insert_status':'fail',
                         'reason':'Integrity Error'}
                    )
        if conn.closed == False:
            conn.close()
        if return_status:
            return status_report 
    
    def pd_query(self,statement=None,name=None,storage_path='sql_queries/',load=False):
        
        if statement:
            result = pd.read_sql(statement,self.db_engine)
        
        # if a name is specified, pickle the results and store
        if name != None:
            if load:
                result = joblib.load(storage_path+name+'.pkl')['result']
            else:
                storage_dict = {'result':result,'statement':statement}
                joblib.dump(storage_dict,storage_path+name+'.pkl')
            return result
    
# ###################

# ## RELATIONSHIPS ##

# ###################






# Play.pitchData = relationship(
#     'PitchData', order_by=PitchData.index, back_populates='play')
# PitchData.play = relationship('Play',back_populates='pitchData')


# Pitch.pitchData = relationship(
#     'PitchData',back_populates='pitch',uselist=False)
# PitchData.pitch = relationship(
#     'Pitch',back_populates='pitchData',viewonly=True)


