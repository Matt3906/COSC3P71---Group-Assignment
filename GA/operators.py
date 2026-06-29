# ga/operators.py
# The three genetic operators that drive evolution across generations.

import random
from ga.chromosome import Chromosome
from simulator.rules import RULE_POOL


def selection(population, fitnesses, tournament_size=3):
    """
    Tournament selection: randomly picks tournament_size chromosomes,
    returns the one with the highest fitness as a parent.

    Args:
        population     (list[Chromosome]): Current generation.
        fitnesses      (list[float]):      Corresponding fitness scores.
        tournament_size (int):             How many compete in each tournament.

    Returns:
        Chromosome: The winning parent.
    """
    competitors = random.sample(range(len(population)), tournament_size)
    best = max(competitors, key=lambda i: fitnesses[i])
    return population[best]


def crossover(parent_a, parent_b):
    """
    Single-point crossover: splits both parents at a random point,
    combines the first half of A with the second half of B.
    Deduplicates rules to avoid repeats.

    Args:
        parent_a (Chromosome): First parent.
        parent_b (Chromosome): Second parent.

    Returns:
        Chromosome: A new child chromosome.
    """
    split = random.randint(1, max(1, len(parent_a.rules) - 1))
    # Take first `split` rules from A, fill the rest from B (skip duplicates)
    child_rules = parent_a.rules[:split]
    seen = set(id(r) for r in child_rules)
    for rule in parent_b.rules:
        if id(rule) not in seen:
            child_rules.append(rule)
            seen.add(id(rule))
    return Chromosome(rules=child_rules)


def mutate(chromosome, mutation_rate=0.2):
    """
    Randomly mutates a chromosome in one of three ways:
        - Swap: swap two rules in the ordering
        - Delete: remove a random rule (if more than 3 remain)
        - Add: insert a random rule from RULE_POOL that isn't already present

    Args:
        chromosome    (Chromosome): The chromosome to mutate (mutated in place).
        mutation_rate (float):      Probability that mutation occurs at all.

    Returns:
        Chromosome: The (possibly mutated) chromosome.
    """
    if random.random() > mutation_rate:
        return chromosome  # No mutation this time

    mutation_type = random.choice(["swap", "delete", "add"])

    if mutation_type == "swap" and len(chromosome.rules) >= 2:
        i, j = random.sample(range(len(chromosome.rules)), 2)
        chromosome.rules[i], chromosome.rules[j] = chromosome.rules[j], chromosome.rules[i]

    elif mutation_type == "delete" and len(chromosome.rules) > 3:
        idx = random.randint(0, len(chromosome.rules) - 1)
        chromosome.rules.pop(idx)

    elif mutation_type == "add":
        existing_ids = set(id(r) for r in chromosome.rules)
        new_candidates = [r for r in RULE_POOL if id(r) not in existing_ids]
        if new_candidates:
            chromosome.rules.append(random.choice(new_candidates))

    return chromosome