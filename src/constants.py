"""
Constants used system-wide.
"""
import os

from pathlib import Path


# SYSTEM DEFINITIONS

PROJECT_PATH = Path(os.path.dirname(os.path.abspath(__file__ + "/..")))

# ML MODEL'S RELATED CONSTANTS
DEFAULT_SCORING_MODEL = "similarity_scorer"
DEFAULT_SCORING_VERSION = (0,0,1)
DEFAULT_MODEL_ROUND_ROBIN_RATIO = 10

DEFAULT_CANDIDATE_INTERESTS_LENGTH = 3
DEFAULT_CANDIDATE_INTERESTS_INFO_FIELDS = ["category", "position", "experience"]
