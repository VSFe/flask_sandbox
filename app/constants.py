SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")
SQLALCHEMY_DATABASE_URI_FORMAT = SQLALCHEMY_DATABASE_URI.format(
        USER="test",
        PASSWORD="VSFe03025!",
        ADDR="localhost",
        PORT=3306,
        NAME="testdb"
    )