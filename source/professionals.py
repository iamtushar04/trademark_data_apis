import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text, func
from database.models import Professionals

DATABASE_URL = "sqlite:///database/law_firms_data.db"
ENGINE = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=ENGINE)


def clean(data):
    import pdb;
    pdb.set_trace()
    data = [val[0].strip() for val in data if val not in (None, '')]
    return data


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
            data = fts_results.fetchall()
            return clean(data)
        except SQLAlchemyError as e:
            logging.error(f"Error querying 3GPP database: {str(e)}")
            return []
        finally:
            self.session.close()

    # def get_attorneys(self, limit: int = 10):
    #     """
    #     :Title: Funtion to query to 3GPP database to get file content
    #     :return:
    #     """
    #     try:
    #         query = text(
    #             f"SELECT company, name, designation, email, phone, services, weblink from professionals limit 100;")
    #         fts_results = self.session.execute(query)
    #         return fts_results.fetchall()
    #     except SQLAlchemyError as e:
    #         logging.error(f"Error querying 3GPP database: {str(e)}")
    #         return []
    #     finally:
    #         self.session.close()
    def get_attorneys(self,
                      company: Optional[str] = None,
                      designation: Optional[str] = None,
                      keyword: Optional[str] = None,
                      limit: int = 10
                      ):
        """
        Function to query the professionals table to get filtered users
        based on company, designation, and service.
        """
        try:
            # Base query to fetch users
            query = f"SELECT company, name, designation, email, phone, services, weblink FROM professionals"

            # Dynamic query construction based on provided parameters
            filters = []
            if company:
                filters.append(f"company LIKE '%{company}%'")
                # filters.append(f"company in ({', '.join(company)})")
            if designation:
                filters.append(f"designation = :designation")
                # filters.append(f"designation in ({', '.join(company)})")
            if keyword:
                filters.append(f"description LIKE : '%{keyword}%'")

            # Add filters to query if any
            if filters:
                query += " WHERE " + " AND ".join(filters)

            # Limit the number of results
            # query += f" LIMIT :limit"
            # Prepare the SQL statement
            statement = text(query)
            print(query)
            # Execute the query with the parameters
            fts_results = self.session.execute(
                statement,
                {"company": company, "designation": designation, "keyword": keyword}
                # {"company": company, "designation": designation, "keyword": keyword, "limit": limit}
            )
            return fts_results.fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error querying database: {str(e)}")
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

    def add_attorney(self, user_data: dict):
        """Function to insert a new user record into the professionals table."""
        try:
            new_professional = Professionals(**user_data)
            self.session.add(new_professional)
            self.session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error adding user to the database: {str(e)}")
            self.session.rollback()  # Rollback the transaction in case of error
            raise e

    def __del__(self):
        self.session.close()
