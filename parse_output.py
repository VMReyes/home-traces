import trparse
import pandas as pd

def trparse_tree_to_record(trparse_trees, max_hops=30, num_probes=1):
    """Converts parsed traceroute tree into a pandas DataFrame record for our datatable."""
    columns = ["dest name", "dest ip", "num hops"]
    probe_atts = ["name", "ip", "asn", "rtt", "annotation"]
    for h in range(1, max_hops+1):
        for p in range(1, num_probes+1):
            header = f"hop {h} probe {p} "
            for att in probe_atts:
                columns.append(header+att)

    rows = []
    for trparse_tree in trparse_trees:
        row = []
        dest_name = trparse_tree.dest_name
        dest_ip = trparse_tree.dest_ip
        hops = len(trparse_tree.hops)
        row = [dest_name, dest_ip, hops]

        for hop in trparse_tree.hops:
            for probe in hop.probes:
                row.extend([probe.name, probe.ip, probe.asn, probe.rtt, probe.annotation])
        
        while len(row) < len(columns):
            row.append(None)
        rows.append(row)

    return pd.DataFrame(rows, columns=columns)

def parse_output(path):
    """Parse our data output files."""
    output_df = pd.read_csv(path, names=["time", "traceroute"])
    trparse_trees = []
    for ind, row in output_df.iterrows():
        # print(row)
        trparse_tree = trparse.loads(row["traceroute"])
        trparse_trees.append(trparse_tree)
    
    traceroute_df = trparse_tree_to_record(trparse_trees)
    traceroute_df['time'] = output_df['time']
    return traceroute_df

if __name__ == "__main__":
    path = "data/results-1637199367-linux.csv" # Change on your machine
    df = parse_output(path)
    print(df)