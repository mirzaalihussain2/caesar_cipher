from .utils import count_alpha_characters, unigram_frequencies, bigram_frequencies, get_observed_frequencies
from .encryption import encrypt_text
from .types import Solution

def hack_cipher(ciphertext: str) -> list[Solution]:
    text_length = count_alpha_characters(ciphertext)
    solutions = generate_all_solutions(ciphertext)

    solutions = calculate_solution_statistics(
        solutions=solutions,
        ngram_size=1,
        ngram_expected_frequencies=unigram_frequencies(),
        stat_name='unigrams'
    )

    if text_length > 50:
        solutions = calculate_solution_statistics(
            solutions=solutions,
            ngram_size=2,
            ngram_expected_frequencies=bigram_frequencies(),
            stat_name='bigrams'
        )
    
    solutions.sort(key=lambda x: x['chi_squared_total'])
    return solutions

def calculate_solution_statistics(
        solutions: list[Solution],
        ngram_size: int,
        ngram_expected_frequencies: dict[str, float],
        stat_name: str
) -> list[Solution]:
    for solution in solutions:
        chi_squared_stat = calculate_chi_squared_stat(
            text=solution['text'],
            ngram_size=ngram_size,
            normalised_expected_frequencies=ngram_expected_frequencies
        )
        solution['chi_squared_stats'][stat_name] = round(chi_squared_stat, 4)

        if solution['chi_squared_total'] is None:
            solution['chi_squared_total'] = chi_squared_stat
        else:
            solution['chi_squared_total'] *= chi_squared_stat
        
        solution['chi_squared_total'] = round(solution['chi_squared_total'], 4)

    return solutions

def generate_all_solutions(ciphertext: str) -> list[Solution]:
    solutions = []

    for key in range(26):
        solution = {
            'key': key,
            'text': encrypt_text(ciphertext, key),
            'chi_squared_stats': {},
            'chi_squared_total': None
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
