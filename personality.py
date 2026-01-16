"""
personality.py

Purpose:
- Resolve candidate personality from query params (ca=)
- Support DEV/TST mode param (mode=DEV|TST)
- Load candidate context text from files in ./context/
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class CandidatePersonality:
    key: str               # e.g., "saw"
    display_name: str      # e.g., "Kshama Sawant"
    context_file: str      # e.g., "sawant.txt"


# Canonical candidate map
CANDIDATES: Dict[str, CandidatePersonality] = {
    "saw": CandidatePersonality(
        key="saw",
        display_name="Kshama Sawant",
        context_file="sawant.txt",
    ),
    "cha": CandidatePersonality(
        key="cha",
        display_name="Chaudhry",
        context_file="chaudhry.txt",
    ),

    "tur": CandidatePersonality(
        key="tur",
        display_name="Jack Turner (Fictional)",
        context_file="turner.txt",
    ),

}

DEFAULT_CANDIDATE_KEY = "saw"
VALID_MODES = {"dev", "tst"}


def normalize(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def get_mode(args) -> str:
    """Return normalized mode string, or '' for production."""
    mode = normalize(args.get("mode"))
    return mode if mode in VALID_MODES else ""


def should_show_debug(args) -> bool:
    """True only when mode is DEV or TST (case-insensitive)."""
    return get_mode(args) in VALID_MODES


def get_candidate_key(args) -> str:
    """Return normalized candidate key from args, falling back to default."""
    ca = normalize(args.get("ca"))
    return ca if ca in CANDIDATES else DEFAULT_CANDIDATE_KEY


def get_candidate(args) -> CandidatePersonality:
    key = get_candidate_key(args)
    return CANDIDATES[key]


def load_candidate_context(candidate: CandidatePersonality) -> str:
    """
    Load the candidate context text from ./context/<file>.
    If missing, return a small fallback string (do not crash the app).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "context", candidate.context_file)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return (
            f"It is January 2026. You are responding on behalf of {candidate.display_name}. "
            "Provide a thoughtful, respectful response."
        )
