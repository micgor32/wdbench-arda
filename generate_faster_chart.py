import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


def faster(first_frame: pd.DataFrame, second_frame: pd.DataFrame):
    results = 0
    rezultz = 0
    first = 0
    second = 0
    num_first_rows = len(first_frame)
    num_second_rows = len(second_frame)
    # Traverse the csv results
    while first < num_first_rows and second < num_second_rows:
        # Compare first_frame execution time in ms with second_frame execution time in ms
        if first_frame.iloc[first, 3] < second_frame.iloc[second, 3]:
            results += 1
        else:
            rezultz += 1
        # Increase index counters for further traversal
        first = first + 1
        second = second + 1
    # Pack the collected results into a single return list, unpack it in faster_bar function.
    return [results, rezultz]


def faster_multiple_dataframes(*frames):
    if len(frames) > 10:
        raise ValueError("Too many dataframes. The maximum allowed is 10.")
    if len(frames) % 2 != 0:
        raise ValueError("The number of dataframes should be even.")

    blazegraph_results_list = []
    neo4j_results_list = []

    for i in range(0, len(frames), 2):
        results, rezultz = faster(frames[i], frames[i + 1])
        blazegraph_results_list.append(results)
        neo4j_results_list.append(rezultz)

    return [blazegraph_results_list, neo4j_results_list]


def faster_bar(results, labels, save_to_file):
    x = np.arange(5)
    blaze_results = results[0]
    neo4j_results = results[1]

    y1_flat = blaze_results
    y2_flat = neo4j_results

    width = 0.2

    plt.bar(x - 0.2, y1_flat, width, color='cyan')
    plt.bar(x, y2_flat, width, color='orange')

    plt.xticks(x, ['Single', 'Multiple', 'Opts', 'Paths', 'C2rpqs'])
    plt.xlabel("Query types")
    plt.ylabel("Number of queries")
    plt.title('Number of faster queries per each database for each query type')
    plt.legend([labels[0], labels[1]])

    if save_to_file.lower() == 'y':
        output_filename = "faster_queries_chart.png"
        plt.savefig(output_filename)
        print(f"Chart saved to {output_filename}")
    elif save_to_file.lower() == 'n':
        plt.show()
    else:
        print("Invalid input, must be either 'y' or 'n'")


def generate_faster_chart(first_db_name: str, second_db_name: str, save_to_file: str, *filenames):
    labels = [first_db_name, second_db_name]
    frames = [pd.read_csv(filename) for filename in filenames]

    results = faster_multiple_dataframes(*frames)
    faster_bar(results, labels, save_to_file)


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print(
            "Usage: python script.py <first_db_name> <second_db_name> <save_to_file_flag> <filename1> <filename2> ...")
        sys.exit(1)

    generate_faster_chart(sys.argv[1], sys.argv[2], sys.argv[3], *sys.argv[4:])
