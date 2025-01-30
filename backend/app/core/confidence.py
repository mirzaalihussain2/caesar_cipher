from .utils import CONFIDENCE_THRESHOLDS
from .types import SolutionWithTotal, ConfidenceLevel, ConfidenceThreshold
import statistics

def set_confidence(solutions: list[SolutionWithTotal]) -> ConfidenceLevel:
    chi_squared_values = [solution['chi_squared_total'] for solution in solutions]
    confidence_stats = calculate_confidence_stats(chi_squared_values)

    return get_confidence_level(confidence_stats)

def calculate_confidence_stats(chi_squared_values: list[float]) -> ConfidenceThreshold:
    sorted_values = sorted(chi_squared_values)

    # lowest value is best match, in context of chi-squared stats
    lowest_value, second_lowest_value = sorted_values[0], sorted_values[1]

    mean = statistics.mean(sorted_values[1:])
    std_dev = statistics.stdev(sorted_values[1:])

    return ConfidenceThreshold(
        z_statistic=(mean - lowest_value) / std_dev,
        separation_score=(second_lowest_value - lowest_value) / std_dev,
        relative_rank=lowest_value / mean
    )

def get_confidence_level(stats: ConfidenceThreshold) -> ConfidenceLevel:
    low_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.LOW]
    high_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.HIGH]

    if (
        stats.separation_score < low_threshold.separation_score or 
        stats.z_statistic < low_threshold.z_statistic or
        stats.relative_rank > low_threshold.relative_rank
    ):
        return ConfidenceLevel.LOW
    
    if (
        stats.separation_score > high_threshold.separation_score and 
        stats.z_statistic > high_threshold.z_statistic and
        stats.relative_rank < high_threshold.relative_rank
    ):
        return ConfidenceLevel.HIGH
    
    return ConfidenceLevel.MEDIUM
