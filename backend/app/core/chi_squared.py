from .utils import get_observed_frequencies, get_ngram_weight, DECIMAL_PLACES
from .types import Solution, StatName, SolutionWithTotal

def run_chi_squared_test(
    text: str,
    ngram_size: int,
    normalised_expected_frequencies: dict[str, float]
) -> float:
    """ Run chi-squared test comparing text frequencies against expected frequencies """
    observed = get_observed_frequencies(text, ngram_size)
    text_length = sum(observed.values())
    expected = {
        ngram: freq * text_length
        for ngram, freq in normalised_expected_frequencies.items()
    }

    return calculate_chi_squared(observed, expected)


def calculate_chi_squared(
    observed: dict[str, int],
    expected: dict[str, float]
) -> float:
    chi_squared_stat = 0

    for ngram, expected_freq in expected.items():
        observed_freq = observed.get(ngram, 0)
        chi_squared_stat += ((observed_freq - expected_freq) ** 2) / expected_freq if expected_freq != 0 else 0

    return chi_squared_stat


def normalise_chi_squared_stats(
        solutions: list[Solution],
        stat_name: StatName
) -> list[Solution]:
    if not all(stat_name in solution['chi_squared_stats'] for solution in solutions):
        raise ValueError(f"All solutions must have {StatName} chi_squared stats before normalising values")
    
    max_stat = max(solution['chi_squared_stats'][stat_name] for solution in solutions)

    for solution in solutions:
        solution['normalised_chi_squared_stats'][stat_name] = round(
            solution['chi_squared_stats'][stat_name] / max_stat,
            DECIMAL_PLACES
        )

    return solutions


def calculate_chi_squared_total(
    solutions: list[Solution],
    text_length: int
) -> list[SolutionWithTotal]:
    # Check if unigram stats exist for all solutions
    if not all(StatName.UNIGRAM in solution['normalised_chi_squared_stats'] for solution in solutions):
        raise ValueError("All solutions must have at least one normalised chi-squared stat before computing chi-squared total")

    has_bigrams = all(StatName.BIGRAM in solution['normalised_chi_squared_stats'] for solution in solutions)

    for solution in solutions:
        if not has_bigrams:
            solution['chi_squared_total'] = solution['chi_squared_stats'][StatName.UNIGRAM]
        else:
            weighted_unigram = get_ngram_weight(StatName.UNIGRAM, text_length) * solution['normalised_chi_squared_stats'][StatName.UNIGRAM]
            weighted_bigram = get_ngram_weight(StatName.BIGRAM, text_length) * solution['normalised_chi_squared_stats'][StatName.BIGRAM]
            solution['chi_squared_total'] = round(weighted_unigram + weighted_bigram, DECIMAL_PLACES)
    
    return solutions