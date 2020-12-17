#!/usr/bin/env python3
import os
import sys
import unittest
from pathlib import Path

thisDir = Path(__file__).absolute().parent
sys.path.insert(0, str(thisDir.parent))

import SpecprParser

class Tests(unittest.TestCase):
	def testOpen(self):
		a = SpecprParser.SpecprParser(thisDir / "test")


if __name__ == "__main__":
	unittest.main()
