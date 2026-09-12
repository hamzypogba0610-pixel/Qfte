# Architecture du projet QFTE

Ce document décrit l'architecture globale du projet QFTE, en expliquant le rôle de chaque module et la façon dont ils interagissent, du moteur de prédiction jusqu'au bot Telegram.

## Vue d'ensemble

QFTE est organisé en trois couches principales :

1. **Couche scientifique (cœur QFTE)**  
   - `app/calibration/` : méthodes de calibration des probabilités.
   - `app/models/` : modèles de prédiction (classification, scores, etc.).
   - `app/metrics/` : métriques d'évaluation (Log Loss, Brier, ECE, etc.).
   - `app/backtest/` : moteur de backtest et métriques de performance (PnL, Sharpe, drawdown).
   - `app/data/`, `app/utils/`, `app/experiments/` : données, utilitaires, configurations d'expériences.

2. **Couche analyse de matchs (application du cœur QFTE)**  
   - `app/analysis/` : module qui utilise le cœur QFTE pour analyser des matchs concrets (football, basketball, tennis).
     - `types.py` : structures de données (`MatchAnalysis`, `MarketPrediction`).
     - `config.py` : seuils, modes (production/experimental), règles de décision.
     - `predictor.py` : fonctions `analyze_match_pre_live` et `analyze_match_live`.
     - `selector.py` : sélection des 2 matchs les plus fiables du jour.

3. **Couche interface utilisateur (bot Telegram)**  
   - `bot/` : bot Telegram privé qui interroge le module d'analyse et renvoie les résultats.
     - `config.py` : token Telegram, user ID, seuils de notification.
     - `messages.py` : formatage des messages en français.
     - `telegram_bot.py` : gestion des commandes (`/start`, `/help`, `/today`, `/analyse`, `/top2`, etc.) et logique de notification automatique.

## Flux typique d'une analyse

1. **Données d'entrée**  
   - Un match (équipes, compétition, date, cotes, stats, etc.).
   - En live : score actuel, minute, éventuellement stats live.

2. **Module d'analyse (`app/analysis/predictor.py`)**  
   - Appelle les modèles appropriés (par sport) depuis `app/models/`.
   - Calcule des probabilités brutes pour chaque marché (1N2, Over/Under, handicap, BTTS, scores, etc.).
   - Applique la calibration via `app/calibration/` pour obtenir des probabilités fiables.
   - Calcule les métriques de confiance et d'edge.
   - Renvoie un objet `MatchAnalysis` (défini dans `app/analysis/types.py`).

3. **Sélection des meilleures opportunités (`app/analysis/selector.py`)**  
   - Prend une liste de `MatchAnalysis` (ex. : tous les matchs du jour).
   - Filtre et classe selon :
     - `global_confidence`,
     - `edge`,
     - `strong_markets_count` (nombre de marchés avec confiance ≥ 7,5).
   - Renvoie les 2 meilleurs matchs.

4. **Bot Telegram (`bot/telegram_bot.py`)**  
   - Reçoit une commande utilisateur (ex. : `/analyse PSG OM`).
   - Appelle `predictor.analyze_match_pre_live` ou `analyze_match_live`.
   - Utilise `messages.format_match_analysis` pour formater la réponse.
   - Envoie le message à l'utilisateur via l'API Telegram.
   - Pour les opportunités très fortes, envoie automatiquement une alerte (selon les seuils dans `bot/config.py`).

## Rôle des fichiers principaux

### Cœur scientifique

- `app/calibration/`  
  - Implémente les méthodes de calibration (Platt, Isotonic, Beta, Temperature Scaling, etc.).
  - Utilisé par le module d'analyse pour ajuster les probabilités brutes.

- `app/models/`  
  - Contient les modèles de prédiction (logistic regression, naive bayes, arbre, modèles de scores, etc.).
  - Sera étendu avec des modules par sport (`football/`, `basketball/`, `tennis/`).

- `app/metrics/`  
  - Fonctions pour calculer Log Loss, Brier score, ECE, etc.
  - Utilisées pour évaluer et comparer les modèles.

- `app/backtest/`  
  - Moteur de backtest pour tester les stratégies de paris sur l'historique.
  - Calcule PnL, Sharpe, drawdown, etc.

### Module d'analyse

- `app/analysis/types.py`  
  - Définit les structures de données :
    - `MarketPrediction` : prédiction pour un marché (1N2, OU, handicap, etc.).
    - `MatchAnalysis` : analyse complète d'un match.

- `app/analysis/config.py`  
  - Centralise :
    - le mode (production/experimental),
    - les seuils de confiance et d'edge,
    - les règles de sélection des matchs.

- `app/analysis/predictor.py`  
  - Fonctions principales :
    - `analyze_match_pre_live(match_data, sport)` : analyse en pré-live.
    - `analyze_match_live(match_data, live_state, sport)` : analyse en live.
  - Pour l'instant, utilise des placeholders ; sera connecté progressivement aux vrais modèles QFTE.

- `app/analysis/selector.py`  
  - Fonction `select_top2_matches(analyses)` :
    - sélectionne les 2 matchs les plus fiables selon les critères QFTE.

### Bot Telegram

- `bot/config.py`  
  - Contient :
    - `TELEGRAM_BOT_TOKEN` : token obtenu via @BotFather.
    - `TELEGRAM_USER_ID` : ton user ID Telegram.
    - Seuils pour les notifications automatiques.

- `bot/messages.py`  
  - Fonctions de formatage :
    - `format_match_analysis(analysis)` : message détaillé pour `/analyse`.
    - `format_top2_matches(analyses)` : message pour `/top2`.
    - `format_match_list(matches, title)` : message pour `/today`, `/next`, `/live`.
    - `format_auto_alert(analysis)` : alerte automatique pour opportunité forte.

- `bot/telegram_bot.py`  
  - Point d'entrée du bot.
  - Gère les commandes :
    - `/start`, `/help` : informations.
    - `/today`, `/next`, `/live` : listes de matchs.
    - `/analyse Équipe1 Équipe2` : analyse complète.
    - `/top2` : les 2 matchs fiables du jour.
  - Appelle le module d'analyse et formate les réponses.

### Scripts et configuration

- `scripts/run_full_pipeline.py`  
  - Lance le pipeline complet (calibration + backtest) sur `data/sample_matches.csv`.

- `scripts/run_bot.py`  
  - Point d'entrée pour lancer le bot Telegram.

- `requirements.txt`  
  - Liste les dépendances Python nécessaires :
    - numpy, scipy, pandas,
    - python-telegram-bot,
    - APScheduler.

## Évolution prévue

- **Modèles par sport**  
  - Ajout de sous-modules dans `app/models/` :
    - `app/models/football/`
    - `app/models/basketball/`
    - `app/models/tennis/`
  - Chaque module aura ses propres modèles et fonctions de prédiction, tout en respectant une interface commune.

- **Données réelles**  
  - Intégration de sources de données (API, fichiers CSV, etc.) pour :
    - récupérer les matchs du jour,
    - les cotes,
    - les stats,
    - les états live.

- **Scheduler pour notifications auto**  
  - Utilisation de `APScheduler` ou d'un cron pour appeler périodiquement `send_auto_alerts` et envoyer les alertes fortes.

- **Suivi de performance**  
  - Enregistrement des analyses et des résultats réels.
  - Calcul a posteriori du ROI, de la précision, etc.
  - Commande `/stats` pour afficher ces métriques.

## Résumé

- Le **cœur QFTE** (calibration, modèles, metrics, backtest) fournit la base scientifique.
- Le **module d'analyse** transforme cette base en prédictions concrètes pour des matchs (1N2, Over/Under, handicap, BTTS, scores).
- Le **bot Telegram** est l'interface utilisateur : il reçoit tes commandes, appelle le module d'analyse, et te renvoie des messages clairs en français.
- Tout est conçu pour être **modulaire** : on peut ajouter de nouveaux sports, modèles, ou marchés sans casser l'ensemble.
