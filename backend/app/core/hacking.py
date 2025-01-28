from .utils import count_alpha_characters, unigram_frequencies, bigram_frequencies, MIN_BIGRAM_TEXT_LENGTH, DECIMAL_PLACES
from .encryption import encrypt_text
from .types import Solution, SolutionWithTotal, StatName
from .statistics import run_chi_squared_test, normalise_chi_squared_stats, calculate_chi_squared_total, calculate_confidence

def hack_cipher(ciphertext: str) -> list[SolutionWithTotal]:
    """
    Hacks simple Caesar cipher using frequency analysis (in English).
    Uses chi-squared test to compare text frequencies with English language frequencies.
    Returns possible solutions sorted by likelihood (lowest chi-squared value = best match).
    """
    text_length = count_alpha_characters(ciphertext)
    solutions = generate_base_solutions(ciphertext)

    solutions = add_solution_statistics(
        solutions=solutions,
        ngram_size=1,
        ngram_expected_frequencies=unigram_frequencies(),
        stat_name=StatName.UNIGRAM
    )

    if text_length > MIN_BIGRAM_TEXT_LENGTH:
        solutions = add_solution_statistics(
            solutions=solutions,
            ngram_size=2,
            ngram_expected_frequencies=bigram_frequencies(),
            stat_name=StatName.BIGRAM
        )
    
    solutionsWithTotals = calculate_chi_squared_total(solutions, text_length)
    calculate_confidence(solutionsWithTotals)
    return sorted(solutionsWithTotals, key=lambda x: x['chi_squared_total'])

def add_solution_statistics(
        solutions: list[Solution],
        ngram_size: int,
        ngram_expected_frequencies: dict[StatName, float],
        stat_name: StatName
) -> list[Solution]:
    for solution in solutions:
        chi_squared_stat = run_chi_squared_test(
            text=solution['text'],
            ngram_size=ngram_size,
            normalised_expected_frequencies=ngram_expected_frequencies
        )
        solution['chi_squared_stats'][stat_name] = round(chi_squared_stat, DECIMAL_PLACES)
    
    normalised_solutions = normalise_chi_squared_stats(solutions, stat_name)
    return normalised_solutions

def generate_base_solutions(ciphertext: str) -> list[Solution]:
    solutions = []

    for key in range(1, 26):
        solution = {
            'key': key,
            'text': encrypt_text(ciphertext, key),
            'chi_squared_stats': {},
            'normalised_chi_squared_stats': {}
        }
        solutions.append(solution)

    return solutions
