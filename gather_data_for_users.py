import subprocess
import time
import csv
import os
import sys

EXPERIMENT_TIME = time.time_ns()
START_TIME = 10000000
OUTPUT_PATH = 'output/'

def load_sites():
    sites = []
    with open('data/top50sites.csv') as sitesfile:
        sitereader = csv.reader(sitesfile)
        for row in sitereader:
            site = row[0]
            sites.append(site)
    return sites

def setup_output_folder():
    outputExists = os.path.exists(OUTPUT_PATH)

    if not outputExists:
        os.makedirs(OUTPUT_PATH)
        print("Created output directory")

def run_traceroute(site):
    if sys.platform == "win32":
        proc = subprocess.check_output("tracert {}".format(site), shell=True, encoding='UTF-8')
    elif sys.platform == "linux" or sys.platform == "linux2":
        proc = subprocess.check_output("traceroute -A -q 1 {}".format(site), shell=True, encoding='UTF-8')
    elif sys.platform == "darwin":
        proc = subprocess.check_output("traceroute -a -q 1 {}".format(site), shell=True, encoding='UTF-8')
    else:
        print("Unknown Operating System.")
        assert False
    return proc

if __name__ == "__main__":
    setup_output_folder()
    sites = load_sites()
    if(time.time() >= START_TIME):
        while (True):
            for site in sites:
                timestamp = time.time()
                try:
                    proc = run_traceroute(site)
                except:
                    continue
                with open('output/results-' +str(EXPERIMENT_TIME)+'.csv', 'a') as outputfile:
                    outputwriter = csv.writer(outputfile)
                    outputwriter.writerow([timestamp, proc])
            time.sleep(60*30)

