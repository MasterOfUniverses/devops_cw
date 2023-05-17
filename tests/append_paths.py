import sys
import os


current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path + "/src")
sys.path.append(parent_path + "/tests")
sys.path.append(parent_path)
