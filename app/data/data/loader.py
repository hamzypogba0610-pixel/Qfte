# app/data/loader.py
"""
Chargement de données pour QFTE.
"""

from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List


def load_csv(
    filepath: str,
    target_column: str,
    feature_columns: Optional[List[str]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Charge un CSV et sépare features / target.

    Args:
        filepath: Chemin du fichier CSV.
        target_column: Nom de la colonne cible.
        feature_columns: Colonnes à utiliser comme features.
                         Si None, utilise toutes les colonnes sauf target.

    Returns:
        X: Features (n_samples, n_features).
        y: Target (n_samples,).
    """
    import csv

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        if target_column not in headers:
            raise ValueError(f"Column '{target_column}' not found in CSV.")

        if feature_columns is None:
            feature_columns = [c for c in headers if c != target_column]

        X_list = []
        y_list = []

        for row in reader:
            x_row = [float(row[c]) for c in feature_columns]
            y_val = float(row[target_column])

            X_list.append(x_row)
            y_list.append(y_val)

    X = np.array(X_list, dtype=float)
    y = np.array(y_list, dtype=float)

    return X, y
