from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, unique=True, index=True, nullable=False)
    sport = Column(String, nullable=False)
    league = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    event_time = Column(DateTime, nullable=False)
    prediction_time = Column(DateTime, nullable=False)
    is_live = Column(Boolean, default=False)
    current_minute = Column(Integer, nullable=True)
    current_period = Column(String, nullable=True)
    current_score = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TeamFeature(Base):
    __tablename__ = "team_features"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), nullable=False)
    team_name = Column(String, nullable=False)
    xg = Column(Float, nullable=True)
    xga = Column(Float, nullable=True)
    xgot = Column(Float, nullable=True)
    shots = Column(Float, nullable=True)
    shots_on_target = Column(Float, nullable=True)
    big_chances = Column(Float, nullable=True)
    possession = Column(Float, nullable=True)
    conversion = Column(Float, nullable=True)
    corners = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Odd(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), nullable=False)
    market = Column(String, nullable=False)  # "1X2", "Over/Under 2.5", etc.
    selection = Column(String, nullable=False)  # "1", "N", "2", "Over", "Under"
    odds_value = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), unique=True, nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    ht_home_score = Column(Integer, nullable=True)
    ht_away_score = Column(Integer, nullable=True)
    status = Column(String, nullable=False)  # "FT", "HT", "POSTPONED", etc.
    created_at = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), nullable=False)
    market = Column(String, nullable=False)
    selection = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    fair_odds = Column(Float, nullable=False)
    market_odds = Column(Float, nullable=False)
    ev = Column(Float, nullable=False)
    decision = Column(String, nullable=False)  # "BET", "WATCH", "PASS"
    confidence = Column(Float, nullable=True)
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
