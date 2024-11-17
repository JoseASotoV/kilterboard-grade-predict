import requests
import json

# API endpoint and headers
url = "https://drmzubrwofxyzyhicvvx.supabase.co/rest/v1/climbs"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzMTI3NDA1MiwiZXhwIjoxOTQ2ODUwMDUyfQ.vBZ8uBgVI3Wc9RaJ2STinaVnd0dY2HHyK42YkqBxUR0"
}

# Total records to retrieve
total_records = 22343
limit = 500
offset = 0

# List to store all the records
all_records = []

# Loop through the API until all records are retrieved
while offset < total_records:
    # Query parameters with offset and limit
    params = {
        "select": "*",
        "order": "total_ascents.desc.nullslast",
        "offset": offset,
        "limit": limit
    }

    # Make the API request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Append the records to the list
        records = response.json()
        all_records.extend(records)
        print(f"Retrieved {len(records)} records, total: {len(all_records)}")

        # Increment the offset
        offset += limit
    else:
        print(f"Failed to retrieve records at offset {offset}. Status code: {response.status_code}")
        break

# Save all the records to a JSON file
with open("../data/climbs_data.json", "w") as json_file:
    json.dump(all_records, json_file, indent=4)

print(f"All records have been saved to climbs_data.json")
