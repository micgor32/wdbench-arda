# Script to generate the charts from benchmark file.
#
# Copyright (c) 2023 Michal Gorlas
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

import pandas as pd
import matplotlib.pyplot as plt
import sys


def generate_chart(queries_type: str, first_db_name: str, second_db_name: str, chart_type: str, filename1: str, filename2: str):
    # Get frames from csv
    first_frame = pd.read_csv(filename1)
    second_frame = pd.read_csv(filename2)

    labels = []
    labels.append(first_db_name)
    labels.append(second_db_name)

    if chart_type.lower() == "average":
        results = average(first_frame, second_frame)
        avg_bar(results, labels, queries_type)

    # elif chart_type.lower() == "faster":
    #     results = faster(first_frame, second_frame)

    elif chart_type.lower() == "timeout":
        results = timeout(first_frame, second_frame)
        tout_bar(results, labels, queries_type)
    else:
        print("Invalid chart type")
        sys.exit(1)


def average(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []
    avg_first = first_frame['time'].mean()
    results.append(avg_first)
    avg_second = second_frame['time'].mean()
    results.append(avg_second)

    return results


def avg_bar(results, labels, queries_type):
    fig, ax = plt.subplots()
    bars = ax.bar(labels, results, color=['blue', 'pink'])
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    plt.ylabel('Time (ms)')
    plt.title('Average query time for each database with ' + queries_type + " queries")
    plt.show()


#def faster


def timeout(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = []

    count_first = countTimeouts(first_frame)
    count_second = countTimeouts(second_frame)
    results.append(count_first)
    results.append(count_second)

    return results
    

def tout_bar(results, labels, queries_type):
    fig, ax = plt.subplots()
    bars = ax.bar(labels, results, color=['blue', 'pink'])
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
    
    plt.ylabel('Number of timeouts')
    plt.title('Number of timeouts for each database with ' + queries_type + ' queries')
    plt.show()


# Helper function
def countTimeouts(frame):
    return sum(count for status, count in frame['status'].value_counts().items() if status != 'OK')


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Usage: python3 generate_charts.py <queries_type> <first_db_name> <second_db_name> <chart_type> <path_to_csv> <path_to_csv>")
    else:
        generate_chart(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
