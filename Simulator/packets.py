# simulator/packets.py
# Generates fake network traffic packets with expected allow/deny outcomes.
# Run this file once to produce data/sample_packets.json.

import json
import random
import os

def generate_packets(n=500):
    """
    Creates n synthetic network packets with expected firewall outcomes.

    Each packet is a dict with:
        source   (str): Where traffic is coming from
        dest     (str): Where it's going
        port     (int): Which port
        expected (str): The correct firewall decision — "allow" or "deny"

    Returns:
        list[dict]: A list of packet dictionaries.
    """
    templates = [
        {"source": "internet",  "dest": "webserver", "port": 443,  "expected": "allow"},
        {"source": "internet",  "dest": "webserver", "port": 80,   "expected": "allow"},
        {"source": "internet",  "dest": "database",  "port": 3306, "expected": "deny"},
        {"source": "admin_pc",  "dest": "database",  "port": 3306, "expected": "allow"},
        {"source": "admin_pc",  "dest": "webserver", "port": 22,   "expected": "allow"},
        {"source": "internet",  "dest": "webserver", "port": 22,   "expected": "deny"},
        {"source": "internet",  "dest": "database",  "port": 22,   "expected": "deny"},
        {"source": "admin_pc",  "dest": "webserver", "port": 443,  "expected": "allow"},
    ]
    # Sample with replacement to hit n packets
    return [dict(random.choice(templates)) for _ in range(n)]


def save_packets(path="data/sample_packets.json", n=500):
    """
    Generates packets and writes them to a JSON file.
    Creates the data/ directory if it doesn't exist.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    packets = generate_packets(n)
    with open(path, "w") as f:
        json.dump(packets, f, indent=2)
    print(f"Saved {len(packets)} packets to {path}")


if __name__ == "__main__":
    save_packets()