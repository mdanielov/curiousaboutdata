from db_layer import get_dbtype
import db_repository as dbnull
import db_repository_mssql as ms
import db_repository_pgpsql as pg
import logging

def get_repository():
    dbtype = get_dbtype()
    dbs = {
        'mssql': ms.dbMSSQL
        , 'postgresql': pg.dbPGSQL
    }
    # logging.info( 'get_repository: ' + str(dbtype))
    return dbs.get( dbtype, dbnull.dbSQL)
