#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base, User


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

    @property
    def add_user(self, email: str, password: str) -> User:
        '''adds a User to db'''

        user = User(email=email, password=password)
        self._session.add(user)
        self._session.commit()
        return user

    @property
    def find_user_by(self, **kwargs) -> User:
        """Takes in arbitrary keyword arguments and returns value"""
        try:
            user = self._session.query(User).filter(kwargs).one()
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

        return user

    def update_user(self, user_id, *args, **kwargs) -> None:
        """Takes arbitrary keyword argument and returns none"""
        """ updates a user """
        valid_keys = ['email', 'id', 'hashed_password',
                      'session_id', 'reset_token']
        user = self.find_user_by(id=user_id)
        for key in kwargs:
            if key not in valid_keys:
                raise ValueError
            user.__setattr__(key, kwargs[key])
        return None
