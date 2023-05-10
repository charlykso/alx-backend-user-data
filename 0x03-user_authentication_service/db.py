"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import User
from user import Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        :param email: The user's email address
        :param hashed_password: The user's hashed password
        :return: The newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the given filter criteria.

        :param kwargs: Keyword arguments specifying the filter criteria
        :return: The first User object matching the filter criteria
        :raises NoResultFound: If no results are found
        :raises InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound()
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database based on the given
        user_id and attribute values.

        :param user_id: The ID of the user to update
        :param kwargs: Keyword arguments specifying the new attribute values
        :return: None
        :raises NoResultFound: If no user is found with the given user_id
        :raises ValueError: If an argument that does not correspond
        to a user attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound as e:
            raise e

        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError()
        self._session.commit()
