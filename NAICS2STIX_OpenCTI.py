import pandas as pd
from stix2 import Identity, Relationship, Bundle
import json
from datetime import datetime
import uuid
'''
NAICS XLSX sourced here: https://www-naics-com.webpkgcache.com/doc/-/s/www.naics.com/wp-content/uploads/2022/05/2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx
'''
def get_current_time():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def create_identity(naics_code, title, description):
    tag = f"naics-{naics_code}"
    return Identity(
        id=f"identity--{str(uuid.uuid4())}",
        name=title,
        description=description,
        identity_class="class",
        labels=[tag],
        created=get_current_time(),
        modified=get_current_time()
    )

def create_relationship(subsector, sector):
    return Relationship(
        relationship_type="part-of",
        source_ref=subsector.id,
        target_ref=sector.id,
        created=get_current_time(),
        modified=get_current_time()
    )
def in_naics_range(subsector_code, sector_code):
    if "-" in sector_code:
        start, end = sector_code.split("-")
        return start <= subsector_code <= end
    return subsector_code == sector_code

def main():
    # Load the Excel file
    file_path = "Inputs/2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx"  
    excel_data = pd.ExcelFile(file_path)
    two_digit_naics_df = pd.read_excel(excel_data, sheet_name='Two Digit NAICS')
    three_digit_naics_df = pd.read_excel(excel_data, sheet_name='Three Digit NAICS')

    # Process Two-Digit NAICS (Sectors)
    sectors = {}
    for index, row in two_digit_naics_df.iterrows():
        naics_code = str(row['2022 NAICS US   Code'])
        title = row['2022 NAICS US Title'].strip()
        description = row['Description']
        sector = create_identity(naics_code, title, description)
        sectors[naics_code] = sector

    # Process Three-Digit NAICS (Subsectors) and establish relationships
    subsectors = []
    relationships = []
    for index, row in three_digit_naics_df.iterrows():
        naics_code = str(row['2022 NAICS US   Code']) 
        title = row['2022 NAICS US Title'].strip()  
        description = row['Description']
        subsector = create_identity(naics_code, title, description)
        subsectors.append(subsector)

        # Identify the parent sector
        parent_sector = None
        for sector_code, sector_obj in sectors.items():
            if in_naics_range(naics_code[:2], sector_code): 
                parent_sector = sector_obj
                break

        if parent_sector:
            relationship = create_relationship(subsector, parent_sector)
            relationships.append(relationship)

    bundle = Bundle(objects=[*sectors.values(), *subsectors, *relationships])

    stix_json = json.loads(bundle.serialize(pretty=True))

    for obj in stix_json['objects']:
        if obj['type'] == 'identity':
            obj['x_opencti_aliases'] = [f"naics-{obj['labels'][0].split('-')[-1]}"]
            obj['x_opencti_type'] = "Sector"

    output_file_path = 'Outputs\\naics_stix_bundle.json' 

    with open(output_file_path, 'w') as file:
        json.dump(stix_json, file, indent=4)

    print(f"STIX bundle written to {output_file_path}")

if __name__ == '__main__':
    main()
