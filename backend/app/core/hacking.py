from .utils import count_alpha_characters, unigram_frequencies, bigram_frequencies, get_observed_frequencies, get_ngram_weight, MIN_BIGRAM_TEXT_LENGTH, DECIMAL_PLACES
from .encryption import encrypt_text
from .types import Solution, SolutionWithTotal, StatName

def hack_cipher(ciphertext: str) -> list[Solution]:
    """
    Hacks simple Caesar cipher using frequency analysis (in English).
    Uses chi-squared test to compare text frequencies with English language frequencies.
    Returns possible solutions sorted by likelihood (lowest chi-squared value = best match).
    """
    text_length = count_alpha_characters(ciphertext)
    solutions = generate_all_solutions(ciphertext)

    solutions = calculate_solution_statistics(
        solutions=solutions,
        ngram_size=1,
        ngram_expected_frequencies=unigram_frequencies(),
        stat_name=StatName.UNIGRAM
    )

    if text_length > MIN_BIGRAM_TEXT_LENGTH:
        solutions = calculate_solution_statistics(
            solutions=solutions,
            ngram_size=2,
            ngram_expected_frequencies=bigram_frequencies(),
            stat_name=StatName.BIGRAM
        )
    
    solutionsWithTotals = calculate_chi_squared_total(solutions, text_length)
    return solutionsWithTotals

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
    
    return sorted(solutions, key=lambda x: x['chi_squared_total'])

def normalise_chi_stats(
        solutions: list[Solution],
        stat_name: StatName
) -> list[Solution]:
    if not all(stat_name in solution['chi_squared_stats'] for solution in solutions):
        raise ValueError(f"All solutions must have {StatName} chi_squared stats before normalising values")
    else:
        max_stat = max(solution['chi_squared_stats'][stat_name] for solution in solutions)
        for solution in solutions:
            solution['normalised_chi_squared_stats'][stat_name] = round(solution['chi_squared_stats'][stat_name] / max_stat, DECIMAL_PLACES)
        return solutions

def calculate_solution_statistics(
        solutions: list[Solution],
        ngram_size: int,
        ngram_expected_frequencies: dict[StatName, float],
        stat_name: StatName
) -> list[Solution]:
    for solution in solutions:
        chi_squared_stat = calculate_chi_squared_stat(
            text=solution['text'],
            ngram_size=ngram_size,
            normalised_expected_frequencies=ngram_expected_frequencies
        )
        solution['chi_squared_stats'][stat_name] = round(chi_squared_stat, DECIMAL_PLACES)
    
    normalised_solutions = normalise_chi_stats(
        solutions=solutions,
        stat_name=stat_name
    )

    return normalised_solutions

def generate_all_solutions(ciphertext: str) -> list[Solution]:
    solutions = []

    for key in range(1, 26):
        solution = {
            'key': key,
            'text': encrypt_text(ciphertext, key),
            'chi_squared_stats': {},
            'normalised_chi_squared_stats': {},
            'chi_squared_total': None,
        }
        solutions.append(solution)

    return solutions

def calculate_chi_squared_stat(
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
