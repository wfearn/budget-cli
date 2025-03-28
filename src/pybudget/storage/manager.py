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

        print('Args Len:', len(args))
        print('Attrs Length:', len(attribute_names_and_classes))
        if (
            kwargs
            or (
                len(args) != len(attribute_names_and_classes)
                and len(args) != len(attribute_names_and_classes[:5])
            )
        ):
            raise InvalidTransactionError

        for i, arg in enumerate(args):
            property_name, data_class = attribute_names_and_classes[i]
            _property = data_class(arg)
            self._set_property(property_name, _property)

        if not hasattr(self, 'transaction_id'):
            self.transaction_id = self._calculate_transaction_hash(self.amount)

        if not hasattr(self, 'sub_transaction_id'):
            self.sub_transaction_id = \
                self._calculate_transaction_hash(self.sub_amount)

        if not hasattr(self, 'human_verified'):
            self.human_verified = 0

        if not hasattr(self, 'category'):
            self.category = 'NONE'

    def _calculate_transaction_hash(self, amount: float):
        hash_string = f'{self.date}{self.description}{amount}{self.bank}'
        return hashlib.sha256(hash_string.encode()).hexdigest()

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
        elif property_name == 'transaction_id':
            self.transaction_id = _property
        elif property_name == 'sub_transaction_id':
            self.sub_transaction_id = _property
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
            ('transaction_id', str),
            ('sub_transaction_id', str),
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
