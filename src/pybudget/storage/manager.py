from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


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
