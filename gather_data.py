import subprocess
import concurrent.futures
import tracerouteparser.tracerouteparser as traceparser
import time

EXPERIMENT_TIME = 60
MAX_WORKERS = 10

sample_sites = [
    "wikipedia.com"
]



def run_traceroute(sites):
    # run traceroute
    parser = traceparser.TracerouteParser()

    start = time.time()
    while time.time() < start + EXPERIMENT_TIME:
        for site in sites:
            proc = subprocess.check_output("traceroute {}".format(site), shell=True, encoding='UTF-8')
            out = proc
            parser.parse_data(out)
            print(parser)
        time.sleep(10)
    return parser

if __name__ == "__main__":
    #run_traceroute(sample_sites)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        num_sites, leftover = divmod(len(sample_sites), MAX_WORKERS)
        sites = [sample_sites[i*num_sites+min(i, leftover):(i+1)*num_sites+min(i+1, leftover)] for i in range(MAX_WORKERS)]

        futures = {executor.submit(run_traceroute, sub_sites): sub_sites for sub_sites in sites}
        for future in concurrent.futures.as_completed(futures):
            tested = futures[future]
            try:
                future.result()
            except Exception as exc:
                print("something went wrong :(")
                raise exc