# simulator/evaluator.py
# Simulates packet traversal through an ordered firewall rule list.
# Returns accuracy, rule count, and average lookup steps — the three
# inputs to the fitness function.

def match_rule(rule, packet):
    """
    Checks whether a single rule applies to a given packet.

    A rule matches if source, dest, and port all match (or are "any").

    Args:
        rule   (Rule):  A Rule object from rules.py
        packet (dict):  A packet dict with keys source, dest, port

    Returns:
        bool: True if the rule applies to this packet.
    """
    source_match = (rule.source == "any" or rule.source == packet["source"])
    dest_match   = (rule.dest   == "any" or rule.dest   == packet["dest"])
    port_match   = (rule.port   == "any" or rule.port   == packet["port"])
    return source_match and dest_match and port_match


def evaluate_packet(firewall, packet):
    """
    Walks an ordered list of rules (the firewall) top-to-bottom.
    Returns the action of the first matching rule, plus how many
    steps it took to find it.

    Args:
        firewall (list[Rule]): Ordered list of Rule objects — one chromosome.
        packet   (dict):       A single packet to evaluate.

    Returns:
        tuple: (action: str, steps: int)
               action is "allow" or "deny" (defaults to "deny" if no match).
               steps is how many rules were checked before a match.
    """
    for i, rule in enumerate(firewall):
        if match_rule(rule, packet):
            return rule.action, i + 1  # i+1 because steps are 1-indexed
    return "deny", len(firewall)  # default deny if nothing matched


def evaluate_firewall(firewall, packets):
    """
    Scores a complete firewall against all test packets.
    This is called by fitness.py to compute the three components
    of the fitness formula.

    Args:
        firewall (list[Rule]): An ordered list of Rule objects.
        packets  (list[dict]): All test packets from sample_packets.json.

    Returns:
        dict with:
            accuracy        (float): Fraction of packets correctly handled (0.0–1.0)
            num_rules       (int):   Total rules in this firewall
            avg_lookup_cost (float): Average number of rules checked per packet
    """
    correct = 0
    total_steps = 0

    for packet in packets:
        action, steps = evaluate_packet(firewall, packet)
        total_steps += steps
        if action == packet["expected"]:
            correct += 1

    return {
        "accuracy":        correct / len(packets),
        "num_rules":       len(firewall),
        "avg_lookup_cost": total_steps / len(packets),
    }