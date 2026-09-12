# bot/messages.py
"""
Formatage des messages du bot Telegram (en français).
"""

from typing import List, Optional
from app.analysis.types import MatchAnalysis, MarketPrediction


def _format_market(m: Optional[MarketPrediction], label: str) -> str:
    """
    Formate un marché (1N2, OU, handicap, etc.) en une ligne lisible.
    """
    if m is None:
        return f"{label}: non disponible"

    lines = [
        f"{label}:",
        f"  - Recommandation : {m.recommendation}",
        f"  - Confiance : {m.confidence:.1f}/10",
    ]
    if m.proba is not None:
        lines.append(f"  - Probabilité : {m.proba:.1%}")
    return "
".join(lines)


def format_match_analysis(analysis: MatchAnalysis) -> str:
    """
    Formate une analyse complète de match pour une réponse à /analyse.
    """
    sport_emoji = {
        "football": "⚽",
        "basketball": "🏀",
        "tennis": "🎾",
    }.get(analysis.sport, "📊")

    header_lines = [
        f"{sport_emoji} {analysis.home} vs {analysis.away}",
        f"🏆 {analysis.competition}",
        f"🕒 {analysis.start_time}",
    ]

    if analysis.is_live:
        header_lines.append(f"🔴 LIVE – Score : {analysis.score_current} ({analysis.minute})")
    else:
        header_lines.append("📅 Pré-live")

    header = "
".join(header_lines)

    # 1N2 / vainqueur
    if analysis.sport == "tennis":
        winner_label = "📊 Vainqueur"
    else:
        winner_label = "📊 1N2"

    winner_txt = _format_market(analysis.winner, winner_label)

    # Over/Under
    ou_lines = [
        "📈 Over/Under",
        _format_market(analysis.ou_1_5, "  OU 1.5"),
        _format_market(analysis.ou_2_5, "  OU 2.5"),
        _format_market(analysis.ou_3_5, "  OU 3.5"),
    ]
    ou_txt = "
".join(ou_lines)

    # Handicap
    handicap_txt = _format_market(analysis.handicap, "📉 Handicap")

    # BTTS (football uniquement)
    btts_txt = ""
    if analysis.btts is not None:
        btts_txt = _format_market(analysis.btts, "🎯 BTTS (les deux équipes marquent)")

    # Scores
    score_txt_parts = []
    if analysis.score_ht is not None:
        score_txt_parts.append(
            f"⏱ Score HT le plus probable : {analysis.score_ht.recommendation} "
            f"(proba ≈ {analysis.score_ht.proba:.1%})"
        )
    if analysis.score_ft is not None:
        score_txt_parts.append(
            f"🏁 Score FT le plus probable : {analysis.score_ft.recommendation} "
            f"(proba ≈ {analysis.score_ft.proba:.1%})"
        )
    score_txt = "
".join(score_txt_parts) if score_txt_parts else "Scores non disponibles"

    # Synthèse
    synthese_lines = [
        "🧾 Synthèse",
        f"  - Confiance globale : {analysis.global_confidence:.1f}/10",
        f"  - Edge : {analysis.edge:.1%}",
        f"  - Marchés forts (≥ 7,5) : {analysis.strong_markets_count}",
    ]
    synthese_txt = "
".join(synthese_lines)

    # Assemblage final
    parts = [
        header,
        "",
        winner_txt,
        "",
        ou_txt,
        "",
        handicap_txt,
    ]

    if btts_txt:
        parts.append("")
        parts.append(btts_txt)

    parts.extend([
        "",
        score_txt,
        "",
        synthese_txt,
    ])

    return "
".join(parts)


def format_top2_matches(analyses: List[MatchAnalysis]) -> str:
    """
    Formate les 2 matchs les plus fiables du jour pour /top2.
    """
    if not analyses:
        return "Aucun match fiable détecté aujourd’hui selon les critères QFTE."

    lines = [
        "🎯 2 matchs fiables du jour (QFTE v22)",
        "",
    ]

    for i, a in enumerate(analyses, start=1):
        sport_emoji = {
            "football": "⚽",
            "basketball": "🏀",
            "tennis": "🎾",
        }.get(a.sport, "📊")

        rec_globale = "N/A"
        if a.winner:
            rec_globale = a.winner.recommendation

        lines.extend([
            f"{i}) {sport_emoji} {a.home} vs {a.away} – {a.competition}",
            f"   - Recommandation principale : {rec_globale}",
            f"   - Confiance globale : {a.global_confidence:.1f}/10",
            f"   - Edge : {a.edge:.1%}",
            f"   - Marchés forts : {a.strong_markets_count}",
            "",
        ])

    lines.append("Utilise /analyse Équipe1 Équipe2 pour voir l’analyse détaillée d’un match.")

    return "
".join(lines)


def format_match_list(matches: List[dict], title: str) -> str:
    """
    Formate une liste de matchs (pour /today, /next, /live).

    matches : liste de dicts avec au moins :
      - sport: str
      - competition: str
      - home: str
      - away: str
      - start_time: str
      - is_live: bool
      - score_current: Optional[str]
      - minute: Optional[str]
    """
    if not matches:
        return f"Aucun match trouvé pour : {title}."

    lines = [f"📅 {title}", ""]

    for m in matches:
        sport_emoji = {
            "football": "⚽",
            "basketball": "🏀",
            "tennis": "🎾",
        }.get(m["sport"], "📊")

        if m.get("is_live"):
            live_tag = f" 🔴 LIVE – {m.get('score_current', '?')} ({m.get('minute', '?')})"
        else:
            live_tag = ""

        lines.append(
            f"{sport_emoji} {m['home']} vs {m['away']} – {m['competition']} "
            f"({m['start_time']}){live_tag}"
        )

    lines.append("")
    lines.append("Utilise /analyse Équipe1 Équipe2 pour lancer une analyse détaillée.")

    return "
".join(lines)


def format_auto_alert(analysis: MatchAnalysis) -> str:
    """
    Formate une alerte automatique pour opportunité forte.
    """
    sport_emoji = {
        "football": "⚽",
        "basketball": "🏀",
        "tennis": "🎾",
    }.get(analysis.sport, "📊")

    rec_globale = "N/A"
    if analysis.winner:
        rec_globale = analysis.winner.recommendation

    lines = [
        "🚨 Opportunité forte détectée (QFTE v22)",
        "",
        f"{sport_emoji} {analysis.home} vs {analysis.away} – {analysis.competition}",
        f"🕒 {analysis.start_time}",
        "",
        f"- Recommandation principale : {rec_globale}",
        f"- Confiance globale : {analysis.global_confidence:.1f}/10",
        f"- Edge : {analysis.edge:.1%}",
        f"- Marchés forts : {analysis.strong_markets_count}",
        "",
        "Utilise /analyse Équipe1 Équipe2 pour voir l’analyse complète.",
    ]

    return "
".join(lines)
