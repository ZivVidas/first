from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# this one is for sqlite3
# db_url = 'sqlite:///./todo.db'

# this one is for postgress
# db_url = 'postgresql://postgres:zz2828@localhost/todo'
db_url = 'postgresql://gflpoptp:r2clggYVe9EK8UsumhwB2Ln-99WRWMpH@flora.db.elephantsql.com/gflpoptp'
# for sqlite
# engine = create_engine(db_url,connect_args={'check_same_thread':False})

# for postgres
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


