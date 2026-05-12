"""
Rackbeat API Script - Location Valuation with Sub-locations

This script connects to the Rackbeat API to retrieve stock valuations per location,
including values from all sub-locations. The Valuation Report endpoint only returns
values for the specified location, so we need to:

1. Get all top-level locations
2. For each location, fetch all sub-locations recursively
3. Get valuation data for the main location and all sub-locations
4. Aggregate to show total value per main location (including sub-locations)
"""

import requests
import csv
from datetime import date
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Location:
    """Represents a location from the Rackbeat API"""
    number: int
    name: str
    parent_id: Optional[int] = None
    children_count: int = 0
    nesting_level: int = 0
    
    def is_top_level(self) -> bool:
        """Check if this is a top-level location"""
        return self.parent_id is None


class RackbeatClient:
    """Client for interacting with the Rackbeat API"""
    
    BASE_URL = "https://app.rackbeat.com/api"
    
    def __init__(self, api_key: str):
        """
        Initialize the Rackbeat client
        
        Args:
            api_key: Your Rackbeat API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the Rackbeat API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Optional query parameters
            
        Returns:
            Response JSON as dictionary
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.request(method, url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_locations(self) -> List[Location]:
        """
        Get all locations from Rackbeat
        
        Returns:
            List of Location objects
        """
        data = self._make_request("GET", "locations")
        locations = []
        for loc_data in data.get("locations", []):
            location = Location(
                number=loc_data["number"],
                name=loc_data["name"],
                parent_id=loc_data.get("parent_id"),
                children_count=loc_data.get("children_count", 0),
                nesting_level=loc_data.get("nesting_level", 0)
            )
            locations.append(location)
        return locations
    
    def get_location_children(self, location_number: int) -> List[Location]:
        """
        Get all sub-locations (children) of a specific location
        
        Args:
            location_number: The parent location number
            
        Returns:
            List of Location objects that are children of the parent
        """
        data = self._make_request("GET", f"locations/{location_number}/children")
        locations = []
        for loc_data in data.get("locations", []):
            location = Location(
                number=loc_data["number"],
                name=loc_data["name"],
                parent_id=loc_data.get("parent_id"),
                children_count=loc_data.get("children_count", 0),
                nesting_level=loc_data.get("nesting_level", 0)
            )
            locations.append(location)
        return locations
    
    def get_valuation_report(self, location_number: int, date_to: Optional[str] = None) -> Dict[str, Any]:
        params = {"location": str(location_number)}
        if date_to:
            params["date_to"] = date_to
        return self._make_request("GET", "reports/valuation", params=params)

    def get_grand_total(self, date_to: Optional[str] = None) -> float:
        params = {}
        if date_to:
            params["date_to"] = date_to
        data = self._make_request("GET", "reports/valuation/total", params=params)
        for key in ("total_value", "value", "total"):
            if key in data:
                return float(data[key] or 0)
        return 0.0
    
    def get_all_descendants(self, location_number: int) -> List[Location]:
        """
        Recursively get all descendants (sub-locations at any level) of a location
        
        Args:
            location_number: The parent location number
            
        Returns:
            List of all descendant Location objects
        """
        descendants = []
        children = self.get_location_children(location_number)
        
        for child in children:
            descendants.append(child)
            # Recursively get descendants of this child
            descendants.extend(self.get_all_descendants(child.number))
        
        return descendants


class LocationValuationAggregator:
    """Aggregates location valuations including sub-locations"""
    
    def __init__(self, client: RackbeatClient):
        """
        Initialize the aggregator
        
        Args:
            client: RackbeatClient instance
        """
        self.client = client
        self.all_locations = None
    
    def _extract_valuation(self, report: Dict[str, Any]) -> float:
        """
        Extract the total valuation from a valuation report
        
        Args:
            report: Valuation report data
            
        Returns:
            Total valuation amount (as float)
        """
        if not isinstance(report, dict):
            return 0.0

        if "total_value" in report:
            try:
                return float(report.get("total_value") or 0)
            except (TypeError, ValueError):
                pass

        total = 0.0
        for item in report.get("lineables", []):
            try:
                total += float(item.get("value") or 0)
            except (TypeError, ValueError):
                continue
        return total
    
    def get_location_value_with_subs(self, location: Location, date_to: Optional[str] = None) -> Dict[str, Any]:
        result = {
            "location_number": location.number,
            "location_name": location.name,
            "nesting_level": location.nesting_level,
            "main_location_value": 0.0,
            "sub_locations": [],
            "total_value": 0.0,
            "items_breakdown": []
        }

        try:
            report = self.client.get_valuation_report(location.number, date_to)
            main_value = self._extract_valuation(report)
            result["main_location_value"] = main_value
            result["items_breakdown"] = report.get("lineables", [])
        except requests.HTTPError as e:
            print(f"Error getting valuation for location {location.number}: {e}")

        total_value = result["main_location_value"]
        for sub_location in self.client.get_all_descendants(location.number):
            try:
                sub_report = self.client.get_valuation_report(sub_location.number, date_to)
                sub_value = self._extract_valuation(sub_report)
                result["sub_locations"].append({
                    "location_number": sub_location.number,
                    "location_name": sub_location.name,
                    "value": sub_value,
                    "nesting_level": sub_location.nesting_level
                })
                total_value += sub_value
            except requests.HTTPError as e:
                print(f"Error getting valuation for sub-location {sub_location.number}: {e}")

        result["total_value"] = total_value
        return result

    def get_all_top_level_valuations(self, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        if self.all_locations is None:
            self.all_locations = self.client.get_locations()

        top_level_locations = [loc for loc in self.all_locations if loc.is_top_level()]

        results = []
        for location in top_level_locations:
            print(f"Processing location: {location.name} ({location.number})")
            results.append(self.get_location_value_with_subs(location, date_to))

        return results


def main():
    """Main execution function"""

    # The token is requested at runtime to avoid hardcoding credentials.
    api_token = input("Enter Rackbeat Bearer token: ").strip()

    default_date = date.today().strftime("%Y-%m-%d")
    date_input = input(f"Valuation date (YYYY-MM-DD) [{default_date}]: ").strip()
    DATE_TO = date_input if date_input else default_date

    if not api_token:
        print("ERROR: Bearer token is required")
        return
    
    try:
        # Initialize client and aggregator
        client = RackbeatClient(api_token)
        aggregator = LocationValuationAggregator(client)
        
        print("Fetching location valuations with sub-locations...")
        print("-" * 60)
        
        # Get all valuations
        valuations = sorted(
            aggregator.get_all_top_level_valuations(DATE_TO),
            key=lambda v: v["location_name"]
        )

        # Display results
        print("\n" + "=" * 80)
        print("LOCATION VALUATIONS (Including Sub-Locations)")
        print("=" * 80)

        for val in valuations:
            print(f"\n📍 {val['location_name']} (Location #{val['location_number']})")
            print("-" * 60)
            print(f"  Main Location Value:      {val['main_location_value']:>15,.2f}")

            if val["sub_locations"]:
                print(f"\n  Sub-Locations:")
                for sub in val["sub_locations"]:
                    indent = "    " * sub["nesting_level"]
                    label = f"{val['location_name']} - {sub['location_name']}"
                    print(f"{indent}  • {label:.<40} {sub['value']:>12,.2f}")

            print(f"\n  {'TOTAL (incl. sub-locations)':.<40} {val['total_value']:>12,.2f}")
            print("-" * 60)

        computed_total = round(sum(val["total_value"] for val in valuations), 2)
        api_total = client.get_grand_total(DATE_TO)
        diff = computed_total - api_total

        print("\n" + "=" * 80)
        print(f"GRAND TOTAL (computed from all locations):      {computed_total:>15,.2f}")
        print(f"GRAND TOTAL (from API endpoint):                {api_total:>15,.2f}")
        print(f"Difference:                                     {diff:>+15,.2f}")
        print("=" * 80)

        # Save results to semicolon-separated CSV file
        output_file = "rackbeat_valuations.csv"
        with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Location Name", "Location Number", "Level", "Main Location Value", "Total (incl. sub-locations)", "Running Subtotal"])
            running = 0.0
            for val in valuations:
                running = round(running + val["main_location_value"], 2)
                writer.writerow([
                    val["location_name"],
                    val["location_number"],
                    val["nesting_level"] + 1,
                    val["main_location_value"],
                    val["total_value"],
                    running
                ])
                for sub in val["sub_locations"]:
                    running = round(running + sub["value"], 2)
                    writer.writerow([
                        f"{val['location_name']} - {sub['location_name']}",
                        sub["location_number"],
                        sub["nesting_level"] + 1,
                        sub["value"],
                        "",
                        running
                    ])
            writer.writerow([])
            writer.writerow(["GRAND TOTAL (computed)", "", "", "", computed_total, running])
            writer.writerow(["GRAND TOTAL (API endpoint)", "", "", "", api_total, ""])
            writer.writerow(["Difference", "", "", "", diff, ""])
        
        print(f"\nResults saved to: {output_file}")
        
    except requests.HTTPError as e:
        print(f"API Error: {e}")
        print("Check your API key and ensure you have access to the Rackbeat API")
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
