from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_profile import ProfileError, load_and_validate, validate


class ProfileValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tomllib

        with (ROOT / "profile/athlete.example.toml").open("rb") as handle:
            cls.example = tomllib.load(handle)

    def test_example_profile_is_valid(self):
        warnings = load_and_validate(ROOT / "profile/athlete.example.toml")
        self.assertIsInstance(warnings, list)

    def test_strict_mode_rejects_placeholders(self):
        with self.assertRaisesRegex(ProfileError, "campos de ejemplo"):
            validate(self.example, strict=True)

    def test_overlapping_zones_are_rejected(self):
        profile = copy.deepcopy(self.example)
        profile["heart_rate_zones"]["z2"] = [110, 145]
        with self.assertRaisesRegex(ProfileError, "solapa"):
            validate(profile)

    def test_long_session_must_be_available(self):
        profile = copy.deepcopy(self.example)
        profile["schedule"]["long_session_day"] = "friday"
        with self.assertRaisesRegex(ProfileError, "long_session_day"):
            validate(profile)

    def test_red_flag_produces_warning(self):
        profile = copy.deepcopy(self.example)
        profile["health"]["red_flags_today"] = True
        warnings = validate(profile)
        self.assertTrue(any("no generar entrenamiento" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
