from app.common.utils import CONFIDENCE_THRESHOLDS
from app.common.types import SolutionWithTotal, ConfidenceLevel, ConfidenceThreshold
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

    # Z-statistic measures the difference between the best match (aka lowest value) and the mean
    # Commonly used in statistics
    z_statistic = (mean - lowest_value) / std_dev
    
    # Separation score is similar to Z-statistic, but it's adapted to frequency analysis,
    # where the chi-squared values for incorrect decryption keys will not be normally distributed
    # and one chi-squared value should stand very distinct from the rest.
    # Separation score measures the difference between the best match and the second best match.
    separation_score = (second_lowest_value - lowest_value) / std_dev
    
    # Relative rank ratio normalises the best match against the mean.
    # A much lower chi-squared value than the mean suggests a standout match.
    # Simpler to interpret than other two statistical measures. Inspired by signal-to-noise ratio in statistics.
    relative_rank = lowest_value / mean

    return ConfidenceThreshold(
        z_statistic=z_statistic,
        separation_score=separation_score,
        relative_rank=relative_rank
    )

def get_confidence_level(stats: ConfidenceThreshold) -> ConfidenceLevel:
    low_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.LOW]
    high_threshold = CONFIDENCE_THRESHOLDS[ConfidenceLevel.HIGH]

    # Confidence Thresholds based on best practice thresholds (e.g. Z-statistic is a common statistical measure).
    # We computed chi-squared values on test ciphertexts and examined the confidence stats to calibrate these thresholds.

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
