# app/calibration/recalibration/drift_detection.py
"""
Détection de dérive (drift) pour la calibration.

Utilise des tests statistiques pour détecter quand la distribution
des probabilités ou des labels change significativement.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple, Optional
from scipy import stats


class DriftDetector:
    """
    Détecteur de dérive pour la calibration.
    """

    def __init__(
        self,
        method: str = "ks",
        significance_level: float = 0.05,
    ):
        """
        Args:
            method: "ks" (Kolmogorov-Smirnov) ou "psi" (Population Stability Index).
            significance_level: Seuil de significativité (alpha).
        """
        self.method = method
        self.significance_level = significance_level
        self.reference_probs: Optional[np.ndarray] = None
        self.reference_labels: Optional[np.ndarray] = None

    def set_reference(
        self,
        probs: np.ndarray,
        labels: np.ndarray,
    ) -> None:
        """
        Définit la distribution de référence.

        Args:
            probs: Probabilités de référence.
            labels: Labels de référence (0 ou 1).
        """
        self.reference_probs = np.array(probs).copy()
        self.reference_labels = np.array(labels).copy()

    def detect(
        self,
        current_probs: np.ndarray,
        current_labels: np.ndarray,
    ) -> Tuple[bool, float]:
        """
        Détecte une dérive.

        Args:
            current_probs: Probabilités actuelles.
            current_labels: Labels actuels.

        Returns:
            (drift_detected, p_value_or_psi)
        """
        if self.reference_probs is None:
            raise ValueError("Reference distribution not set.")

        if self.method == "ks":
            return self._ks_test(current_probs)
        elif self.method == "psi":
            return self._psi_test(current_probs)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _ks_test(
        self,
        current_probs: np.ndarray,
    ) -> Tuple[bool, float]:
        """
        Test de Kolmogorov-Smirnov.
        """
        statistic, p_value = stats.ks_2samp(
            self.reference_probs, current_probs
        )
        drift = p_value < self.significance_level
        return drift, float(p_value)

    def _psi_test(
        self,
        current_probs: np.ndarray,
    ) -> Tuple[bool, float]:
        """
        Population Stability Index (PSI).
        """
        # Discrétisation en 10 bins
        bins = np.linspace(0, 1, 11)

        ref_hist, _ = np.histogram(self.reference_probs, bins=bins)
        curr_hist, _ = np.histogram(current_probs, bins=bins)

        # Éviter division par zéro
        ref_hist = ref_hist + 1e-10
        curr_hist = curr_hist + 1e-10

        ref_pct = ref_hist / np.sum(ref_hist)
        curr_pct = curr_hist / np.sum(curr_hist)

        psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))

        # Seuil classique : PSI > 0.25 = dérive forte
        drift = psi > 0.25
        return drift, float(psi)
