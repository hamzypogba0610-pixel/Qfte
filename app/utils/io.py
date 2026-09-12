# app/utils/io.py
"""
Fonctions d'I/O pour QFTE.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any


def save_object(obj: Any, filepath: str) -> None:
    """
    Sauvegarde un objet avec pickle.

    Args:
        obj: Objet à sauvegarder.
        filepath: Chemin du fichier.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_object(filepath: str) -> Any:
    """
    Charge un objet sauvegardé avec pickle.

    Args:
        filepath: Chemin du fichier.

    Returns:
        Objet chargé.
    """
    with open(filepath, "rb") as f:
        return pickle.load(f)
