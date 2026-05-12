"""
Advanced Rackbeat API Script with Configuration Support

This is an enhanced version of the location valuation script with:
- Configuration file support
- CSV and JSON export options
- Location filtering
- Detailed logging
- Email notifications (optional)
"""

import configparser
import csv
import json
import logging
import requests
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from rackbeat_valuation import (
    RackbeatClient, 
    LocationValuationAggregator, 
    Location
)


class ConfigManager:
    """Manages configuration from INI files"""
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        
        if Path(config_file).exists():
            self.config.read(config_file)
        else:
            print(f"Warning: Config file '{config_file}' not found")
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values"""
        self.config['rackbeat'] = {
            'api_key': 'YOUR_API_KEY_HERE',
            'date_to': ''
        }
        self.config['output'] = {
            'format': 'json',
            'output_directory': './reports',
            'include_item_details': 'false'
        }
        self.config['reporting'] = {
            'email_recipients': '',
            'email_subject': 'Rackbeat Location Valuation Report'
        }
        self.config['logging'] = {
            'log_level': 'INFO',
            'log_file': 'rackbeat_valuation.log'
        }
        self.config['locations'] = {
            'filter_locations': '',
            'exclude_locations': ''
        }
    
    def get(self, section: str, key: str, default: str = '') -> str:
        """Get a configuration value"""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default
    
    def get_list(self, section: str, key: str) -> List[str]:
        """Get a comma-separated list configuration value"""
        value = self.get(section, key).strip()
        if not value:
            return []
        return [item.strip() for item in value.split(',')]
    
    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value"""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default


class AdvancedLocationValuationAggregator(LocationValuationAggregator):
    """Extended aggregator with filtering and formatting options"""
    
    def __init__(self, client: RackbeatClient, config: ConfigManager):
        """
        Initialize the advanced aggregator
        
        Args:
            client: RackbeatClient instance
            config: ConfigManager instance
        """
        super().__init__(client)
        self.config = config
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging based on configuration"""
        logger = logging.getLogger(__name__)

        if logger.handlers:
            return logger

        log_level = self.config.get('logging', 'log_level', 'INFO')
        logger.setLevel(getattr(logging, log_level))

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_file = self.config.get('logging', 'log_file')
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def _should_include_location(self, location_number: int) -> bool:
        """
        Check if a location should be included based on filter settings
        
        Args:
            location_number: Location number to check
            
        Returns:
            True if location should be included, False otherwise
        """
        # Get filter and exclude lists
        filter_list = self.config.get_list('locations', 'filter_locations')
        exclude_list = self.config.get_list('locations', 'exclude_locations')
        
        # If exclude list is set and location is in it, exclude
        if exclude_list and str(location_number) in exclude_list:
            self.logger.debug(f"Location {location_number} excluded")
            return False
        
        # If filter list is set and location is not in it, exclude
        if filter_list and str(location_number) not in filter_list:
            self.logger.debug(f"Location {location_number} not in filter list")
            return False
        
        return True
    
    def get_filtered_valuations(self, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get valuations with filtering applied
        
        Args:
            date_to: Optional end date for the reports
            
        Returns:
            Filtered list of valuation dictionaries
        """
        all_valuations = self.get_all_top_level_valuations(date_to)
        
        filtered = [v for v in all_valuations 
                   if self._should_include_location(v['location_number'])]
        
        self.logger.info(f"Returned {len(filtered)} locations (filtered from {len(all_valuations)})")
        return filtered


class ReportGenerator:
    """Generates reports in various formats"""
    
    def __init__(self, config: ConfigManager):
        """
        Initialize report generator
        
        Args:
            config: ConfigManager instance
        """
        self.config = config
        self.output_dir = Path(config.get('output', 'output_directory', './reports'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_json(self, valuations: List[Dict[str, Any]], 
                     total_value: float, date_to: Optional[str] = None) -> str:
        """
        Generate JSON report
        
        Args:
            valuations: List of valuation dictionaries
            total_value: Total company value
            date_to: Report date
            
        Returns:
            Path to generated file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"valuation_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "date_to": date_to or "Current",
            "total_value": total_value,
            "location_count": len(valuations),
            "locations": valuations
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return str(filename)
    
    def generate_csv(self, valuations: List[Dict[str, Any]], total_value: float) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"valuation_{timestamp}.csv"

        sorted_valuations = sorted(valuations, key=lambda v: v["location_name"])

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Location Name", "Location Number", "Level", "Main Location Value", "Total (incl. sub-locations)"])

            for val in sorted_valuations:
                writer.writerow([
                    val["location_name"],
                    val["location_number"],
                    0,
                    val["main_location_value"],
                    val["total_value"],
                ])
                for sub in val["sub_locations"]:
                    writer.writerow([
                        f"{val['location_name']} - {sub['location_name']}",
                        sub["location_number"],
                        sub["nesting_level"],
                        sub["value"],
                        "",
                    ])

            writer.writerow([])
            writer.writerow(["GRAND TOTAL (from API)", "", "", "", total_value])

        return str(filename)
    
    def generate_console_report(self, valuations: List[Dict[str, Any]], 
                               total_value: float):
        """
        Print formatted report to console
        
        Args:
            valuations: List of valuation dictionaries
            total_value: Total company value
        """
        print("\n" + "=" * 80)
        print("LOCATION VALUATIONS (Including Sub-Locations)")
        print("=" * 80)
        
        for val in sorted(valuations, key=lambda v: v["location_name"]):
            print(f"\n📍 {val['location_name']} (Location #{val['location_number']})")
            print("-" * 60)
            print(f"  Main Location Value:      {val['main_location_value']:>15,.2f}")

            if val["sub_locations"]:
                print(f"\n  Sub-Locations:")
                for sub in sorted(val["sub_locations"], key=lambda x: x["nesting_level"]):
                    indent = "    " * sub["nesting_level"]
                    label = f"{val['location_name']} - {sub['location_name']}"
                    print(f"{indent}  • {label:.<40} {sub['value']:>12,.2f}")
            
            print(f"\n  {'TOTAL (incl. sub-locations)':.<40} {val['total_value']:>12,.2f}")
            print("-" * 60)
        
        # Summary
        print("\n" + "=" * 80)
        print(f"GRAND TOTAL (All Locations):                    {total_value:>15,.2f}")
        print(f"Location Count:                                 {len(valuations):>15}")
        print("=" * 80)


def main():
    """Main execution function"""
    
    # Load configuration
    config = ConfigManager("config.ini")
    
    # Read token from config if present, otherwise prompt interactively.
    api_key = config.get('rackbeat', 'api_key').strip()
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        api_key = input("Enter Rackbeat Bearer token: ").strip()

    if not api_key:
        print("ERROR: Bearer token is required")
        sys.exit(1)
    
    try:
        # Initialize client and aggregator
        client = RackbeatClient(api_key)
        aggregator = AdvancedLocationValuationAggregator(client, config)
        
        # Get date parameter — default to today if not set in config
        date_to = config.get('rackbeat', 'date_to') or datetime.now().strftime("%Y-%m-%d")
        
        print("Fetching location valuations with sub-locations...")
        print("-" * 60)
        
        # Get filtered valuations
        valuations = aggregator.get_filtered_valuations(date_to)
        
        if not valuations:
            print("No locations found matching the filter criteria")
            sys.exit(0)
        
        # Calculate total
        total_value = sum(v['total_value'] for v in valuations)
        
        # Generate console report
        report_gen = ReportGenerator(config)
        report_gen.generate_console_report(valuations, total_value)
        
        # Generate output files based on configuration
        output_format = config.get('output', 'format', 'json').lower()
        
        files_generated = []
        if output_format in ['json', 'both']:
            json_file = report_gen.generate_json(valuations, total_value, date_to)
            files_generated.append(json_file)
            print(f"\n✓ JSON report saved to: {json_file}")
        
        if output_format in ['csv', 'both']:
            csv_file = report_gen.generate_csv(valuations, total_value)
            files_generated.append(csv_file)
            print(f"✓ CSV report saved to: {csv_file}")
        
        print(f"\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except requests.HTTPError as e:
        print(f"API Error: {e}")
        print("Check your API key and ensure you have access to the Rackbeat API")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
