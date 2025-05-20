import xml.etree.ElementTree as ET
import csv
import argparse

def extract_staticmaps_from_interface(interface):
    staticmaps = []
    for staticmap in interface.findall("staticmap"):
        ip = staticmap.findtext("ipaddr", default="").strip()
        mac = staticmap.findtext("mac", default="").strip()
        hostname = staticmap.findtext("hostname", default="").strip()
        descr = staticmap.findtext("descr", default="").strip()
        if ip and mac:  # Nur gültige Einträge
            staticmaps.append({
                "ip_address": ip,
                "hw_address": mac,
                "hostname": hostname,
                "description": descr
            })
    return staticmaps

def parse_opnsense_dhcpd(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    dhcpd = root.find(".//dhcpd")

    entries = []
    if dhcpd is not None:
        for interface in dhcpd:
            entries.extend(extract_staticmaps_from_interface(interface))
    return entries

def write_csv(entries, csv_path):
    with open(csv_path, mode='w', newline='') as csvfile:
        fieldnames = ["ip_address", "hw_address", "hostname", "description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

def main():
    parser = argparse.ArgumentParser(description="Convert OPNsense DHCP static map XML to Kea DHCP CSV format.")
    parser.add_argument("input_xml", help="Path to the input OPNsense XML file")
    parser.add_argument("output_csv", help="Path to the output CSV file")

    args = parser.parse_args()
    entries = parse_opnsense_dhcpd(args.input_xml)
    write_csv(entries, args.output_csv)

if __name__ == "__main__":
    main()
