# app/database_operations.py

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker, Session


# Define the DatabaseManager class to handle the database connection and queries
class Attorneys:
    def __init__(self, db_url: str):
        # Create the SQLite engine
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        # Create a sessionmaker
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Reflect metadata for the tables
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        # Assume you have a table called 'users' (adjust as per your actual table name)
        self.attorneys_table = self.metadata.tables['professionals']

    # Dependency to get the database session
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # CRUD operation to get all users
    def get_attorneys(self, db: Session, skip: int = 0, limit: int = 10):
        query = select(self.attorneys_table.c.company,
                       self.attorneys_table.c.name,
                       self.attorneys_table.c.designation,
                       self.attorneys_table.c.email,
                       self.attorneys_table.c.phone,
                       self.attorneys_table.c.keyword,
                       self.attorneys_table.c.services,
                       self.attorneys_table.c.weblink).offset(skip).limit(limit)
        return db.execute(query).fetchall()

    # CRUD operation to get a user by ID
    def get_attorney_by_id(self, db: Session, user_id: int):
        query = select([self.attorneys_table]).where(self.attorneys_table.c.id == user_id)
        return db.execute(query).first()
