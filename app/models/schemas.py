from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HealthCheck(BaseModel):
    status: str
    service: str


class Match(BaseModel):
    match_id: str
    sport: str  # "football", "tennis", "basketball", "hockey"
    league: str
    home_team: str
    away_team: str
    event_time: datetime
    prediction_time: datetime
    is_live: bool = False
    current_minute: Optional[int] = None
    current_period: Optional[str] = None
    current_score: Optional[str] = None


class TeamFeatures(BaseModel):
    xg: Optional[float] = None
    xga: Optional[float] = None
    xgot: Optional[float] = None
    shots: Optional[float] = None
    shots_on_target: Optional[float] = None
    big_chances: Optional[float] = None
    possession: Optional[float] = None
    conversion: Optional[float] = None
    corners: Optional[float] = None


class QFTEFeatures(BaseModel):
    drs: Optional[float] = None
    rde: Optional[float] = None
    fce: Optional[float] = None
    dfi: Optional[float] = None
    oeq: Optional[float] = None
    oqce: Optional[float] = None
    fpi: Optional[float] = None
    scre: Optional[float] = None
    sti: Optional[float] = None
    esi: Optional[float] = None
    uqs: Optional[float] = None


class LiveFeatures(BaseModel):
    current_score_home: int
    current_score_away: int
    current_minute: int
    current_period: str

    shots_home: int
    shots_away: int
    shots_on_target_home: int
    shots_on_target_away: int

    xg_home: float
    xg_away: float

    possession_home: float
    possession_away: float

    corners_home: int
    corners_away: int

    yellow_cards_home: int
    yellow_cards_away: int

    red_cards_home: int
    red_cards_away: int


class ScoreDistribution(BaseModel):
    sport: str
    match_id: str

    # Distribution FT
    ft_distribution: dict[str, float]
    ft_top_scores: list[tuple[str, float]]

    # Distribution HT
    ht_distribution: dict[str, float]
    ht_top_scores: list[tuple[str, float]]

    # Probas dérivées
    p_home_ft: float
    p_draw_ft: float
    p_away_ft: float

    p_home_ht: float
    p_draw_ht: float
    p_away_ht: float

    p_over_2_5_ft: float
    p_btts_ft: float


class Decision(BaseModel):
    action: str  # "BET", "WATCH", "PASS", "NO_QUALIFIED"
    market: Optional[str] = None

    probability: Optional[float] = None
    fair_odds: Optional[float] = None
    market_odds: Optional[float] = None
    ev: Optional[float] = None

    market_fit: Optional[float] = None
    mechanism_fit: Optional[float] = None

    esi: Optional[float] = None
    uqs: Optional[float] = None
    tail_risk: Optional[str] = None  # "LOW", "MODERATE", "HIGH"

    confidence: Optional[float] = None
    is_live: bool = False
