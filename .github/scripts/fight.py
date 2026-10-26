#!/usr/bin/env python3
"""Challenge Zain — plays one round of STRIKE / THROW / GUARD for a GitHub issue,
updates game/state.json and redraws assets/scoreboard.svg.

Triangle (classic fighting-game logic):  STRIKE beats THROW · THROW beats GUARD · GUARD beats STRIKE
Env in: ISSUE_TITLE ("fight|strike"), ISSUE_USER (login).  Out: result.md (issue comment).
"""
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arcade import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "game" / "state.json"
BOARD = ROOT / "assets" / "scoreboard.svg"
BEATS = {"strike": "throw", "throw": "guard", "guard": "strike"}
DEFAULT = {"visitor_wins": 0, "zain_wins": 0, "draws": 0, "rounds": 0, "streak": 0, "best_streak": 0, "recent": []}


def load():
    try:
        s = json.loads(STATE.read_text(encoding="utf-8"))
        return {**DEFAULT, **s}
    except Exception:
        return dict(DEFAULT)


def judge(you, zain):
    if you == zain:
        return "draw"
    return "win" if BEATS[you] == zain else "lose"


def render_scoreboard(s):
    W, H = 880, 392
    body = mono(28, 42, "ARENA SCOREBOARD", 14, GOLD, ls=4)
    body += mono(W - 28, 42, f"ROUNDS PLAYED  {s['rounds']}", 13, DIM, "end", 2)
    body += f'<line x1="28" y1="58" x2="{W - 28}" y2="58" stroke="{EDGE}"/>'
    body += mono(220, 96, "CHALLENGERS", 14, CYA, "middle", 5)
    body += disp(220, 178, s["visitor_wins"], 96, CYA, "middle")
    body += mono(660, 96, "ZAIN", 14, GOLD, "middle", 5)
    body += disp(660, 178, s["zain_wins"], 96, "url(#gold)", "middle")
    body += (f'<g transform="translate(440 150)"><g>{AT("scale", [1, 1.18, 1], dur=1.6)}'
             + disp(0, 22, "VS", 78, RED, "middle", 'stroke="#000" stroke-width="5" paint-order="stroke"') + "</g></g>")
    body += mono(440, 214, f"DRAWS {s['draws']}   ·   CHALLENGER STREAK {s['streak']}   ·   BEST STREAK {s['best_streak']}", 13, SOFT, "middle", 1.5)
    body += f'<line x1="28" y1="232" x2="{W - 28}" y2="232" stroke="{EDGE}"/>'
    body += mono(28, 256, "LAST ROUNDS", 12, DIM, ls=4)
    if not s["recent"]:
        body += f'<g>{blink(2.4)}' + mono(440, 312, "NO FIGHTS YET — BE THE FIRST CHALLENGER", 15, SOFT, "middle", 2) + "</g>"
    y = 284
    for r in s["recent"][:5]:
        col, label = {"win": (CYA, "YOU WIN"), "lose": (GOLD, "ZAIN WINS"), "draw": (DIM, "DRAW")}[r["result"]]
        body += mono(28, y, "@" + r["user"][:22], 15, WHT)
        body += mono(340, y, f"{r['you'].upper()}  vs  {r['zain'].upper()}", 14, SOFT, ls=1)
        body += disp(W - 28, y + 1, label, 19, col, "end")
        y += 22
    body += sweep(W, H, dur=5)
    return svg(W, H, body, f"Arena scoreboard: challengers {s['visitor_wins']}, Zain {s['zain_wins']}", glows=[(220, 140, 150, CYA, 0.12), (660, 140, 150, GOLD, 0.12)])


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
        "The profile scoreboard updates within a minute or two. Thanks for playing!\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
