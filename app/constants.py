SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")
SQLALCHEMY_DATABASE_URI_FORMAT = SQLALCHEMY_DATABASE_URI.format(
        USER="user_name",
        PASSWORD="password",
        ADDR="localhost",
        PORT=3306,
        NAME="testdb"
    )
