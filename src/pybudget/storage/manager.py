from abc import ABC, abstractmethod
from datetime import datetime
import hashlib
from typing import Any
import uuid

import pandas as pd


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


class Transaction(TransactionObject):
    def __init__(self, *args, **kwargs) -> None:
        attribute_names_and_classes = Transaction._get_input_data_format()

        if kwargs or len(args) != len(attribute_names_and_classes):
            raise InvalidTransactionError

        for i, arg in enumerate(args):
            property_name, data_class = attribute_names_and_classes[i]
            _property = data_class(arg)
            self._set_property(property_name, _property)

        self._set_transaction_id(self.amount)
        self._set_transaction_id(self.sub_amount)

    def _set_transaction_id(self, amount: float):
        hash_string = f'{self.date}{self.description}{amount}{self.bank}'

        if amount == self.amount and not hasattr(self, 'transaction_id'):
            self.transaction_id = hashlib.sha256(hash_string.encode()).hexdigest()

        elif amount == self.sub_amount:
            self.sub_transaction_id = hashlib.sha256(hash_string.encode()).hexdigest()

        else:
            raise InvalidTransactionError

    def _set_property(
        self,
        property_name: str,
        _property: Any
    ):
        if property_name == 'date':
            self.date = _property
        elif property_name == 'description':
            self.description = _property
        elif property_name == 'amount':
            self.amount = _property
        elif property_name == 'sub_amount':
            self.sub_amount = _property
        elif property_name == 'bank':
            self.bank = _property
        elif property_name == 'category':
            self.category = _property
        elif property_name == 'human_verified':
            self.human_verified = _property
        else:
            raise InvalidTransactionError

    @classmethod
    def _get_input_data_format(self) -> list[Any]:
        return [
            ('date', str),
            ('description', str),
            ('amount', float),
            ('sub_amount', float),
            ('bank', str),
            ('category', str),
            ('human_verified', int)
        ]


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
