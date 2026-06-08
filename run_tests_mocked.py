import sys
import unittest
from unittest.mock import MagicMock

# Mock litellm since it's not installed
sys.modules['litellm'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['Bio'] = MagicMock()
sys.modules['Bio.Blast'] = MagicMock()

import os
os.environ["HUGGING_FACE_API_KEY"] = "test"

# Run tests
loader = unittest.TestLoader()
tests = loader.discover('Proyecto_Agente/test')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
