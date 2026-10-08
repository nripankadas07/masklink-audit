import json
import unittest
from masklink_audit import audit

class ContractTests(unittest.TestCase):
    def pair(self,source="id,label\na,one\nb,two\n",masked="id,label\nx,one\ny,two\n"):
        return {"source":source,"masked":masked,"domains":{"id":"person"}}
    def codes(self,r):return {x["code"]for x in r["findings"]}
    def test_good(self):self.assertTrue(audit([self.pair()])["ok"])
    def test_collision(self):
        self.assertIn("token_collision",self.codes(audit([self.pair(masked="id,label\nx,one\nx,two\n")])))
    def test_cross_file_inconsistent(self):
        self.assertIn("inconsistent_token",self.codes(audit([self.pair(),self.pair(masked="id,label\nz,one\ny,two\n")])))
    def test_join_different_column(self):
        r=audit([self.pair(),{"source":"ref,label\na,visit\n","masked":"ref,label\nx,visit\n","domains":{"ref":"person"}}])
        self.assertTrue(r["ok"]);self.assertEqual(r["distinct_domain_identifiers"],2)
    def test_unchanged(self):
        self.assertIn("identifier_unchanged",self.codes(audit([self.pair(masked="id,label\na,one\ny,two\n")])))
    def test_non_id_changed(self):
        self.assertIn("unmapped_column_changed",self.codes(audit([self.pair(masked="id,label\nx,two\ny,one\n")])))
    def test_no_values_in_report(self):
        r=audit([self.pair(source="id,label\nprivate@example.invalid,one\n",masked="id,label\nprivate@example.invalid,one\n")])
        self.assertNotIn("private@example.invalid",json.dumps(r));self.assertFalse(r["ok"])
    def test_row_count(self):
        with self.assertRaises(ValueError):audit([self.pair(masked="id,label\nx,one\n")])
    def test_duplicate_headers(self):
        with self.assertRaises(ValueError):audit([self.pair(source="id,id\na,b\n")])
    def test_blank_preserved(self):
        self.assertTrue(audit([self.pair(source="id,label\n,one\n",masked="id,label\n,one\n")])["ok"])
    def test_ragged(self):
        with self.assertRaises(ValueError):audit([self.pair(source="id,label\na\n")])

if __name__=="__main__":unittest.main()
