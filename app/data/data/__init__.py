# app/data/__init__.py
"""
Module data pour QFTE.

Fournit :
- Chargement de données (CSV, etc.).
- Préprocessing de base (split, normalisation).
"""

from .loader import load_csv
from .preprocessing import train_test_split, StandardScaler

__all__: list[str] = [
    "load_csv",
    "train_test_split",
    "StandardScaler",
]
