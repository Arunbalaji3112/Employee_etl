import csv

def load_csv(file_path, records, fieldnames):

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(records)