from datetime import datetime
import hashlib
import pytest

from pybudget.storage import InvalidTransactionError, Transaction


test_data = [
    '2000-01-01',
    'Transaction',
    '111.111',
    '111.111',
    'bank',
    'category',
    '1'
]


class TestTransaction:
    def test_constructor_throws_no_errors_on_correct_data(self):
        Transaction(*test_data)

    def test_constructor_throws_invalid_transaction_error_on_incorrect_data(self):
        with pytest.raises(InvalidTransactionError):
            Transaction(*test_data[:-1])

    def test_attributes_correctly_set_post_construction(self):
        t = Transaction(*test_data)

        transaction_id_string = f'{t.date}{t.description}{t.amount}{t.bank}'
        sub_transaction_id_string = \
            f'{t.date}{t.description}{t.sub_amount}{t.bank}'

        transaction_id = hashlib.sha256(transaction_id_string.encode()).hexdigest()
        sub_transaction_id = hashlib \
                             .sha256(sub_transaction_id_string.encode()) \
                             .hexdigest()

        assert t.date == test_data[0]
        assert t.description == test_data[1]
        assert t.amount == float(test_data[2])
        assert t.sub_amount == float(test_data[3])
        assert t.bank == test_data[4]
        assert t.category == test_data[5]
        assert t.human_verified == int(test_data[6])
        assert t.transaction_id == transaction_id
        assert t.sub_transaction_id == sub_transaction_id
