# ga/chromosome.py
# A chromosome represents one candidate firewall solution.
# It's an ordered subset of rules drawn from RULE_POOL in rules.py.

import random
from simulator.rules import RULE_POOL


class Chromosome:
    """
    Represents a single firewall configuration (one individual in the GA population).

    Attributes:
        rules (list[Rule]): An ordered list of rules — this IS the firewall.
                            Order matters: first matching rule wins.
    """

    def __init__(self, rules=None):
        """
        Creates a chromosome.

        If no rules are passed, generates a random firewall by sampling
        a random subset of RULE_POOL and shuffling the order.

        Args:
            rules (list[Rule], optional): Provide specific rules to create
                                          a chromosome directly (used in crossover).
        """
        if rules is not None:
            self.rules = rules
        else:
            # Random initialization: pick between 5–12 rules, shuffle the order
            k = random.randint(5, 12)
            self.rules = random.sample(RULE_POOL, k)

    def __repr__(self):
        return f"Chromosome({len(self.rules)} rules)"