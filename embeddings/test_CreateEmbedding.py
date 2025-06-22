import unittest
from CreateEmbedding import CreateEmbedding  # Import the function directly

class TestCreateEmbedding(unittest.TestCase):
    
    def test_create_embedding_with_hello_world(self):
        input_text = "Hello World"
        result = CreateEmbedding(input_text)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], float)

if __name__ == '__main__':
    unittest.main()
