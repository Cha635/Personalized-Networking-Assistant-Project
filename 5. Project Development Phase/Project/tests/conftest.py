import sys
from pathlib import Path

# Ensure project root is first on sys.path for all test modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
