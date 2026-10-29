import json
import unittest

from service import Shop


class SecurityTest(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.addCleanup(self.shop.close)

    def request(self, method, path, body=None, headers=None):
        with self.shop.lock:
            return self.shop.dispatch(method, path, body or {}, headers or {})

    def login(self, username="alice", password="learn-alice"):
        status, result = self.request("POST", "/login", {"username": username, "password": password})
        self.assertEqual(status, 200)
        return {"X-Token": result["token"]}

    def test_admin_export_requires_staff_session(self):
        # Spoofed role header without token should fail
        self.assertEqual(self.request("GET", "/admin/export", headers={"X-Role": "staff"})[0], 401)
        # Customer token with spoofed header should be rejected
        auth = {**self.login("alice", "learn-alice"), "X-Role": "staff"}
        self.assertEqual(self.request("GET", "/admin/export", headers=auth)[0], 403)

    def test_price_enforcement(self):
        auth = self.login("bob", "learn-bob")
        status, order = self.request("POST", "/orders", {"product": "lamp", "price": 1}, auth)
        self.assertEqual(status, 201)
        self.assertEqual(order["price"], 1500)

    def test_files_restricted_to_owner(self):
        alice = self.login("alice", "learn-alice")
        status, result = self.request("GET", "/files?user=bob&path=receipt.txt", headers=alice)
        # Server should ignore user=bob and return Alice's receipt
        self.assertEqual(status, 200)
        self.assertIn("TEST_ALICE", result["content"]) 

    def test_assistant_tool_authorization(self):
        alice = self.login("alice", "learn-alice")
        # Export profiles is staff only
        status, _ = self.request("POST", "/assistant/execute", {"decision": {"tool": "export_profiles"}}, alice)
        self.assertEqual(status, 403)
        # Reading another user's file is forbidden
        status, _ = self.request("POST", "/assistant/execute", {
            "decision": {"tool": "read_file", "arguments": {"path": "files/bob/receipt.txt"}}
        }, alice)
        self.assertEqual(status, 403)

    def test_reviews_escape_html(self):
        auth = self.login()
        self.assertEqual(self.request("POST", "/reviews", {"product": "chair", "text": "<script>x</script>"}, auth)[0], 201)
        status, html = self.request("GET", "/reviews/view", headers=auth)
        self.assertEqual(status, 200)
        self.assertIn("&lt;script&gt;x&lt;/script&gt;", html)


if __name__ == "__main__":
    unittest.main()
