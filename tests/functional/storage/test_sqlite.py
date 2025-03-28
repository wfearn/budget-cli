from pybudget.storage import Transaction, SqliteManager


test_db_name = 'test.db'
test_data = [
    '2000-01-01',
    'Transaction',
    '111.111',
    'bank',
    'category',
    '351d18a0-4772-48ea-88f5-935ac7a9900d',
    '99c0f6f58877b507be8a875cb83b0d12b06531dd31d0bd32e7c320624c06b0b8',
    '1'
]

def execute_sql(sql: str) -> None:
    con = sqlite3.connect(test_db_name)
    cur = con.cursor()
    return cur.execute(sql)


class TestSqliteManager:
    def test_create_executes_with_no_errors(self):
        raise NotImplementedError

    def test_create_adds_data_to_db(self):
        raise NotImplementedError

    def test_update_executes_with_no_errors(self):
        raise NotImplementedError

    def test_update_updates_data_in_db(self):
        raise NotImplementedError

    def test_delete_executes_with_no_errors(self):
        raise NotImplementedError

    def test_delete_deletes_data_in_db(self):
        raise NotImplementedError

    def test_exists_returns_true_if_data_in_db(self):
        raise NotImplementedError

    def test_exists_returns_false_if_data_not_in_db(self):
        raise NotImplementedError
