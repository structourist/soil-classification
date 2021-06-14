import requests
from environs import Env
import json

env = Env()
env.read_env()

headers = {"Authorization": f"Bearer {env('AIRTABLE_KEY')}"}
BASE_URL = f"https://api.airtable.com/v0/{env('AIRTABLE_BASE')}"


def main():

    with open("soil.json", "w") as fd:
        tables = [("USDA%20Taxonomy%20Main", "soil_types"), ("Criteria", "soil_criteria"), ("Meta%20Criteria", "meta_criteria")]
        data = {}
        
        for table_name, table_key in tables:
                
            offset = None
            records = []
            while True:
                resp = requests.get(
                    f"{BASE_URL}/{table_name}",
                    params=[("offset", offset)],
                    headers=headers,
                )
                obj = resp.json()
                for record in obj["records"]:
                    records.append(record)
                if "offset" in obj:
                    offset = obj["offset"]
                else:
                    break
            data[table_key] = records
        fd.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
