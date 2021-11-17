import subprocess
import concurrent.futures
import time
import trparse
import csv
import pandas as pd

EXPERIMENT_TIME = 60
MAX_WORKERS = 3

sample_sites = [
    "google.com",
]

def run_single_traceroute_and_return_tree(site):
    proc = subprocess.check_output("traceroute -A -q 1 {}".format(site), shell=True, encoding='UTF-8')
    out = proc
    traceroute = trparse.loads(out)
    return traceroute

def run_traceroute(sites):
    # run traceroute
    results_dict = {}
    for site in sites:
        proc = subprocess.check_output("traceroute -a -q 1 {}".format(site), shell=True, encoding='UTF-8')
        out = proc
        traceroute = trparse.loads(out)
        results_dict[site] = traceroute
        print(traceroute)
    # output your traceroute
    return results_dict

def was_traceroute_successful(traceroute):
    """Returns true if we found the resolved IP in the traceroute (success)."""
    for hop in traceroute.hops:
        probe = hop.probes[0]
        if probe.ip == traceroute.dest_ip:
            return True
    return False

def find_friendly_websites():
    with open('data/top50sites.csv') as sitesfile:
        sitereader = csv.reader(sitesfile)
        for row in sitereader:
            site = row[0]
            try:
                parsed_traceroute = run_single_traceroute_and_return_tree(site)
                successful = was_traceroute_successful(parsed_traceroute)
            except Exception:
                print(f'Failed to run traceroute on {site}. Retrying in 10 seconds...')
                time.sleep(10)
                try:
                    parsed_traceroute = run_single_traceroute_and_return_tree(site)
                except Exception:
                    successful = False

            with open('output/top50sites_friendly_result.csv', 'a') as friendlyfile:
                friendlywriter = csv.writer(friendlyfile)
                friendlywriter.writerow([site, successful])

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



if __name__ == "__main__":
    pass
    #data = dict()
    #for i in range(10):
    #    experiment_time = time.time()
    #    sample = run_traceroute(sample_sites)
    #    data[experiment_time] = sample
    #    time.sleep(1)
    #print(data)
    #while True:
    #    experiment_time = time.time()
    #    results = []
    #    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    #        num_sites, leftover = divmod(len(sample_sites), MAX_WORKERS)
    #        sites = [sample_sites[i*num_sites+min(i, leftover):(i+1)*num_sites+min(i+1, leftover)] for i in range(MAX_WORKERS)]

    #        futures = {executor.submit(run_traceroute, sub_sites): sub_sites for sub_sites in sites}
    #        for future in concurrent.futures.as_completed(futures):
    #            tested = futures[future]
    #            future.result()
    #            results.append(future)
    #    print(results)
    #    results_dict[experiment_time] = results
    #    time.sleep(30)
