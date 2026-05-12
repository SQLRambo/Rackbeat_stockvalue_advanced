# Rackbeat API - Location Valuation Script

This Python script connects to the Rackbeat API to retrieve stock valuations per location, including values from all sub-locations (nested locations).

## Problem It Solves

The Rackbeat Valuation Report endpoint only returns the value for the specified location and does not automatically include sub-locations. This script:

1. Gets all top-level locations
2. Recursively fetches all sub-locations for each location
3. Retrieves valuation data for each location and all its sub-locations
4. Aggregates the values to show the total value per main location (including all descendants)

## Requirements

- Python 3.7 or higher
- `requests` library

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install requests
```

## Setup

1. **Get your Rackbeat Bearer token:**
   - Log in to your Rackbeat account
   - Navigate to Account Settings
   - Find the API token section (or contact support if you need to enable API access)
   - Copy your token

2. **Run the script and paste token when prompted:**
   - The script asks for `Enter Rackbeat Bearer token:`
   - Token input is hidden (secure prompt)
   - No hardcoded token is required

## Usage

### Basic Usage

Run the script to get valuations for all top-level locations:

```bash
python rackbeat_valuation.py
```

When prompted, paste your Bearer token.

### With a Specific Date

To get valuations as of a specific date, modify the script:

```python
DATE_TO = "2024-05-08"  # Format: YYYY-MM-DD
```

## Output

The script generates:

1. **Console Output**: A formatted table showing:
   - Location name and number
   - Main location value
   - Sub-location values (with nesting indication)
   - Total value (including all sub-locations)

2. **JSON File**: `rackbeat_valuations.json` containing:
   - Timestamp of the report
   - Date used for the valuation
   - Total company value
   - Detailed breakdown for each location

### Example Output

```
================================================================================
LOCATION VALUATIONS (Including Sub-Locations)
================================================================================

📍 Lager Sjælland (Location #1004)
------------------------------------------------------------
  Main Location Value:      50,000.00

  Sub-Locations:
      • Lager Sjælland - A........................  25,000.00
      • Lager Sjælland - B........................  15,000.00
        • Lager Sjælland - B1.....................   5,000.00

  TOTAL (incl. sub-locations)................ 95,000.00
------------------------------------------------------------
...
================================================================================
GRAND TOTAL (All Locations):                    250,000.00
================================================================================
```

## API Endpoints Used

- `GET /locations` - List all locations
- `GET /locations/{location_number}/children` - Get sub-locations
- `GET /reports/valuation` - Get valuation report for a location

## Classes and Functions

### RackbeatClient

Main client for API communication:
- `get_locations()` - Get all locations
- `get_location_children(location_number)` - Get sub-locations
- `get_valuation_report(location_number, date_to)` - Get valuation data
- `get_all_descendants(location_number)` - Recursively get all descendants

### LocationValuationAggregator

Handles valuation aggregation:
- `get_location_value_with_subs(location, date_to)` - Get total value for location including subs
- `get_all_top_level_valuations(date_to)` - Get valuations for all top-level locations

### Location (Dataclass)

Represents a Rackbeat location with:
- number
- name
- parent_id
- children_count
- nesting_level

## Error Handling

The script handles common errors:
- Invalid API key
- Network errors
- Rate limiting (will raise HTTPError)
- Missing or malformed responses

Check the console output for error messages if something fails.

## Troubleshooting

### "Authorization Failed" Error
- Verify your API key is correct
- Check that API access is enabled for your account
- Ensure the API key hasn't expired

### "No locations found"
- Your Rackbeat account may not have any locations set up
- Check that you have permission to view locations

### Empty valuations
- Locations may not have any stock
- Check the date_to parameter - it may be in the future
- Verify that the locations actually have inventory

## Customization

You can extend the script to:

### Filter by specific locations:
```python
valuations = [v for v in aggregator.get_all_top_level_valuations() 
              if v['location_number'] in [1004, 1003]]
```

### Export to CSV:
```python
import csv
with open('valuations.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['location_number', 'location_name', 'total_value'])
    writer.writerows(valuations)
```

### Set up scheduled runs:
Use cron (Linux/Mac) or Task Scheduler (Windows) to run the script daily/weekly

## API Rate Limiting

Rackbeat API has rate limits. For accounts with many locations, consider:
- Adding delays between requests
- Caching location data
- Running reports during off-peak hours

## Support

For issues with:
- **The script**: Check the error message and troubleshooting section
- **Rackbeat API**: Visit https://developer.rackbeat.com/ or contact Rackbeat support
- **Python**: Refer to Python documentation

## License

This script is provided as-is for use with Rackbeat API.

## Additional Resources

- [Rackbeat API Documentation](https://developer.rackbeat.com/)
- [Rackbeat Support](https://helpdesk.rackbeat.com/)
- Python Requests Library: https://docs.python-requests.org/
