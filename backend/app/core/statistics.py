from .utils import get_observed_frequencies, get_ngram_weight, DECIMAL_PLACES
from .types import Solution, SolutionWithTotal, StatName

def run_chi_squared_test(
    text: str,
    ngram_size: int,
    normalised_expected_frequencies: dict[str, float]
) -> float:
    observed_frequencies = get_observed_frequencies(text, ngram_size)
    text_length = sum(observed_frequencies.values())
    chi_squared_stat = 0
    expected_frequencies = {k: v * text_length for k, v in normalised_expected_frequencies.items()}

    for ngram, expected_freq in expected_frequencies.items():
        observed_freq = observed_frequencies.get(ngram, 0)
        chi_squared_stat += ((observed_freq - expected_freq) ** 2) / expected_freq if expected_freq != 0 else 0
    
    return chi_squared_stat

def normalise_chi_squared_stats(
        solutions: list[Solution],
        stat_name: StatName
) -> list[Solution]:
    if not all(stat_name in solution['chi_squared_stats'] for solution in solutions):
        raise ValueError(f"All solutions must have {StatName} chi_squared stats before normalising values")
    else:
        print(stat_name)
        max_stat = max(solution['chi_squared_stats'][stat_name] for solution in solutions)
        for solution in solutions:
            solution['normalised_chi_squared_stats'][stat_name] = round(solution['chi_squared_stats'][stat_name] / max_stat, DECIMAL_PLACES)
        return solutions

def calculate_chi_squared_total(
        solutions: list[Solution],
        text_length: int
) -> list[SolutionWithTotal]:
    # Check if unigram stats exist for all solutions
    if not all(StatName.UNIGRAM in solution['normalised_chi_squared_stats'] for solution in solutions):
        raise ValueError("All solutions must have at least one normalised chi-squared stat before computing chi-squared total")
    else:
        if not all(StatName.BIGRAM in solution['normalised_chi_squared_stats'] for solution in solutions):
            # Update with unigram stats only
            for solution in solutions:
                solution['chi_squared_total'] = solution['chi_squared_stats'][StatName.UNIGRAM]
        else:
            # Update with weighted combination of unigram and bigram stats
            for solution in solutions:
                weighted_unigram_stat = get_ngram_weight(StatName.UNIGRAM, text_length) * solution['normalised_chi_squared_stats'][StatName.UNIGRAM]
                weighted_bigram_stat = get_ngram_weight(StatName.BIGRAM, text_length) * solution['normalised_chi_squared_stats'][StatName.BIGRAM]
                solution['chi_squared_total'] = round(weighted_unigram_stat + weighted_bigram_stat, DECIMAL_PLACES)
    
    return solutions