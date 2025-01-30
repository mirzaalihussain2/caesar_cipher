from .utils import DECIMAL_PLACES
from .encryption import encrypt_text
from .types import Solution, StatName
from .chi_squared import run_chi_squared_test, normalise_chi_squared_stats

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

def generate_base_solutions(ciphertext: str, analysis_length: int) -> list[Solution]:
    solutions = []

    for key in range(1, 26):
        solution = {
            'key': key,
            'full_text': encrypt_text(ciphertext, key),
            'text': encrypt_text(ciphertext[:analysis_length], key),
            'chi_squared_stats': {},
            'normalised_chi_squared_stats': {}
        }
        solutions.append(solution)

    return solutions
