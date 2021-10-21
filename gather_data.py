import subprocess
import tracerouteparser.tracerouteparser as traceparser

if __name__ == "__main__":
    # run traceroute
    parser = traceparser.TracerouteParser()
    proc = subprocess.check_output("traceroute google.com", shell=True, encoding='UTF-8')
    out = proc
    parser.parse_data(out)
    print(parser)
