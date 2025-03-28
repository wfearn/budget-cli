from abc import ABC, abstractmethod
from datetime import datetime
import os
import sqlite3
from typing import Any


default_database_location = os.path.join(
    os.environ['HOME'],
    '.pybudget',
    'transactions.db'
 )


class InvalidTransactionError(Exception):
    pass


class TransactionObject(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _get_input_data_format(self) -> list[Any]:
        raise NotImplementedError


class StorageManager(ABC):
    @abstractmethod
    def get_transactions(self) -> list[TransactionObject]:
        raise NotImplementedError

    @abstractmethod
    def create_transaction(self, t: TransactionObject) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_transaction(
        self,
        old_transaction: TransactionObject,
        new_transaction: TransactionObject
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_transaction(self, tid: str) -> TransactionObject:
        raise NotImplementedError

    @abstractmethod
    def load_new_transactions(self, path: str) -> bool:
        raise NotImplementedError


class DatabaseManager(StorageManager):
    def __init__(self, database_location: str = default_database_location):
        cur = sqlite3.connect(database_location).cursor()

        table_exists = cur.execute('''
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='transactions';
        ''')

    def get_transactions(self) -> list[TransactionObject]:
        raise NotImplementedError

    def create_transaction(self, t: TransactionObject) -> bool:
        raise NotImplementedError

    def update_transaction(
        self,
        old_transaction: TransactionObject,
        new_transaction: TransactionObject
    ) -> bool:
        raise NotImplementedError

    def get_transaction(self, tid: str) -> TransactionObject:
        raise NotImplementedError

    def load_new_transactions(self, path: str) -> bool:
        raise NotImplementedError
