from parse_output import parse_output
import pandas as pd
from ipwhois.net import Net
from ipwhois.asn import IPASN

def gen_ip_to_asn(df):
    cols = ["target ip", "asn", "asn cidr", "asn country code", "asn date", "asn description", "asn registry"]
    rows = []
    ip_to_asn = {}
    for ind, row in df.iterrows():
        print(ind)
        for i in range(1, 31):
            ip = row[f"hop {i} probe 1 ip"]
            if not pd.isnull(ip) and ip not in ip_to_asn:
                curr_row = []
                try:
                    net = Net(ip)
                    obj = IPASN(net)
                    results = obj.lookup()
                    curr_row.extend([ip, results["asn"], results["asn_cidr"], results["asn_country_code"], results["asn_date"],
                    results["asn_description"], results["asn_registry"]])
                except:
                    pass
        if curr_row:
            rows.append(curr_row)
    return pd.DataFrame(rows, columns=cols)

if __name__ == '__main__':
    data_path = "data/home-victor-results-1637268720-incomplete.csv"
    df = parse_output(data_path)
    print(df.shape)
    ip_to_asn = gen_ip_to_asn(df.head(1))
    ip_to_asn.to_csv("data/ip-to-asn.csv", index=False)
