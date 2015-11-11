from ouija.tests.util import TestCase

class TablesApiTestCase(TestCase):
    def setUp(self):
        super(TablesApiTestCase, self).setUp()

    def test_table_list(self):
        res = self.client.get('/api/tables')
        assert res.status_code == 200, res

    def test_table_get(self):
        pass
        # res = self.client.get('/api/table/zz_testtable')
        # assert res.status_code == 200, res

    def test_table_rows(self):
        pass
        #res = self.client.get('/api/table/zz_testtable/rows')
        #assert res.status_code == 200, res
