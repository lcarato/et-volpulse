from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
from weasyprint import HTML

from .data_feed import get_prices
from .weights import get_weights
from .metrics import calc_trvi


def build_report() -> Path:
    today = date.today()
    start = today - timedelta(days=14)
    prices = get_prices(start, today)
    close = prices.unstack("ticker")["Close"]
    ret = close.pct_change().dropna()
    weights = get_weights(pd.Timestamp(today))
    trvi = calc_trvi(ret, weights)

    fig, ax = plt.subplots()
    trvi.plot(ax=ax)
    img_path = Path("reports/trvi.png")
    img_path.parent.mkdir(exist_ok=True)
    fig.savefig(img_path)
    plt.close(fig)

    template = Template("""# Weekly ET Vol Report\n![TRVI](trvi.png)""")
    html = template.render()
    report_path = Path(f"reports/{today:%Y-%W}.pdf")
    HTML(string=html, base_url=img_path.parent).write_pdf(report_path)
    return report_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    path = build_report()
    print(f"Report saved to {path}")


if __name__ == "__main__":
    main()
