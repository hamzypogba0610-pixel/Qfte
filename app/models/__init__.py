# app/models/__init__.py
"""
Modèles pour QFTE.

Inclut :
- Classes de base.
- Régression logistique.
- Modèles de scores (Poisson, Dixon-Coles, etc.).
- Métriques et schémas associés.
- Backtest.
"""

from .base import BaseModel
from .logistic import LogisticRegression

# Imports existants (à adapter si besoin)
# from .metrics import ...
# from .poisson import ...
# from .dixon_coles import ...
# from .backtest import ...

__all__: list[str] = [
    "BaseModel",
    "LogisticRegression",
    # Ajoute ici les autres modèles au fur et à mesure
]
