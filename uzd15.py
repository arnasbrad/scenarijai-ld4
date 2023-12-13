#!/usr/bin/python3

import csv
import sys
import requests
import ipaddress
import gzip
import os


def download_and_decompress_gzip(url, output_filename="ip-to-country.csv"):
    """
    Download a gzip file from a URL and decompress it.

    Args:
    url (str): URL of the gzip file.
    output_filename (str): Filename for the decompressed file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the download was successful
        compressed_filename = output_filename + ".gz"

        with open(compressed_filename, "wb") as file:
            file.write(response.content)

        with gzip.open(compressed_filename, "rb") as compressed_file:
            with open(output_filename, "wb") as decompressed_file:
                decompressed_file.write(compressed_file.read())

        os.remove(compressed_filename)  # Clean up compressed file
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")
        sys.exit(1)


def convert_ip_to_integer(ip_address):
    """
    Convert an IP address to its integer representation.

    Args:
    ip_address (str): IP address.

    Returns:
    int: Integer representation of the IP address.
    """
    return int(ipaddress.ip_address(ip_address))


def load_csv_as_list(filename):
    """
    Load a CSV file into a list of lists.

    Args:
    filename (str): Filename of the CSV to read.

    Returns:
    list: A list of lists with the CSV content.
    """
    with open(filename, mode="r", encoding="utf-8") as file:
        return list(csv.reader(file))


def locate_country_by_ip(ip_integer, ip_data):
    """
    Find the country corresponding to an IP address.

    Args:
    ip_integer (int): Integer representation of the IP address.
    ip_data (list): List of IP ranges with associated countries.

    Returns:
    str: Country corresponding to the IP address or 'Unknown Country' if not found.
    """
    for start_ip_str, end_ip_str, country in ip_data:
        start_ip = int(ipaddress.ip_address(start_ip_str))
        end_ip = int(ipaddress.ip_address(end_ip_str))
        if start_ip <= ip_integer <= end_ip:
            return country
    return "Unknown Country"


def main():
    if len(sys.argv) < 2:
        print("Please enter an IP address as an argument.")
        sys.exit(1)

    ip_address = sys.argv[1]
    csv_url = "https://download.db-ip.com/free/dbip-country-lite-2023-12.csv.gz"

    download_and_decompress_gzip(csv_url)
    ip_data = load_csv_as_list("ip-to-country.csv")
    ip_integer = convert_ip_to_integer(ip_address)

    country = locate_country_by_ip(ip_integer, ip_data)
    print(f"The country for IP address '{ip_address}': {country}")


if __name__ == "__main__":
    main()
