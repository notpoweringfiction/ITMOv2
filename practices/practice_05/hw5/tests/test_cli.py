import os
import subprocess
import sys
import tempfile
import unittest


CLI = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cli.py"))


def run_cli(args, env):
    proc = subprocess.run([
        sys.executable,
        CLI,
        *args,
    ], capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout, proc.stderr


class CLITest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = os.environ.copy()
        self.env["SUBSCRIBERS_DB"] = os.path.join(self.tmp.name, "db.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_subscribe_ok(self):
        code, out, err = run_cli(["subscribe", "Ann"], self.env)
        self.assertEqual(code, 0, err)
        self.assertIn("subscribed: true", out)

    def test_subscribe_empty(self):
        code, out, err = run_cli(["subscribe", "   "], self.env)
        self.assertNotEqual(code, 0)
        self.assertIn("empty name", err)

    def test_list_and_filter(self):
        for name in ["Ann", "alice", "Bob"]:
            code, _, _ = run_cli(["subscribe", name], self.env)
            self.assertEqual(code, 0)
        code, out, err = run_cli(["list", "--prefix", "a"], self.env)
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip().splitlines(), ["Ann", "alice"])

    def test_export(self):
        for name in ["Ann", "Bob", "Alice"]:
            code, _, _ = run_cli(["subscribe", name], self.env)
            self.assertEqual(code, 0)
        out_path = os.path.join(self.tmp.name, "out.txt")
        code, out, err = run_cli(["export", "--prefix", "a", "--out", out_path], self.env)
        self.assertEqual(code, 0, err)
        self.assertIn("exported: ", out)
        with open(out_path, "r", encoding="utf-8") as f:
            lines = [x.strip() for x in f.readlines()]
        self.assertEqual(lines, ["Ann", "Alice"])


if __name__ == "__main__":
    unittest.main()
