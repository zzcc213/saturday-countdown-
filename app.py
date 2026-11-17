"""Зворотний відлік: скільки днів лишилося до наступної суботи."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from flask import Flask, render_template_string

app = Flask(__name__)

KYIV = ZoneInfo("Europe/Kyiv")
SATURDAY = 5  # date.weekday(): понеділок = 0, неділя = 6
WEEKDAYS = [
    "понеділок",
    "вівторок",
    "середа",
    "четвер",
    "п’ятниця",
    "субота",
    "неділя",
]

PAGE = """<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Зворотний відлік до суботи</title>
  <style>
    body { margin: 0; min-height: 100vh; display: flex; align-items: center;
           justify-content: center; font-family: system-ui, sans-serif;
           background: #f3f5f8; color: #1d2733; }
    main { text-align: center; padding: 2rem; }
    .days { font-size: 7rem; font-weight: 700; line-height: 1; color: #2b5fa8; }
    .label { font-size: 1.6rem; margin: .5rem 0; }
    .info { margin-top: 1.5rem; color: #5a6878; }
  </style>
</head>
<body>
  <main>
    <div class="label">Лишилося</div>
    <div class="days">{{ days }}</div>
    <div class="label">{{ word }} до наступної суботи</div>
    <p class="info">Сьогодні {{ today }}, {{ weekday }}.<br>
       Наступна субота — {{ saturday }}.</p>
  </main>
</body>
</html>"""


def days_until_saturday(today: date) -> int:
    """Повертає кількість днів до наступної суботи (у суботу — 7)."""
    days = (SATURDAY - today.weekday()) % 7
    return days or 7


def days_word(n: int) -> str:
    """Повертає слово «день» у потрібній формі для числа n."""
    if n % 10 == 1 and n % 100 != 11:
        return "день"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "дні"
    return "днів"


@app.route("/")
def index():
    today = datetime.now(KYIV).date()
    days = days_until_saturday(today)
    saturday = today + timedelta(days=days)
    return render_template_string(
        PAGE,
        days=days,
        word=days_word(days),
        today=today.strftime("%d.%m.%Y"),
        weekday=WEEKDAYS[today.weekday()],
        saturday=saturday.strftime("%d.%m.%Y"),
    )


if __name__ == "__main__":
    app.run(debug=True)
