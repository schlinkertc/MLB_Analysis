import os
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
    
    def insert_game(self,gamePk,method='IGNORE'):
        gamePk = int(gamePk)
        
        if method == 'IGNORE':
            q = self.db_engine.execute('select pk from games').fetchall()
            existing_pks = [x[0] for x in q]

            if gamePk in existing_pks:
                return {'game':gamePk,
                        'insert_status':'fail',
                        'reason':'already exists'}
            else:
                try:
                    call = API_call(gamePk)
                except:
                    return {'game':gamePk,
                            'insert_status':'fail',
                            'reason':'API call failed'}

                for table_name in self.meta.tables.keys():
                    table = self.meta.tables[table_name]
                    cols = [x.name for x in table.c]
                    
                    if table_name in ['hit_data','pitch_data']:
                        records = call.__dict__['pitches']
                    else:
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

                    conn = self.db_engine.connect()    
                    try:
                        conn.execute(table.insert(),insert_values)
                        return {'game':gamePk,
                                'table':table_name,
                                'insert_status':'success',
                                'reason':'None'}
                    except IntegrityError:
                        return {'game':gamePk,
                                'table':'table_name'
                                'insert_status':'fail',
                                'reason':'Integrity Error'}
        if method == 'REPLACE':
            return 'replace method needs to be done!'    
    
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


