# NAICS to STIX 2.1 Converter for OpenCTI

This script converts [NAICS](https://www.census.gov/naics/) (North American Industry Classification System) sector data into [STIX 2.1](https://oasis-open.github.io/cti-documentation/stix/intro) format, making it compatible for ingestion into [OpenCTI](https://www.opencti.io/), the open-source threat intelligence platform.

## 📂 Source Data

NAICS codes were sourced from the official 2022 list available here:

> [2022 NAICS Codes - 2-Digit through 6-Digit (Excel)](https://www-naics-com.webpkgcache.com/doc/-/s/www.naics.com/wp-content/uploads/2022/05/2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx)

## 📘 What is NAICS?

NAICS is the standard used by Federal statistical agencies in classifying business establishments. It provides a consistent framework for analyzing and comparing economic activity across various sectors and subsectors in North America.

NAICS codes are hierarchical:
- **2-digit codes** represent broad economic sectors.
- **3-digit codes** represent subsectors.
- **4- to 6-digit codes** offer increasingly specific industry definitions.

For example:
- `52` = Finance and Insurance (broad sector)
- `524` = Insurance Carriers and Related Activities (subsector)

## 🎯 Why Convert NAICS to STIX?

By integrating NAICS data into STIX 2.1, threat intelligence platforms like OpenCTI can benefit from structured and standardized industry classification, enabling:
- Better **sector attribution** in threat reports.
- Enhanced **analytical granularity**, allowing users to correlate threat actor activity or malware campaigns with specific economic sectors or industries.
- Improved **data enrichment** capabilities when combining threat intelligence with sector-specific risk analysis.

## 📊 Benefits of Using 2- and 3-digit NAICS Codes

While full 6-digit NAICS codes offer precision, the **2- and 3-digit levels** are often more practical for cybersecurity applications:
- They strike a balance between **detail and generalization** — ideal for threat modeling without overfitting data.
- They help **normalize sector references** in OpenCTI across different data sources.
- Many threat actors are reported to target sectors at the 2- or 3-digit level (e.g., `51` - Information, `62` - Healthcare and Social Assistance), making this granularity particularly useful.

## 🧾 Sample Output

The script outputs a STIX 2.1 bundle containing `Identity` objects with detailed sector information. Below is a truncated example:

```json
{
  "type": "bundle",
  "id": "bundle--fa529a22-36b6-4c03-aa18-764540ea9c13",
  "objects": [
    {
      "type": "identity",
      "spec_version": "2.1",
      "id": "identity--2fe74f0c-66bb-40d0-b759-42d67ea397d7",
      "created": "2024-10-16T14:34:32.721Z",
      "modified": "2024-10-16T14:34:32.721Z",
      "name": "Agriculture, Forestry, Fishing and Hunting",
      "description": "The Agriculture, Forestry, Fishing and Hunting sector comprises establishments primarily engaged in growing crops, raising animals, harvesting timber, and harvesting fish and other animals from a farm, ranch, or their natural habitats.",
      "identity_class": "class",
      "labels": ["naics-11"],
      "x_opencti_aliases": ["naics-11"],
      "x_opencti_type": "Sector"
    },
    {
      "type": "identity",
      "spec_version": "2.1",
      "id": "identity--8fa3380a-b8f2-4638-a2cd-ecbdbf81411f",
      "created": "2024-10-16T14:34:32.721Z",
      "modified": "2024-10-16T14:34:32.721Z",
      "name": "Mining, Quarrying, and Oil and Gas Extraction",
      "description": "The Mining, Quarrying, and Oil and Gas Extraction sector comprises establishments that extract naturally occurring mineral solids, such as coal and ores; liquid minerals, such as crude petroleum; and gases, such as natural gas.",
      "identity_class": "class",
      "labels": ["naics-21"],
      "x_opencti_aliases": ["naics-21"],
      "x_opencti_type": "Sector"
    }
  ]
}
