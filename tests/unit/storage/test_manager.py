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
    hashlib.sha256(b'test_1').hexdigest(),
    hashlib.sha256(b'test_2').hexdigest(),
    'category',
    '1'
]


class TestTransaction:
    def test_constructor_throws_no_errors_on_correct_data(self):
        Transaction(*test_data)

    def test_constructor_throws_invalid_transaction_error_on_incorrect_data(self):
        with pytest.raises(InvalidTransactionError):
            Transaction(*test_data[:-1])

    def test_base_attributes_correctly_set_post_construction(self):
        t = Transaction(*test_data[:5])

        assert t.date == test_data[0]
        assert t.description == test_data[1]
        assert t.amount == float(test_data[2])
        assert t.sub_amount == float(test_data[3])
        assert t.bank == test_data[4]

    def test_human_verified_has_correct_default_if_not_passed_in(self):
        t = Transaction(*test_data[:5])

        expected_human_verified = 0

        assert t.human_verified == expected_human_verified

    def test_transaction_id_has_correct_value_if_not_passed_in(self):
        t = Transaction(*test_data[:5])

        transaction_id_string = f'{t.date}{t.description}{t.amount}{t.bank}'

        expected_transaction_id = hashlib \
                                  .sha256(transaction_id_string.encode()) \
                                  .hexdigest()


        assert t.transaction_id == expected_transaction_id

    def test_sub_transaction_id_has_correct_value_if_not_passed_in(self):
        t = Transaction(*test_data[:5])

        sub_transaction_id_string = \
            f'{t.date}{t.description}{t.sub_amount}{t.bank}'

        expected_sub_transaction_id = hashlib.sha256(
            sub_transaction_id_string.encode()
        ).hexdigest()

        assert t.sub_transaction_id == expected_sub_transaction_id

    def test_category_has_correct_value_if_not_passed_in(self):
        t = Transaction(*test_data[:5])

        expected_category = 'NONE'

        assert t.category == expected_category

    def test_additional_attributes_correctly_set_if_passed_in(self):
        t = Transaction(*test_data)

        expected_transaction_id = hashlib.sha256(b'test_1').hexdigest()
        expected_sub_transaction_id = hashlib.sha256(b'test_2').hexdigest()

        expected_category = 'category'
        expected_human_verified = 1

        assert t.transaction_id == expected_transaction_id
        assert t.sub_transaction_id == expected_sub_transaction_id
        assert t.category == expected_category
        assert t.human_verified == expected_human_verified
