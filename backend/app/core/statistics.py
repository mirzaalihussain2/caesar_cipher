import statistics
from .utils import get_observed_frequencies, get_ngram_weight, DECIMAL_PLACES, CONFIDENCE_THRESHOLDS
from .types import Solution, SolutionWithTotal, StatName, ConfidenceLevel
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
import random

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

def display_distribution(solutionsWithTotals: list[SolutionWithTotal]):
    matplotlib.use('Agg')  # Set backend to non-interactive
    
    # Create charts directory if it doesn't exist
    charts_dir = 'charts'
    
    # Generate random number for filename
    random_num = random.randint(100, 999)
    filename = f'chi_squared_distribution_{random_num}.png'
    filepath = os.path.join(charts_dir, filename)
    
    chi_squared_values = [s['chi_squared_total'] for s in solutionsWithTotals]
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(chi_squared_values, bins='auto', alpha=0.7, color='skyblue')
    plt.xlabel('Chi-squared Total')
    plt.ylabel('Frequency')
    plt.title('Distribution of Chi-squared Values')
    
    # Add vertical line for mean and median
    mean = np.mean(chi_squared_values)
    median = np.median(chi_squared_values)
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median:.2f}')
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save to file
    plt.savefig(filepath)
    plt.close()  # Close the figure to free memory

def determine_confidence(separation_score: float, relative_rank: float) -> ConfidenceLevel:
    if (separation_score < CONFIDENCE_THRESHOLDS[ConfidenceLevel.LOW]['separation_score'] or relative_rank > CONFIDENCE_THRESHOLDS[ConfidenceLevel.LOW]['relative_rank']):
        return ConfidenceLevel.LOW
    if (separation_score > CONFIDENCE_THRESHOLDS[ConfidenceLevel.HIGH]['separation_score'] and relative_rank < CONFIDENCE_THRESHOLDS[ConfidenceLevel.HIGH]['relative_rank']):
        return ConfidenceLevel.HIGH
    return ConfidenceLevel.MEDIUM

def get_confidence(chi_squared_totals: list[float]):
    sorted_values = sorted(chi_squared_totals)
    lowest_value = sorted_values[0] # lowest value is best match, in context of chi-squared stats
    second_lowest_value = sorted_values[1]

    mean = round(statistics.mean(sorted_values[1:]))
    standard_deviation = round(statistics.stdev(sorted_values[1:]))

    relative_rank = lowest_value / mean
    separation_score = (second_lowest_value - lowest_value) / standard_deviation

    return { 'separation_score': separation_score, 'relative_rank': relative_rank }


def calculate_confidence(solutionsWithTotals: list[SolutionWithTotal]):
    chi_squared_values = [s['chi_squared_total'] for s in solutionsWithTotals]

    sorted_values = sorted(chi_squared_values)
    lowest_value = sorted_values[0]
    second_lowest_value = sorted_values[1]

    mean = round(statistics.mean(sorted_values), DECIMAL_PLACES)
    median = round(statistics.median(sorted_values), DECIMAL_PLACES)
    standard_deviation = round(statistics.pstdev(sorted_values), DECIMAL_PLACES)

    z_stat_mean = (mean - lowest_value) / standard_deviation
    # if z_stat > 2 (i.e. 2 standard deviations better than the mean),
    # then high confidence value is right
    # z-stat can be 2 or 3

    first_second_difference = second_lowest_value - lowest_value
    first_second_ratio = second_lowest_value / lowest_value
    # if ratio is > 1.5 or > 2, then suggests high confidence

    # separation score
    sep_score = (second_lowest_value - lowest_value) / standard_deviation
    # > 2 or 3, high confidence correct key
    # < 1, low confidence key is correct

    # best / mean ratio
    best_mean_difference = mean - lowest_value
    best_median_difference = median - lowest_value
    
    # best / mean ratio
    # example threshold for ratio: 1.5
    best_mean_ratio = mean / lowest_value
    best_median_ratio = median / lowest_value

    relative_rank_mean = lowest_value / mean
    relative_rank_median = lowest_value / median
    # if < 0.5 , then high confidence

    # high confidence: separation_score > 2 AND relative_rank < 0.5
    # low confidence: separation_score < 1

    print("\nConfidence Analysis:")
    print("-" * 50)
    print(f"Basic Statistics:")
    print(f"  Lowest value: {lowest_value:.5f}")
    print(f"  Second lowest value: {second_lowest_value:.5f}")
    print(f"  Mean: {mean:.5f}")
    print(f"  Median: {median:.5f}")
    print(f"  Standard deviation: {standard_deviation:.5f}")
    
    print("\nZ-Statistics:")
    print(f"  Z-stat (mean): {z_stat_mean:.5f}")
    
    print("\nFirst-Second Analysis:")
    print(f"  Difference: {first_second_difference:.5f}")
    print(f"  Ratio: {first_second_ratio:.5f}")
    
    print("\nSeparation Analysis:")
    print(f"  Separation score: {sep_score:.5f}")
    
    print("\nBest vs Distribution:")
    print(f"  Best-Mean difference: {best_mean_difference:.5f}")
    print(f"  Best-Median difference: {best_median_difference:.5f}")
    print(f"  Best-Mean ratio: {best_mean_ratio:.5f}")
    print(f"  Best-Median ratio: {best_median_ratio:.5f}")
    
    print("\nRelative Rankings:")
    print(f"  Relative to mean: {relative_rank_mean:.5f}")
    print(f"  Relative to median: {relative_rank_median:.5f}")
