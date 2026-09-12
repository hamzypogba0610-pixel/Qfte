# Roadmap du projet QFTE

Ce document décrit les prochaines étapes pour faire évoluer QFTE depuis l'architecture actuelle jusqu'à un bot Telegram pleinement opérationnel, multi-sports, avec analyses pré-live et live.

## État actuel (v22 – socle + bot squelette)

À ce stade, le projet dispose de :

- **Cœur scientifique QFTE**
  - Calibration (Platt, Isotonic, Beta, Temperature Scaling, etc.).
  - Modèles de base (logistic regression, naive bayes, arbre, modèles de scores).
  - Métriques (Log Loss, Brier, ECE, etc.).
  - Backtest (PnL, Sharpe, drawdown, etc.).

- **Module d'analyse de matchs (`app/analysis/`)**
  - Structures de données (`MatchAnalysis`, `MarketPrediction`).
  - Configuration (seuils, modes, règles).
  - Fonctions `analyze_match_pre_live` et `analyze_match_live` (placeholders).
  - Sélection des 2 matchs fiables du jour (`selector.py`).

- **Bot Telegram (`bot/`)**
  - Configuration (token, user ID, seuils).
  - Formatage des messages en français.
  - Commandes : `/start`, `/help`, `/today`, `/next`, `/live`, `/analyse`, `/top2`.
  - Squelette de notifications automatiques.

- **Documentation**
  - `README.md` : présentation, structure, exemples, instructions pour le bot.
  - `ARCHITECTURE.md` : description détaillée de l'architecture et des flux.
  - `ROADMAP.md` : ce fichier.

L'objectif maintenant est de **remplacer les placeholders par de vrais modèles et de vraies données**, puis de rendre le bot pleinement opérationnel.

---

## Phase 1 – Finaliser les modèles par sport

Objectif : avoir, pour chaque sport, des modèles capables de produire des probabilités brutes pour tous les marchés requis.

### 1.1. Football

- **Marchés à couvrir** :
  - 1N2 (victoire domicile / nul / victoire extérieur).
  - Over/Under 1.5, 2.5, 3.5 buts.
  - Handicap asiatique.
  - BTTS (les deux équipes marquent).
  - Distribution des scores (HT et FT).

- **Travaux à faire** :
  - Créer `app/models/football/` :
    - `predict_1n2.py` : modèle de prédiction 1N2.
    - `predict_ou.py` : modèle Over/Under.
    - `predict_handicap.py` : modèle handicap.
    - `predict_btts.py` : modèle BTTS.
    - `predict_scores.py` : distribution des scores (Poisson, Dixon-Coles, etc.).
  - Relier ces modèles à `app/analysis/predictor.py` :
    - remplacer les fonctions `_build_*_prediction` placeholders par des appels aux vrais modèles.
  - Intégrer la calibration :
    - utiliser `app/calibration/` pour calibrer chaque type de probabilité.

- **Critère de fin de phase** :
  - Pour un match de foot avec données d'entrée, `analyze_match_pre_live` renvoie des probabilités réalistes et calibrées pour tous les marchés.

### 1.2. Basketball

- **Marchés à couvrir** :
  - Vainqueur (1 ou 2).
  - Over/Under 1.5, 2.5, 3.5 (à adapter : total de points, quarters, etc.).
  - Handicap.

- **Travaux à faire** :
  - Créer `app/models/basketball/` :
    - modèles de total de points, handicap, vainqueur.
  - Adapter `predictor.py` pour le basketball.

### 1.3. Tennis

- **Marchés à couvrir** :
  - Vainqueur (joueur 1 / joueur 2).
  - Over/Under (sets, games).
  - Handicap (sets ou games).

- **Travaux à faire** :
  - Créer `app/models/tennis/`.
  - Adapter `predictor.py`.

---

## Phase 2 – Données réelles (matchs, cotes, stats)

Objectif : alimenter le moteur avec de vraies données de matchs, cotes et statistiques.

### 2.1. Sources de données

- Définir les sources :
  - API de scores/cotes (ex. : API-Football, SportMonks, etc.) ou
  - Fichiers CSV/Excel mis à jour régulièrement.
- Pour chaque sport, lister les champs nécessaires :
  - équipes / joueurs,
  - compétition,
  - date/heure,
  - cotes (1N2, O/U, handicap, BTTS),
  - stats récentes (forme, buts/points, etc.),
  - état live (score, minute, etc.).

### 2.2. Module d'ingestion

- Créer `app/data/sources/` ou `app/ingestion/` :
  - fonctions pour :
    - récupérer la liste des matchs du jour,
    - récupérer les cotes,
    - récupérer les stats,
    - récupérer l'état live.
- Normaliser les données dans un format commun utilisé par `predictor.py`.

### 2.3. Intégration avec le bot

- Modifier `bot/telegram_bot.py` :
  - remplacer `_dummy_matches_today()` par un appel aux vraies sources.
  - pour `/today`, `/next`, `/live`, afficher les vrais matchs.

---

## Phase 3 – Analyse live avancée

Objectif : avoir une vraie analyse en temps réel, adaptée au score et au temps écoulé.

### 3.1. Modèles live

- Pour chaque sport, développer des modèles conditionnels :
  - ex. : proba de finir Over 2.5 sachant 1-0 à la 30e minute.
  - ex. : proba de victoire sachant le score et le temps restant.

### 3.2. Mise à jour en temps réel

- Dans `app/analysis/live.py` :
  - fonctions pour recalculer les probas en fonction du score et du temps.
- Dans `predictor.py` :
  - utiliser ces fonctions dans `analyze_match_live`.

### 3.3. Commandes live du bot

- `/live` : liste des matchs en cours avec un résumé.
- `/live Équipe1 Équipe2` : analyse live complète (1N2, O/U, handicap, score FT probable, etc.).

---

## Phase 4 – Notifications automatiques et scheduler

Objectif : que le bot t'envoie automatiquement les meilleures opportunités, sans que tu aies à demander.

### 4.1. Scheduler

- Utiliser `APScheduler` (déjà dans `requirements.txt`) :
  - planifier une tâche toutes les heures (ou à une fréquence définie).
  - cette tâche :
    - récupère les matchs du jour,
    - lance les analyses,
    - détecte les opportunités fortes (selon les seuils dans `bot/config.py`),
    - envoie les alertes via Telegram.

### 4.2. Règles de notification

- Définir précisément :
  - quelles conditions déclenchent une notif auto (confiance, edge, nombre de marchés forts),
  - à quels moments de la journée (ex. : pas de notif la nuit).

---

## Phase 5 – Suivi de performance et commande `/stats`

Objectif : mesurer a posteriori la performance des analyses et des paris recommandés.

### 5.1. Enregistrement des analyses

- Créer un module `app/logging/` ou `app/tracking/` :
  - enregistrer chaque analyse envoyée :
    - match,
    - prédictions,
    - confiances,
    - edge,
    - recommandations.

### 5.2. Enregistrement des résultats

- Après chaque match :
  - récupérer le résultat réel,
  - comparer avec les prédictions,
  - calculer :
    - précision par marché,
    - ROI simulé (si on suit les recommandations),
    - performance par sport, par type de pari.

### 5.3. Commande `/stats`

- Dans le bot :
  - `/stats` : affiche :
    - nombre d'analyses,
    - % de bons pronostics,
    - ROI global,
    - performance par type de marché.

---

## Phase 6 – Améliorations et extensions

Une fois les phases 1–5 réalisées, on pourra :

- Ajouter d'autres sports (hockey, volleyball, etc.).
- Ajouter d'autres marchés (corners, cartons, mi-temps/fin de match, etc.).
- Améliorer l'interface (messages plus riches, graphiques, etc.).
- Eventuellement ouvrir le bot à d'autres utilisateurs (gestion de droits, abonnements, etc.).

---

## Résumé des priorités

1. **Phase 1** : vrais modèles par sport (foot, basket, tennis).
2. **Phase 2** : données réelles (matchs, cotes, stats).
3. **Phase 3** : analyse live avancée.
4. **Phase 4** : scheduler + notifications auto.
5. **Phase 5** : suivi de performance et `/stats`.

Chaque phase peut être découpée en petites étapes, fichier par fichier, comme on a fait jusqu'ici.
