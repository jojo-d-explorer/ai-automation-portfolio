#!/usr/bin/env python3
"""
Loader for joey_profile.yaml — fails loudly on missing/malformed required
keys instead of letting downstream pipeline code hit a silent KeyError deep
in a run. Phase 0 acceptance criterion (HANDOFF_ROADMAP_v4 §3): "profile.yaml
validates (write a tiny loader that fails loudly on missing keys)".

Usage:
    python3 config/load_profile.py            # validate, print a summary
    from config.load_profile import load_profile  # import elsewhere
"""

import sys
import os
import yaml

PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "joey_profile.yaml")

REQUIRED_TOP_LEVEL_KEYS = [
    "role_families",
    "seniority_gate",
    "location_tiers",
    "sectors",
    "scoring_rubric",
    "spanish_requirement_rule",
    "comp_floor",
    "reserved_decisions",
]

REQUIRED_RUBRIC_KEYS = ["weights", "two_stretch_cap", "score_cutoff", "flag_band", "red_flag_archetypes"]
REQUIRED_WEIGHT_KEYS = ["skills_experience", "geography", "seniority", "sector"]


class ProfileValidationError(Exception):
    pass


def load_profile(path: str = PROFILE_PATH) -> dict:
    if not os.path.exists(path):
        raise ProfileValidationError(f"profile not found at {path}")

    with open(path) as f:
        profile = yaml.safe_load(f)

    if not isinstance(profile, dict):
        raise ProfileValidationError("profile did not parse to a dict — check YAML syntax")

    missing = [k for k in REQUIRED_TOP_LEVEL_KEYS if k not in profile]
    if missing:
        raise ProfileValidationError(f"missing required top-level key(s): {missing}")

    if not profile["role_families"]:
        raise ProfileValidationError("role_families is empty")

    rubric = profile["scoring_rubric"]
    missing_rubric = [k for k in REQUIRED_RUBRIC_KEYS if k not in rubric]
    if missing_rubric:
        raise ProfileValidationError(f"scoring_rubric missing key(s): {missing_rubric}")

    missing_weights = [k for k in REQUIRED_WEIGHT_KEYS if k not in rubric["weights"]]
    if missing_weights:
        raise ProfileValidationError(f"scoring_rubric.weights missing key(s): {missing_weights}")

    total = sum(rubric["weights"].values())
    if total != 100:
        raise ProfileValidationError(f"scoring_rubric.weights must sum to 100, got {total}")

    comp_floor = profile["comp_floor"]
    if not isinstance(comp_floor, dict) or "status" not in comp_floor:
        raise ProfileValidationError("comp_floor must be a dict with a 'status' key")

    return profile


def main():
    try:
        profile = load_profile()
    except ProfileValidationError as e:
        print(f"PROFILE INVALID: {e}", file=sys.stderr)
        sys.exit(1)

    n_families = len(profile["role_families"])
    n_keywords = sum(len(v) for v in profile["role_families"].values())
    weights = profile["scoring_rubric"]["weights"]
    comp_status = profile["comp_floor"]["status"]

    print("profile.yaml validated OK")
    print(f"  role families: {n_families} ({n_keywords} keywords total)")
    print(f"  rubric weights: {weights} (sums to {sum(weights.values())})")
    print(f"  score cutoff: {profile['scoring_rubric']['score_cutoff']}, flag band: {profile['scoring_rubric']['flag_band']}")
    print(f"  comp_floor status: {comp_status}")
    if comp_status == "UNRESOLVED":
        print("  ^ reserved decision, not yet set by Joey — do not default it")


if __name__ == "__main__":
    main()
