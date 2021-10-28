import subprocess
import concurrent.futures
import time
import trparse

EXPERIMENT_TIME = 60
MAX_WORKERS = 3

sample_sites = [
    "google.com",
]


def run_traceroute(sites):
    # run traceroute
    results_dict = {}
    for site in sites:
        proc = subprocess.check_output("traceroute {}".format(site), shell=True, encoding='UTF-8')
        out = proc
        traceroute = trparse.loads(out)
        results_dict[site] = traceroute
        #print(traceroute)
    # output your traceroute
    return results_dict

if __name__ == "__main__":
    data = dict()
    for i in range(10):
        experiment_time = time.time()
        sample = run_traceroute(sample_sites)
        data[experiment_time] = sample
        time.sleep(1)
    print(data)
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
