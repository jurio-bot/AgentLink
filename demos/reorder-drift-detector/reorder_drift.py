from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class Order:
    account_id: str
    order_date: date


@dataclass(frozen=True)
class ReorderAlert:
    account_id: str
    last_order_date: date
    typical_interval_days: float
    days_since_last_order: int
    drift_ratio: float


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_orders(rows: Iterable[dict[str, str]]) -> list[Order]:
    orders: list[Order] = []
    for row in rows:
        account_id = row["account_id"].strip()
        if not account_id:
            continue
        orders.append(
            Order(
                account_id=account_id,
                order_date=_parse_date(row["order_date"].strip()),
            )
        )
    return orders


def detect_reorder_drift(
    orders: Iterable[Order],
    as_of: date,
    min_orders: int = 3,
    drift_threshold: float = 1.25,
) -> list[ReorderAlert]:
    by_account: dict[str, list[date]] = defaultdict(list)
    for order in orders:
        by_account[order.account_id].append(order.order_date)

    alerts: list[ReorderAlert] = []
    for account_id, dates in by_account.items():
        dates = sorted(set(dates))
        if len(dates) < min_orders:
            continue

        intervals = [
            (later - earlier).days
            for earlier, later in zip(dates, dates[1:])
            if (later - earlier).days > 0
        ]
        if not intervals:
            continue

        typical_interval = float(median(intervals))
        if typical_interval <= 0:
            continue

        days_since_last = (as_of - dates[-1]).days
        if days_since_last < 0:
            continue

        drift_ratio = days_since_last / typical_interval
        if drift_ratio >= drift_threshold:
            alerts.append(
                ReorderAlert(
                    account_id=account_id,
                    last_order_date=dates[-1],
                    typical_interval_days=typical_interval,
                    days_since_last_order=days_since_last,
                    drift_ratio=drift_ratio,
                )
            )

    return sorted(alerts, key=lambda alert: alert.drift_ratio, reverse=True)
