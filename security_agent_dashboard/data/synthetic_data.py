"""
Synthetic Security Event Generator
-----------------------------------
Generates FAKE, illustrative cybersecurity event data for the research
prototype. No real network traffic, real IP reputation data, or real
credentials are used anywhere in this module. All "threat intelligence"
indicators are hard-coded, made-up labels used purely to demonstrate how
a multi-agent pipeline could reason over such data.
"""

import random
from datetime import datetime, timedelta

import pandas as pd

# ---------------------------------------------------------------------------
# Static "known-bad" synthetic threat intel indicators (fictional, for demo)
# ---------------------------------------------------------------------------
SYNTHETIC_THREAT_INTEL_IPS = {
    "203.0.113.77": "Reported in synthetic feed: credential-stuffing infrastructure",
    "198.51.100.23": "Reported in synthetic feed: known brute-force relay",
    "192.0.2.184": "Reported in synthetic feed: anonymizing proxy exit node",
}

NORMAL_LOCATIONS = ["Chennai, IN", "Coimbatore, IN", "Bengaluru, IN", "Mumbai, IN"]
UNUSUAL_LOCATIONS = ["Lagos, NG", "Kyiv, UA", "Manila, PH", "Bucharest, RO"]

USERNAMES = ["r.menon", "s.iyer", "a.khan", "j.fernandes", "p.raman", "v.das"]


def _random_ip(pool_bad=False):
    if pool_bad:
        return random.choice(list(SYNTHETIC_THREAT_INTEL_IPS.keys()))
    return f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"


def generate_normal_events(n=40, start_time=None):
    """Generate benign, everyday login events."""
    start_time = start_time or (datetime.now() - timedelta(hours=6))
    rows = []
    for i in range(n):
        ts = start_time + timedelta(minutes=random.randint(0, 300))
        rows.append(
            {
                "event_id": f"EVT-{1000+i}",
                "timestamp": ts,
                "username": random.choice(USERNAMES),
                "ip_address": _random_ip(),
                "location": random.choice(NORMAL_LOCATIONS),
                "hour_of_day": ts.hour,
                "success": True,
                "failed_attempts_in_window": 0,
                "suspicious_indicator": False,
                "event_type": "login_success",
            }
        )
    return rows


def generate_suspicious_login_incident(anchor_time=None):
    """
    Build the canonical demo incident: a burst of failed logins followed
    by a success, from an unusual location, at an unusual hour, from an
    IP that matches a synthetic threat-intel indicator.
    """
    anchor_time = anchor_time or datetime.now()
    username = "s.iyer"
    bad_ip = _random_ip(pool_bad=True)
    unusual_location = random.choice(UNUSUAL_LOCATIONS)
    unusual_hour = 3  # 3 AM local — unusual for this fictional user

    base_ts = anchor_time.replace(
        hour=unusual_hour, minute=random.randint(0, 20), second=0, microsecond=0
    )

    rows = []
    num_failures = 6
    for i in range(num_failures):
        ts = base_ts + timedelta(seconds=i * 20)
        rows.append(
            {
                "event_id": f"EVT-INC-{i}",
                "timestamp": ts,
                "username": username,
                "ip_address": bad_ip,
                "location": unusual_location,
                "hour_of_day": ts.hour,
                "success": False,
                "failed_attempts_in_window": i + 1,
                "suspicious_indicator": True,
                "event_type": "login_failed",
            }
        )

    # Final "successful" login after the failed burst — classic account
    # take-over pattern used purely for demonstration purposes.
    final_ts = base_ts + timedelta(seconds=num_failures * 20 + 15)
    rows.append(
        {
            "event_id": f"EVT-INC-{num_failures}",
            "timestamp": final_ts,
            "username": username,
            "ip_address": bad_ip,
            "location": unusual_location,
            "hour_of_day": final_ts.hour,
            "success": True,
            "failed_attempts_in_window": num_failures,
            "suspicious_indicator": True,
            "event_type": "login_success_after_failures",
        }
    )
    return rows


def build_dataset(include_incident=True):
    """Return a full synthetic event log as a pandas DataFrame."""
    rows = generate_normal_events(n=40)
    if include_incident:
        rows += generate_suspicious_login_incident()
    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df
