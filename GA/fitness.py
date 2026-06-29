# ga/fitness.py
# Computes the fitness score for a single chromosome (firewall).
# Higher score = better firewall.
#
# Formula: fitness = 1000 * accuracy - 10 * num_rules - avg_lookup_cost
#
# - Accuracy is weighted heavily (we care most about correct decisions)
# - Penalize for too many rules (simpler firewalls are better)
# - Penalize for slow lookups (fewer steps = faster real-world performance)

from simulator.evaluator import evaluate_firewall


def compute_fitness(chromosome, packets):
    """
    Scores a chromosome against the full packet test suite.

    Args:
        chromosome (Chromosome): A Chromosome object whose .rules we evaluate.
        packets    (list[dict]): All test packets loaded from sample_packets.json.

    Returns:
        float: The fitness score. Higher is better.
    """
    stats = evaluate_firewall(chromosome.rules, packets)

    fitness = (
        1000 * stats["accuracy"]
        - 10  * stats["num_rules"]
        - stats["avg_lookup_cost"]
    )
    return fitness