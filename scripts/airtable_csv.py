import requests
from environs import Env
import csv


env = Env()
env.read_env()

headers = {"Authorization": f"Bearer {env('AIRTABLE_KEY')}"}
BASE_URL = f"https://api.airtable.com/v0/{env('AIRTABLE_BASE')}"

field_names = ["Order", "Suborder", "Great Group", "Summary", "Key"]


def main():

    with open("soil_classification.csv", "w") as fd:
        writer = csv.DictWriter(fd, fieldnames=field_names)
        writer.writeheader()
        offset = None
        while True:
            resp = requests.get(
                f"{BASE_URL}/USDA%20Taxonomy%20Main",
                params=[("offset", offset)] + [("fields[]", f) for f in field_names],
                headers=headers,
            )
            obj = resp.json()
            for record in obj["records"]:
                # print(record["fields"]["Order"])
                writer.writerow(record["fields"])
            if "offset" in obj:
                offset = obj["offset"]
            else:
                break
            print(".")


if __name__ == "__main__":
    main()
