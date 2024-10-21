import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text, func
from database.models import Professionals

DATABASE_URL = "sqlite:///database/law_firms_data.db"
ENGINE = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=ENGINE)


# Dependency to get the session for FastAPI route handlers
def get_db():
    """
    Dependency for getting the database session in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Attorneys:
    """
    :Title: Class with function to extract data from 3gpp database.
    """

    def __init__(self, db_session: Session):
        """
        Initialize with a database session provided as a dependency.
        """
        self.session = db_session

    def get_companies(self):
        """
        :Title: Funtion to query to 3GPP database to get file content
        :return:
        """
        try:
            query = text(f"SELECT distinct company from professionals;")
            fts_results = self.session.execute(query)
            return fts_results.fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error querying 3GPP database: {str(e)}")
            return []
        finally:
            self.session.close()

    def get_designations(self):
        """
        :Title: Funtion to query to 3GPP database to get file content
        :return:
        """
        try:
            query = text(f"SELECT distinct designation from professionals;")
            fts_results = self.session.execute(query)
            return fts_results.fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error querying 3GPP database: {str(e)}")
            return []
        finally:
            self.session.close()

    def get_attorneys(self, limit: int = 10):
        """
        :Title: Funtion to query to 3GPP database to get file content
        :return:
        """
        try:
            query = text(
                f"SELECT company, name, designation, email, phone, services, weblink from professionals limit {limit};")
            fts_results = self.session.execute(query)
            return fts_results.fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error querying 3GPP database: {str(e)}")
            return []
        finally:
            self.session.close()

    def get_services(self):
        """
        :Title: Funtion to query to 3GPP database to get file content
        :return:
        """
        try:
            query = text(f"SELECT distinct services from professionals;")
            fts_results = self.session.execute(query)
            return fts_results.fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error querying 3GPP database: {str(e)}")
            return []
        finally:
            self.session.close()

    # def insert_data(self, item):
    #     file_ = FilesData(None, item['items'], item['work_group'], item['parent_'], item['main_dir'], item['file_name'],
    #                       item['file_path'], item['file_content'], item['published_at'], None, item['pdf_file'])
    #     try:
    #         self.session.add(file_)
    #         self.session.commit()
    #         logging.warning("Data is Inserted Successfully")
    #
    #     except sqlalchemy.exc.IntegrityError:
    #         logging.warning("Data already Exists")
    #
    #     finally:
    #         self.session.close()

    def __del__(self):
        self.session.close()
