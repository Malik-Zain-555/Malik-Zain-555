#!/usr/bin/env python3
"""Play a round vs Zain — plays one round of STRIKE / THROW / GUARD for a GitHub issue,
updates game/state.json and redraws assets/scoreboard.svg.

STRIKE beats THROW · THROW beats GUARD · GUARD beats STRIKE
Env in: ISSUE_TITLE ("fight|strike"), ISSUE_USER (login).  Out: result.md (issue comment).
"""
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "game" / "state.json"
BOARD = ROOT / "assets" / "scoreboard.svg"
BEATS = {"strike": "throw", "throw": "guard", "guard": "strike"}
DEFAULT = {"visitor_wins": 0, "zain_wins": 0, "draws": 0, "rounds": 0, "streak": 0, "best_streak": 0, "recent": []}


def load():
    try:
        return {**DEFAULT, **json.loads(STATE.read_text(encoding="utf-8"))}
    except Exception:
        return dict(DEFAULT)


def judge(you, zain):
    if you == zain:
        return "draw"
    return "win" if BEATS[you] == zain else "lose"


def render_scoreboard(s):
    W, H = 880, 372
    body = mono(32, 44, "SCOREBOARD", 12, OR, ls=3) + mono(W - 32, 44, f"ROUNDS PLAYED  {s['rounds']}", 12, MUT, "end", 1.5)
    body += f'<line x1="32" y1="62" x2="{W - 32}" y2="62" stroke="{LINE}"/>'
    body += mono(220, 100, "CHALLENGERS", 12, SOFT, "middle", 3) + serif(220, 178, s["visitor_wins"], 84, MINT, "middle")
    body += mono(660, 100, "ZAIN", 12, SOFT, "middle", 3) + serif(660, 178, s["zain_wins"], 84, OR, "middle")
    body += serif(440, 160, "vs", 38, MUT, "middle", True)
    body += mono(440, 214, f"DRAWS {s['draws']}   ·   CURRENT STREAK {s['streak']}   ·   BEST STREAK {s['best_streak']}", 12, SOFT, "middle", 1)
    body += f'<line x1="32" y1="234" x2="{W - 32}" y2="234" stroke="{LINE}"/>' + mono(32, 258, "LAST ROUNDS", 11, MUT, ls=3)
    if not s["recent"]:
        body += f'<g>{blink(2.4)}' + serif(440, 320, "No fights yet. Be the first challenger.", 20, SOFT, "middle", True) + "</g>"
    y = 288
    for r in s["recent"][:5]:
        col, label = {"win": (MINT, "you win"), "lose": (OR, "Zain wins"), "draw": (MUT, "draw")}[r["result"]]
        body += mono(32, y, "@" + r["user"][:22], 13, TX) + mono(330, y, f"{r['you'].upper()}  vs  {r['zain'].upper()}", 12, SOFT, ls=1)
        body += serif(W - 32, y + 1, label, 16, col, "end", True)
        y += 22
    body += tick(W, H - 1, OR, 6)
    return svg(W, H, body, f"Scoreboard: challengers {s['visitor_wins']}, Zain {s['zain_wins']}")


def main():
    title = os.environ.get("ISSUE_TITLE", "").strip().lower()
    user = os.environ.get("ISSUE_USER", "someone")
    parts = title.split("|")
    choice = parts[1].strip() if len(parts) == 2 and parts[0].strip() == "fight" else ""
    if choice not in BEATS:
        (ROOT / "result.md").write_text("That wasn't a valid move. Use the STRIKE / THROW / GUARD buttons on the profile.\n", encoding="utf-8")
        return
    s = load()
    zain = random.SystemRandom().choice(list(BEATS))
    res = judge(choice, zain)
    s["rounds"] += 1
    if res == "win":
        s["visitor_wins"] += 1
        s["streak"] += 1
        s["best_streak"] = max(s["best_streak"], s["streak"])
    elif res == "lose":
        s["zain_wins"] += 1
        s["streak"] = 0
    else:
        s["draws"] += 1
    s["recent"] = ([{"user": user, "you": choice, "zain": zain, "result": res}] + s["recent"])[:6]
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
    BOARD.write_text(render_scoreboard(s), encoding="utf-8")
    verdict = {"win": "**You win. 🏆** Zain has been defeated.", "lose": "**Zain wins this round.** 🥋 Try again.", "draw": "**Draw.** Both read each other perfectly."}[res]
    (ROOT / "result.md").write_text(
        f"## Round {s['rounds']}\n\n@{user} chose **{choice.upper()}** · Zain chose **{zain.upper()}**\n\n{verdict}\n\n"
        f"Score: challengers **{s['visitor_wins']}** · Zain **{s['zain_wins']}** · draws **{s['draws']}**\n\n"
        "The profile scoreboard updates within a minute or two. Thanks for playing!\n", encoding="utf-8")


if __name__ == "__main__":
    main()
