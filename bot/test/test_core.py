import unittest
from assistant.core import Common


class TestCore(unittest.TestCase):

    def setUp(self):
        self.core = Common()

    def test_add_command(self):
        with self.assertRaises(TypeError):
            self.core.add_command({
                "name": "some_name",
                "callback": "some_callback"
            })

    def tearDown(self):
        del self.core

if __name__ == "__main__":
    unittest.main()
