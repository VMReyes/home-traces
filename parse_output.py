import gather_data
import trparse
import pandas as pd

def parse_output(path):
    """Parse our data output files."""
    output_df = pd.read_csv(path, names=["time", "traceroute"])
    trparse_trees = []
    for ind, row in output_df.iterrows():
        print(row)
        trparse_tree = trparse.loads(row["traceroute"])
        trparse_trees.append(trparse_tree)

    return gather_data.trparse_tree_to_record(trparse_trees)

if __name__ == "__main__":
    path = "data/results-1637199367-linux.csv" # Change on your machine
    df = parse_output(path)
    print(df)