#!/usr/bin/python3

import csv
import sys
import requests
import zipfile
import os


def download_and_extract_zip(url, destination_folder="."):
    """
    Downloads and extracts a zip file from a given URL into a specified directory.

    Args:
    url (str): URL of the zip file to download.
    destination_folder (str): Directory where the zip file will be extracted.
    """
    zip_filename = url.split("/")[-1]
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Ensure the request was successful
            with open(zip_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        with zipfile.ZipFile(zip_filename, "r") as zip_file:
            zip_file.extractall(destination_folder)
        os.remove(zip_filename)  # Clean up the downloaded zip file
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file.")


def read_csv_as_dictionary(csv_file_path):
    """
    Reads a CSV file and returns a dictionary mapping the second column to the first.

    Args:
    csv_file_path (str): Path to the CSV file.

    Returns:
    dict: A dictionary with keys from the second column and values from the first.
    """
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            return {rows[1]: rows[0] for rows in csv_reader}
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} does not exist.")
        return {}


def display_domain_rankings(domain, tranco_dict, umbrella_dict):
    """
    Prints the rankings of a domain from the provided dictionaries.

    Args:
    domain (str): The domain to search for in the dictionaries.
    tranco_dict (dict): Tranco ranking dictionary.
    umbrella_dict (dict): Umbrella ranking dictionary.
    """
    tranco_rank = tranco_dict.get(domain, "No ranking")
    umbrella_rank = umbrella_dict.get(domain, "No ranking")
    print(f"Rank of '{domain}' in Tranco database: {tranco_rank}")
    print(f"Rank of '{domain}' in Umbrella database: {umbrella_rank}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]

    # URLs for the ranking data
    tranco_url = "https://tranco-list.eu/top-1m.csv.zip"
    umbrella_url = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"

    download_and_extract_zip(tranco_url, "tranco")
    download_and_extract_zip(umbrella_url, "umbrella")

    tranco_dict = read_csv_as_dictionary("tranco/top-1m.csv")
    umbrella_dict = read_csv_as_dictionary("umbrella/top-1m.csv")

    display_domain_rankings(domain, tranco_dict, umbrella_dict)


if __name__ == "__main__":
    main()
