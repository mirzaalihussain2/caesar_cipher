from .utils import count_alpha_characters, unigram_frequencies, bigram_frequencies, MIN_BIGRAM_TEXT_LENGTH, ConfidenceLevel, ANALYSIS_LENGTHS, DECIMAL_PLACES
from .types import Solution, StatName, HackResult, SolutionWithTotal
from .chi_squared import calculate_chi_squared_total, run_chi_squared_test, normalise_chi_squared_stats
from .confidence import set_confidence
from .encryption import encrypt_text

def crack_cipher(ciphertext: str) -> HackResult:
    """
    Main function to run frequency analysis on ciphertext samples of increasingly length
    until confident our solution is correct or full text analysed
    """
    full_text_length = len(ciphertext)
    analysis_lengths = ANALYSIS_LENGTHS.copy()
    result = try_crack(ciphertext, full_text_length, analysis_lengths)

    while retry_analysis(result.confidence_level, result.analysis_length, full_text_length):
        analysis_lengths.pop(0)
        result = try_crack(ciphertext, full_text_length, analysis_lengths)
    
    return result

def try_crack(ciphertext: str, full_text_length: int, analysis_lengths: list[int]) -> HackResult:
    analysis_length = get_analysis_length(full_text_length, analysis_lengths)
    solutions = run_frequency_analysis(ciphertext, analysis_length)
    confidence_level = set_confidence(solutions)

    return HackResult(
        solutions=solutions,
        confidence_level=confidence_level,
        analysis_length=analysis_length
    )

def run_frequency_analysis(ciphertext: str, analysis_length: int) -> list[SolutionWithTotal]:
    """ Runs frequency analysis on ciphertext and returns sorted solutions"""
    solutions = generate_base_solutions(ciphertext, analysis_length)
    alpha_length = count_alpha_characters(ciphertext[:analysis_length])

    # Add unigram statistics
    solutions = add_solution_statistics(
        solutions=solutions,
        ngram_size=1,
        ngram_expected_frequencies=unigram_frequencies(),
        stat_name=StatName.UNIGRAM
    )

    # Add bigram statistics if text is long enough
    if alpha_length > MIN_BIGRAM_TEXT_LENGTH:
        solutions = add_solution_statistics(
            solutions=solutions,
            ngram_size=2,
            ngram_expected_frequencies=bigram_frequencies(),
            stat_name=StatName.BIGRAM
        )
    
    solutions = calculate_chi_squared_total(solutions, alpha_length)
    return sorted(solutions, key=lambda x: x['chi_squared_total'])

def retry_analysis(
    confidence_level: ConfidenceLevel,
    current_analysis_length: int,
    full_text_length: int
) -> bool:
    """ Determines if frequency analysis should be retried with a longer text sample """
    return (
        confidence_level in (ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM) and
        current_analysis_length < full_text_length
    )

def get_analysis_length(full_text_length: int, analysis_lengths: list[int]) -> int:
    if not analysis_lengths:
        return full_text_length
    else:
        next_length = sorted(analysis_lengths)[0]
        return min(full_text_length, next_length)

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