import os
import tempfile
import unittest

from practices.practice_05.hw5.service_ext import (
    clear_state,
    load_state,
    save_state,
    add_subscriber,
    list_subscribers,
    export_subscribers,
)


class LogicTest(unittest.TestCase):
    def setUp(self):
        # изолируем БД на каждый тест
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["SUBSCRIBERS_DB"] = os.path.join(self.tmp.name, "db.json")
        clear_state()
        load_state()

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_list(self):
        self.assertEqual(add_subscriber(" Ann "), {"subscribed": True})
        save_state()
        self.assertEqual(list_subscribers(), ["Ann"])

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            add_subscriber("   ")

    def test_idempotent(self):
        add_subscriber("Ann")
        add_subscriber("Ann")
        self.assertEqual(list_subscribers(), ["Ann"])

    def test_filtering_case_insensitive(self):
        for n in ["Ann", "alice", "Bob"]:
            add_subscriber(n)
        self.assertEqual(list_subscribers(prefix="A"), ["Ann", "alice"])

    def test_export(self):
        for n in ["Ann", "Bob", "Alice"]:
            add_subscriber(n)
        out = os.path.join(self.tmp.name, "out.txt")
        export_subscribers(prefix="a", path=out)
        with open(out, "r", encoding="utf-8") as f:
            lines = [x.strip() for x in f.readlines()]
        self.assertEqual(lines, ["Ann", "Alice"])

    def test_export_invalid_path(self):
        add_subscriber("Ann")
        with self.assertRaises(ValueError):
            export_subscribers(prefix="", path="")


if __name__ == "__main__":
    unittest.main()
