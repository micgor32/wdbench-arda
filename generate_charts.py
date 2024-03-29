# Script to generate the charts from benchmark file.
#
# Copyright (c) 2024 Michal Gorlas, Nedas Adamavicius
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Usage: python3 generate_charts.py <queries_type> <first_db_name> <second_db_name> <chart_type> <path_to_csv> <path_to_csv> 
# Available chart types are:
# - Average
# - Faster
# - Timeout
#
# Save to file can be either Y or N (case insensitive)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def generate_chart(queries_type: str, first_db_name: str, second_db_name: str, chart_type: str, filename1: str,
                   filename2: str, save_to_file: str):
    # Get frames from csv
    first_frame = pd.read_csv(filename1)
    second_frame = pd.read_csv(filename2)

    labels = []
    labels.append(first_db_name)
    labels.append(second_db_name)

    if chart_type.lower() == "average":
        results = average(first_frame, second_frame)
        avg_bar(results, labels, queries_type, save_to_file)

    elif chart_type.lower() == "faster":
        results = faster(first_frame, second_frame)
        faster_bar(results, labels, queries_type, save_to_file)

    elif chart_type.lower() == "timeout":
        results_tout = timeout(first_frame, second_frame)
        results_success = success(first_frame, second_frame)
        tout_bar(results_tout, results_success, labels, queries_type, save_to_file)
    else:
        print("Invalid chart type " + chart_type)
        sys.exit(1)


def average(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []
    avg_first = first_frame['time'].mean()
    results.append(avg_first)
    avg_second = second_frame['time'].mean()
    results.append(avg_second)

    return results


def avg_bar(results, labels, queries_type, save_to_file):
    fig, ax = plt.subplots()
    bars = ax.bar(labels, results, color=['blue', 'pink'])

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    plt.ylabel('Time (ms)')

    if save_to_file.lower() == 'y':
        output_filename = f"{queries_type}_queries_chart.png"
        plt.savefig(output_filename)
        print(f"Chart saved to {output_filename}")
    elif save_to_file.lower() == 'n':
        plt.show()
    else:
        print("Invalid input, must be either 'y' or 'n'")


def faster(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []
    rezultz = []
    first = 0
    second = 0
    num_first_rows = len(first_frame)
    num_second_rows = len(second_frame)
    # Traverse the csv results
    while first < num_first_rows and second < num_second_rows:
        # Compare first_frame execution time in ms with second_frame execution time in ms
        if first_frame.iloc[first, 3] < second_frame.iloc[second, 3]:
            results.append(first_frame.iloc[first, :])
        else:
            rezultz.append(second_frame.iloc[second, :])
        # Increase index counters for further traversal
        first = first + 1
        second = second + 1
    # Pack the collected results into a single return list, unpack it in faster_bar function.
    return [results, rezultz]


def faster_bar(results, labels, query_type, save_to_file):
    bar_width = 0.35
    index = range(len(labels))

    sizes = [len(results[0]), len(results[1])]

    fig, ax = plt.subplots()

    bars = ax.bar(index, sizes, bar_width)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    ax.set_xticks([i for i in index])
    ax.set_xticklabels(labels)

    plt.ylabel('Number of queries')

    if save_to_file.lower() == 'y':
        output_filename = f"{query_type}_queries_chart.png"
        plt.savefig(output_filename)
        print(f"Chart saved to {output_filename}")
    elif save_to_file.lower() == 'n':
        plt.show()
    else:
        print("Invalid input, must be either 'y' or 'n'")


def timeout(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []

    count_first = countTimeouts(first_frame)
    count_second = countTimeouts(second_frame)
    results.append(count_first)
    results.append(count_second)

    return results


def success(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []

    count_first = countSuccess(first_frame)
    count_second = countSuccess(second_frame)
    results.append(count_first)
    results.append(count_second)

    return results


def tout_bar(results_tout, results_success, labels, queries_type, save_to_file):
    n_groups = len(labels)
    index = np.arange(n_groups)
    bar_width = 0.35

    fig, ax = plt.subplots()

    tout_bars = ax.bar(index - bar_width / 2, results_tout, bar_width,
                       color='firebrick', label='Timeout')

    success_bars = ax.bar(index + bar_width / 2, results_success, bar_width,
                          color='limegreen', label='OK')

    for bar in tout_bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 1),
                    textcoords="offset points",
                    ha='center', va='bottom')

    for bar in success_bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 1),
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_ylabel('Number of Queries')
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.legend(['Timeout', 'OK'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    if save_to_file.lower() == 'y':
        output_filename = f"{queries_type}_queries_chart.png"
        plt.savefig(output_filename)
        print(f"Chart saved to {output_filename}")
    elif save_to_file.lower() == 'n':
        plt.show()
    else:
        print("Invalid input, must be either 'y' or 'n'")

# Helper function
def countTimeouts(frame):
    return sum(count for status, count in frame['status'].value_counts().items() if status != 'OK')


# Helper function for counting the successful queries
def countSuccess(frame):
    return sum(count for status, count in frame['status'].value_counts().items() if status == 'OK')


if __name__ == '__main__':
    if len(sys.argv) < 8:
        print(
            "Usage: python3 generate_charts.py <queries_type> <first_db_name> <second_db_name> <chart_type> <path_to_csv> <path_to_csv> <save_to_file>")
        print(
            """Available chart types are:
 - Average
 - Faster
 - Timeout

 Save to file can be either Y or N (case insensitive)
""")
    else:
        generate_chart(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
