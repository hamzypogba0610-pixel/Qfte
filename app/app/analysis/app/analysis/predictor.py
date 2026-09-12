# app/analysis/predictor.py
"""
Fonctions principales d'analyse de matchs (pré-live et live).
"""

from typing import Any, Dict, Optional
from .types import MatchAnalysis, MarketPrediction
from . import config


def _build_winner_prediction(sport: str, match_data: Dict[str, Any]) -> MarketPrediction:
    """
    Construit une prédiction 1N2 / vainqueur (placeholder).
    À remplacer par le vrai modèle QFTE par sport.
    """
    # Exemple simplifié : on simule des probas
    if sport == "football":
        details = {"1": 0.55, "N": 0.25, "2": 0.20}
        recommendation = "1"
        proba = details[recommendation]
        confidence = 7.8
    elif sport == "basketball":
        details = {"1": 0.60, "2": 0.40}
        recommendation = "1"
        proba = details[recommendation]
        confidence = 8.0
    elif sport == "tennis":
        details = {"1": 0.52, "2": 0.48}
        recommendation = "1"
        proba = details[recommendation]
        confidence = 6.5
    else:
        details = {"1": 0.5, "2": 0.5}
        recommendation = "1"
        proba = 0.5
        confidence = 5.0

    return MarketPrediction(
        market_type="1N2",
        recommendation=recommendation,
        confidence=confidence,
        proba=proba,
        details=details,
    )


def _build_ou_prediction(
    line: float, sport: str, match_data: Dict[str, Any]
) -> MarketPrediction:
    """
    Construit une prédiction Over/Under pour une ligne donnée (placeholder).
    """
    # Simulation simple
    if line == 1.5:
        details = {"Over": 0.70, "Under": 0.30}
        recommendation = "Over"
        confidence = 7.2
    elif line == 2.5:
        details = {"Over": 0.58, "Under": 0.42}
        recommendation = "Over"
        confidence = 6.8
    elif line == 3.5:
        details = {"Over": 0.45, "Under": 0.55}
        recommendation = "Under"
        confidence = 6.0
    else:
        details = {"Over": 0.5, "Under": 0.5}
        recommendation = "Over"
        confidence = 5.0

    proba = details[recommendation]

    return MarketPrediction(
        market_type=f"OU_{int(line)}",
        recommendation=recommendation,
        confidence=confidence,
        proba=proba,
        details=details,
    )


def _build_handicap_prediction(sport: str, match_data: Dict[str, Any]) -> MarketPrediction:
    """
    Construit une prédiction handicap (placeholder).
    """
    # Exemple très simplifié
    details = {"home_-0.5": 0.57, "away_+0.5": 0.43}
    recommendation = "home_-0.5"
    proba = details[recommendation]
    confidence = 7.0

    return MarketPrediction(
        market_type="handicap",
        recommendation=recommendation,
        confidence=confidence,
        proba=proba,
        details=details,
    )


def _build_btts_prediction(match_data: Dict[str, Any]) -> Optional[MarketPrediction]:
    """
    Construit une prédiction BTTS (football uniquement).
    """
    # Pour l'instant, on ne gère que le foot
    if match_data.get("sport") != "football":
        return None

    details = {"BTTS_Oui": 0.54, "BTTS_Non": 0.46}
    recommendation = "BTTS_Oui"
    proba = details[recommendation]
    confidence = 6.7

    return MarketPrediction(
        market_type="btts",
        recommendation=recommendation,
        confidence=confidence,
        proba=proba,
        details=details,
    )


def _build_score_predictions(sport: str, match_data: Dict[str, Any]):
    """
    Construit les prédictions score_ht et score_ft (placeholder).
    """
    if sport != "football":
        return None, None

    # HT
    score_ht = MarketPrediction(
        market_type="score_ht",
        recommendation="1-0",
        confidence=6.0,
        proba=0.14,
        details={"1-0": 0.14, "0-0": 0.12, "1-1": 0.10},
    )

    # FT
    score_ft = MarketPrediction(
        market_type="score_ft",
        recommendation="2-1",
        confidence=6.5,
        proba=0.11,
        details={"2-1": 0.11, "2-0": 0.09, "1-1": 0.08},
    )

    return score_ht, score_ft


def analyze_match_pre_live(match_data: Dict[str, Any], sport: str) -> MatchAnalysis:
    """
    Analyse complète d'un match en pré-live.

    match_data doit contenir au moins :
      - competition: str
      - home: str
      - away: str
      - start_time: str
      - sport: str (redondant avec l'argument, mais utile en interne)
    """
    match_data["sport"] = sport

    # Prédictions par marché
    winner = _build_winner_prediction(sport, match_data)
    ou_1_5 = _build_ou_prediction(1.5, sport, match_data)
    ou_2_5 = _build_ou_prediction(2.5, sport, match_data)
    ou_3_5 = _build_ou_prediction(3.5, sport, match_data)
    handicap = _build_handicap_prediction(sport, match_data)
    btts = _build_btts_prediction(match_data)
    score_ht, score_ft = _build_score_predictions(sport, match_data)

    # Calcul de métriques globales (version simplifiée)
    confidences = [
        c.confidence
        for c in [winner, ou_1_5, ou_2_5, ou_3_5, handicap, btts, score_ft]
        if c is not None
    ]
    global_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    # Edge simulé (à remplacer par un vrai calcul basé sur les cotes)
    edge = 0.06  # 6%

    # Nombre de marchés "forts" (confiance ≥ seuil)
    strong_markets_count = sum(
        1 for c in confidences if c >= config.CONFIDENCE_THRESHOLD_STRONG
    )

    return MatchAnalysis(
        sport=sport,
        competition=match_data["competition"],
        home=match_data["home"],
        away=match_data["away"],
        start_time=match_data["start_time"],
        is_live=False,
        winner=winner,
        ou_1_5=ou_1_5,
        ou_2_5=ou_2_5,
        ou_3_5=ou_3_5,
        handicap=handicap,
        btts=btts,
        score_ht=score_ht,
        score_ft=score_ft,
        global_confidence=global_confidence,
        edge=edge,
        strong_markets_count=strong_markets_count,
    )


def analyze_match_live(
    match_data: Dict[str, Any], live_state: Dict[str, Any], sport: str
) -> MatchAnalysis:
    """
    Analyse complète d'un match en live.

    live_state contient :
      - score_current: str (ex: "1-0")
      - minute: str (ex: "32'", "Q2", "Set 2")
      - éventuellement d'autres stats live.
    """
    # Pour l'instant, on fait une version simplifiée :
    # on appelle analyze_match_pre_live puis on adapte quelques champs.

    analysis = analyze_match_pre_live(match_data, sport)
    analysis.is_live = True
    analysis.score_current = live_state.get("score_current")
    analysis.minute = live_state.get("minute")

    # Ici, plus tard :
    # - recalculer les probas en fonction du score et du temps,
    # - ajuster confiances et edge.

    # Pour l'exemple, on augmente un peu la confiance globale en live
    analysis.global_confidence = min(10.0, analysis.global_confidence + 0.5)

    return analysis
