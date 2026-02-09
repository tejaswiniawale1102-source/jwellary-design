import oracledb

def get_connection():
    return oracledb.connect(
        user="system",
        password="system",
        host="localhost",
        port=1521,
        service_name="XEPDB1"
    )
