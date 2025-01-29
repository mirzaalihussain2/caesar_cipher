import statistics
from .utils import get_observed_frequencies, get_ngram_weight, DECIMAL_PLACES, CONFIDENCE_THRESHOLDS
from .types import Solution, SolutionWithTotal, StatName, ConfidenceLevel, ConfidenceThreshold

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

def determine_confidence(confidence_stats: ConfidenceThreshold) -> ConfidenceLevel:
    separation_score, relative_rank, z_statistic = confidence_stats.separation_score, confidence_stats.relative_rank, confidence_stats.z_statistic
    low_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.LOW]
    high_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.HIGH]

    if (
        separation_score < low_threshold.separation_score or 
        z_statistic < low_threshold.z_statistic or
        relative_rank > low_threshold.relative_rank
    ):
        return ConfidenceLevel.LOW
    
    if (
        separation_score > high_threshold.separation_score and 
        z_statistic > high_threshold.z_statistic and
        relative_rank < high_threshold.relative_rank
    ):
        return ConfidenceLevel.HIGH
    
    return ConfidenceLevel.MEDIUM

def get_confidence(chi_squared_totals: list[float]) -> ConfidenceThreshold:
    sorted_values = sorted(chi_squared_totals)
    lowest_value = sorted_values[0] # lowest value is best match, in context of chi-squared stats
    second_lowest_value = sorted_values[1]

    mean = round(statistics.mean(sorted_values[1:]))
    standard_deviation = round(statistics.stdev(sorted_values[1:]))

    relative_rank = lowest_value / mean
    z_statistic = (mean - lowest_value) / standard_deviation

    # separation_score is a Z-statistic adapted for frequency analysis whwere chi-squared stats are NOT expected to be normally distributed,
    # separation_score compares lowest value against second lowest value rather than mean
    separation_score = (second_lowest_value - lowest_value) / standard_deviation

    return ConfidenceThreshold(
        z_statistic,
        separation_score,
        relative_rank
    )

