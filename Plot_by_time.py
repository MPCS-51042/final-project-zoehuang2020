import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd
from Confidence_Interval import confidence_interval_batch


def plot_by_time(data, column_name, time_variable, group_by, course_code):
    fig, axs = plt.subplots(2, figsize=(10, 8))
    fig.subplots_adjust(left=0.1, bottom=0.1)
    sub_data = data[data["Course Code"] == course_code]
    test_data_summary = pd.DataFrame(sub_data.groupby(time_variable)[column_name].mean())
    # Add a trending plot for the selected course
    axs[0].plot(test_data_summary.index, test_data_summary[column_name], label="Average", linestyle='dashed',
                marker='o')
    section_code = sorted(set(sub_data[group_by]))
    for i in section_code:
        sub_data_group = sub_data[sub_data[group_by] == i]
        axs[0].plot(sub_data_group[time_variable], sub_data_group[column_name], linewidth=2, label=i, marker='o')
    plt.sca(axs[0])
    plt.xticks(sorted(set(sub_data[time_variable])), rotation=30, horizontalalignment='right', size='small')
    # show legend
    plt.title(f"Trending plot for Course Code: {course_code}")
    plt.ylabel(column_name)
    plt.legend()
    plt.grid()

    # Add a table at the bottom of the axes
    test_data = data[data["Course Code"] == course_code]
    test_data_stats = confidence_interval_batch(test_data, "Phase 1 Price", ["Course Code", "Section Code"])
    cell_text = []
    for row in range(len(test_data_stats)):
        cell_text.append(list(test_data_stats.loc[row][1:]))
    axs[1].table(cellText=cell_text,
                 rowLabels=test_data_stats["grouping"],
                 colLabels=test_data_stats.columns.values[1:],
                 loc='center')
    axs[1].axis('off')

    plt.suptitle(f"Bidding Points Analysis for Course Code: {course_code}", fontsize=20)
    plt.show()
    return plt
