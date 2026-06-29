# simulator/rules.py
# Defines what a single firewall rule looks like, and the master rule pool
# the GA will select from.

class Rule:
    """
    Represents a single firewall rule.

    Attributes:
        source (str): Traffic origin, e.g. "internet", "admin_pc", "any"
        dest   (str): Traffic destination, e.g. "webserver", "database", "any"
        port   (int|str): Port number or "any"
        action (str): "allow" or "deny"
    """
    def __init__(self, source, dest, port, action):
        self.source = source
        self.dest   = dest
        self.port   = port
        self.action = action

    def __repr__(self):
        return f"Rule({self.source} -> {self.dest}:{self.port} = {self.action})"


# Master rule pool — the GA picks subsets and orderings from this list.
# Think of this as the "gene pool" for your chromosomes.
RULE_POOL = [
    Rule("internet",  "webserver", 443,    "allow"),
    Rule("internet",  "webserver", 80,     "allow"),
    Rule("internet",  "database",  3306,   "deny"),
    Rule("admin_pc",  "database",  3306,   "allow"),
    Rule("admin_pc",  "webserver", 22,     "allow"),
    Rule("internet",  "webserver", 22,     "deny"),
    Rule("any",       "webserver", "any",  "deny"),
    Rule("any",       "database",  "any",  "deny"),
    Rule("admin_pc",  "any",       "any",  "allow"),
    Rule("internet",  "any",       443,    "allow"),
    Rule("internet",  "any",       80,     "allow"),
    Rule("internet",  "any",       22,     "deny"),
    Rule("any",       "any",       3306,   "deny"),
    Rule("admin_pc",  "database",  "any",  "allow"),
    Rule("internet",  "database",  "any",  "deny"),
]