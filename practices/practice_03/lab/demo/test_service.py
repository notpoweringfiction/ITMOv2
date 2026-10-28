<<<<<<< Updated upstream
import unittest
from service import subscribe, subscribers


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann"), {"subscribed": True})
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaises(ValueError):
            subscribe(" ")

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)


if __name__ == "__main__":
    unittest.main()

=======
import unittest
from service import subscribe, unsubscribe, list_subscribers, subscribers


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann"), {"subscribed": True})
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaises(ValueError):
            subscribe(" ")

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)

    def test_unsubscribe_present(self):
        subscribe("Ann")
        self.assertEqual(unsubscribe("Ann"), {"unsubscribed": True})
        self.assertEqual(len(subscribers), 0)

    def test_unsubscribe_absent(self):
        self.assertEqual(unsubscribe("Bob"), {"unsubscribed": False})
        self.assertEqual(len(subscribers), 0)

    def test_unsubscribe_empty(self):
        with self.assertRaises(ValueError):
            unsubscribe("   ")

    def test_list_subscribers_sorted(self):
        subscribe("Zed")
        subscribe("Ann")
        subscribe("Mike")
        self.assertEqual(list_subscribers(), ["Ann", "Mike", "Zed"])

    def test_list_subscribers_unsorted(self):
        subscribe("Mike")
        result = list_subscribers(sorted_=False)
        self.assertCountEqual(result, ["Mike"])  # order not guaranteed


if __name__ == "__main__":
    unittest.main()
>>>>>>> Stashed changes
