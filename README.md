QFTE

QFTE est un projet Python pour l'entraînement et l'évaluation de modèles de prédiction, avec un accent sur la calibration des probabilités.

Structure principale

· app/calibration/ : méthodes de calibration (Platt, Isotonic, Beta, Temperature Scaling, etc.) et recalibration adaptative.
· app/models/ : modèles de classification :
  · LogisticRegression
  · GaussianNaiveBayes
  · SimpleDecisionTree
  · ainsi que des modèles de scores (Poisson, Dixon-Coles, etc.).
· app/metrics/ : métriques (Log Loss, Brier score, ECE, etc.).
· app/data/ : chargement et préprocessing des données.
· app/utils/ : utilitaires (I/O, validation, etc.).
· app/experiments/ : configurations et lancement d'expériences.
· app/backtest/ : moteur de backtest et métriques de performance (PnL, Sharpe, drawdown, etc.).
· app/analysis/ : module d'analyse de matchs (pré-live et live) pour football, basketball, tennis.
· bot/ : bot Telegram privé pour interroger le moteur QFTE et recevoir des analyses et alertes.
· examples/ : scripts d'exemple pour chaque module.

Exemples

Voir le dossier examples/ :

```bash
# Démarrage rapide
python examples/quickstart.py

# Calibration seule
python examples/calibration_example.py

# Modèle + calibration
python examples/logistic_calibration_example.py

# Pipeline complet avec data
python examples/full_data_pipeline_example.py

# Expériences configurées
python examples/experiment_example.py

# Comparaison de modèles
python examples/compare_models_example.py

# Backtest football
python examples/backtest_football_example.py
```

Lancer le pipeline

Pour lancer le pipeline complet (calibration + backtest) sur les données d'exemple :

```bash
python scripts/run_full_pipeline.py
```

Cela charge data/sample_matches.csv, calibre les probabilités et affiche :

· les métriques de calibration (Log Loss, Brier, ECE),
· les performances du backtest (PnL, Sharpe, drawdown).

Bot Telegram

Le bot Telegram QFTE est un assistant privé pour analyser des matchs (football, basketball, tennis) avec la méthodologie QFTE (modèles + calibration + backtest).

Configuration

1. Crée un bot via @BotFather sur Telegram :
   · Envoie /newbot et suis les instructions.
   · Copie le token fourni (ex. : 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11).
2. Récupère ton user ID Telegram :
   · Utilise un bot comme @userinfobot ou @getmyid_bot.
   · Note ton user ID (nombre entier, ex. : 123456789).
3. Dans le fichier bot/config.py :
   · Remplace TELEGRAM_BOT_TOKEN = "TON_TOKEN_ICI" par ton token.
   · Remplace TELEGRAM_USER_ID = 0 par ton user ID.

Installation des dépendances

Depuis la racine du projet :

```bash
pip install -r requirements.txt
```

Lancer le bot

Depuis la racine du projet :

```bash
python scripts/run_bot.py
```

Commandes disponibles

· /start : message de bienvenue
· /help : aide et liste des commandes
· /today : matchs du jour
· /next : matchs à venir (24–48h)
· /live : matchs en cours
· /analyse Équipe1 Équipe2 : analyse complète d'un match
· /top2 : les 2 matchs les plus fiables du jour selon QFTE

Le bot peut aussi t'envoyer automatiquement des alertes pour les opportunités les plus fortes (confiance élevée, edge important).

Installation

```bash
git clone <ton-depot>
cd Qfte
```

Puis utilise Python 3.10+ avec les dépendances standards (numpy, scipy, python-telegram-bot, etc.).

Licence

À définir
