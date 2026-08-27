from datetime import date

from reorder_drift import Order, detect_reorder_drift


def test_flags_accounts_past_their_normal_reorder_interval():
    orders = [
        Order("A", date(2026, 1, 1)),
        Order("A", date(2026, 1, 31)),
        Order("A", date(2026, 3, 2)),
    ]
    alerts = detect_reorder_drift(orders, date(2026, 4, 15), drift_threshold=1.25)
    assert len(alerts) == 1
    assert alerts[0].account_id == "A"
    assert alerts[0].typical_interval_days == 30.0
    assert alerts[0].days_since_last_order == 44


def test_does_not_flag_accounts_with_insufficient_history():
    orders = [
        Order("B", date(2026, 1, 1)),
        Order("B", date(2026, 2, 1)),
    ]
    assert detect_reorder_drift(orders, date(2026, 4, 15)) == []


def test_orders_alerts_by_severity():
    orders = [
        Order("A", date(2026, 1, 1)),
        Order("A", date(2026, 1, 31)),
        Order("A", date(2026, 3, 2)),
        Order("B", date(2026, 1, 1)),
        Order("B", date(2026, 1, 11)),
        Order("B", date(2026, 1, 21)),
    ]
    alerts = detect_reorder_drift(orders, date(2026, 4, 15))
    assert [alert.account_id for alert in alerts] == ["B", "A"]
