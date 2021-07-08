import pandas as pd
import math
from scipy.stats import t


def confidence_interval_batch(data, column_names, group_by_col, confidence=0.95):
    sample_data = pd.DataFrame(data.groupby(group_by_col)[column_names].agg(["count", "mean", "std"]))
    row_names = (x + "_" + y for x, y in sample_data.index)
    sample_data = sample_data.fillna(0)
    sample_size = list(sample_data["count"])
    standard_deviation = list(sample_data["std"])
    mean = [round(mean,2) for mean in sample_data["mean"]]
    degrees_freedom = [count - 1 for count in sample_size]
    outlier_tails = (1.0 - confidence) / 2.0
    confidence_collection = [outlier_tails for _ in sample_size]
    t_distribution_number = [-1 * t.ppf(tails, df) for tails, df in zip(confidence_collection, degrees_freedom)]

    step_1 = [std / math.sqrt(count) for std, count in zip(standard_deviation, sample_size)]
    step_2 = [step * t for step, t in zip(step_1, t_distribution_number)]

    low_end = pd.Series([round(mean_num - step_num, 2) for mean_num, step_num in zip(mean, step_2)]).fillna(0)
    high_end = pd.Series([round(mean_num + step_num, 2) for mean_num, step_num in zip(mean, step_2)]).fillna(0)
    output_data = pd.DataFrame({"grouping": row_names, "mean": mean, "low end": low_end,
                                "high_end": high_end}).sort_values(by=['mean'], ascending=False)

    return output_data
