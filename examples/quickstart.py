# examples/quickstart.py
"""
Quickstart QFTE (10 lignes).
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import LogisticRegression
from app.calibration import CalibrationManager
from app.metrics import log_loss

# Données
X = np.random.randn(500, 4)
y = (np.random.rand(500) < 0.3).astype(int)

# Modèle
model = LogisticRegression()
model.fit(X, y)

# Calibration
p_raw = model.predict_proba(X)
manager = CalibrationManager(method="platt")
manager.fit(p_raw, y)
p_calib = manager.predict(p_raw)

print("Log Loss calibré :", log_loss(y, p_calib))
