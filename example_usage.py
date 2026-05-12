"""
Example Usage - How to Use the Rackbeat Valuation Script

This file shows various ways to use the rackbeat_valuation module
in your own Python scripts.
"""

from rackbeat_valuation import RackbeatClient, LocationValuationAggregator
import json


# Example 1: Basic Usage - Get all location valuations
def example_basic_usage():
    """Most basic example - get valuations for all locations"""
    
    API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
    
    # Create client
    client = RackbeatClient(API_KEY)
    
    # Create aggregator
    aggregator = LocationValuationAggregator(client)
    
    # Get all valuations with sub-locations
    valuations = aggregator.get_all_top_level_valuations()
    
    # Print results
    for val in valuations:
        print(f"{val['location_name']}: {val['total_value']:,.2f}")


# Example 2: Get valuation for a specific location only
def example_single_location():
    """Get valuation for just one location and its sub-locations"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    location_number = 1004
    
    client = RackbeatClient(API_KEY)
    
    # Get location details
    all_locations = client.get_locations()
    location = next((loc for loc in all_locations if loc.number == location_number), None)
    if location is None:
        print(f"Location {location_number} not found")
        return
    
    # Get aggregator
    aggregator = LocationValuationAggregator(client)
    
    # Get valuation for this specific location
    valuation = aggregator.get_location_value_with_subs(location)
    
    print(f"Location: {valuation['location_name']}")
    print(f"Total value (including sub-locations): {valuation['total_value']:,.2f}")
    print(f"Number of sub-locations: {len(valuation['sub_locations'])}")


# Example 3: Get location hierarchy without valuations
def example_location_hierarchy():
    """Show the location hierarchy structure"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    all_locations = client.get_locations()
    
    # Group by top-level locations
    top_level = [loc for loc in all_locations if loc.is_top_level()]
    
    for top_loc in top_level:
        print(f"\n{top_loc.name} (#{top_loc.number})")
        
        # Get children
        descendants = client.get_all_descendants(top_loc.number)
        
        for desc in sorted(descendants, key=lambda x: (x.nesting_level, x.name)):
            indent = "  " * (desc.nesting_level + 1)
            print(f"{indent}└─ {desc.name} (#{desc.number})")


# Example 4: Compare valuations across dates
def example_date_comparison():
    """Compare valuations for different dates"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    # Get valuations for two dates
    date1 = "2024-01-31"
    date2 = "2024-02-29"
    
    valuations_date1 = aggregator.get_all_top_level_valuations(date1)
    valuations_date2 = aggregator.get_all_top_level_valuations(date2)
    
    # Compare
    for v1 in valuations_date1:
        v2 = next((v for v in valuations_date2
                   if v['location_number'] == v1['location_number']), None)
        if v2 is None:
            print(f"Location {v1['location_name']} not found in {date2} results, skipping")
            continue
        
        difference = v2['total_value'] - v1['total_value']
        percent_change = (difference / v1['total_value'] * 100) if v1['total_value'] > 0 else 0
        
        print(f"{v1['location_name']:.<40}")
        print(f"  {date1}: {v1['total_value']:>12,.2f}")
        print(f"  {date2}: {v2['total_value']:>12,.2f}")
        print(f"  Change: {difference:>12,.2f} ({percent_change:+.1f}%)\n")


# Example 5: Export to CSV manually
def example_csv_export():
    """Export valuations to CSV format"""
    
    import csv
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    valuations = aggregator.get_all_top_level_valuations()
    
    # Write to CSV
    with open('rackbeat_export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'location_name', 'location_number', 'main_value', 
            'sub_count', 'total_value'
        ])
        writer.writeheader()
        
        for val in valuations:
            writer.writerow({
                'location_name': val['location_name'],
                'location_number': val['location_number'],
                'main_value': val['main_location_value'],
                'sub_count': len(val['sub_locations']),
                'total_value': val['total_value']
            })
    
    print("Exported to rackbeat_export.csv")


# Example 6: Get only locations above a certain value
def example_filter_by_value():
    """Find locations with total value above threshold"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    MIN_VALUE = 50000  # 50,000 currency units
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    valuations = aggregator.get_all_top_level_valuations()
    
    # Filter by value
    high_value_locations = [v for v in valuations 
                           if v['total_value'] >= MIN_VALUE]
    
    print(f"Locations with value >= {MIN_VALUE:,.2f}:")
    for val in sorted(high_value_locations, 
                     key=lambda x: x['total_value'], 
                     reverse=True):
        print(f"  {val['location_name']:.<40} {val['total_value']:>12,.2f}")


# Example 7: Analyze sub-location distribution
def example_analyze_sub_locations():
    """Analyze how value is distributed among sub-locations"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    valuations = aggregator.get_all_top_level_valuations()
    
    for val in valuations:
        total = val['total_value']
        main = val['main_location_value']
        
        if total > 0:
            main_pct = (main / total * 100) if main > 0 else 0
            sub_pct = 100 - main_pct
            
            print(f"\n{val['location_name']}:")
            print(f"  Main location:  {main_pct:>5.1f}%  ({main:>12,.2f})")
            print(f"  Sub-locations:  {sub_pct:>5.1f}%  ({total-main:>12,.2f})")


# Example 8: Use case - Find imbalanced locations
def example_identify_imbalances():
    """Identify locations with unusual value distributions"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    valuations = aggregator.get_all_top_level_valuations()
    
    print("Locations with most value in sub-locations (unusual distribution):\n")
    
    for val in valuations:
        total = val['total_value']
        main = val['main_location_value']
        
        if total > 0:
            sub_value = total - main
            sub_pct = sub_value / total * 100
            
            # Flag if >80% is in sub-locations
            if sub_pct > 80:
                print(f"⚠️  {val['location_name']:.<40} {sub_pct:.0f}% in sub-locations")


# Example 9: Generate summary statistics
def example_summary_stats():
    """Generate summary statistics across all locations"""
    
    API_KEY = "YOUR_API_KEY_HERE"
    
    client = RackbeatClient(API_KEY)
    aggregator = LocationValuationAggregator(client)
    
    valuations = aggregator.get_all_top_level_valuations()
    
    values = [v['total_value'] for v in valuations]
    
    if values:
        print("Summary Statistics")
        print("=" * 50)
        print(f"Number of locations:    {len(valuations)}")
        print(f"Total value:            {sum(values):>15,.2f}")
        print(f"Average value:          {sum(values)/len(values):>15,.2f}")
        print(f"Min value:              {min(values):>15,.2f}")
        print(f"Max value:              {max(values):>15,.2f}")
        
        # Median
        sorted_values = sorted(values)
        median = (sorted_values[len(sorted_values)//2] 
                 if len(sorted_values) % 2 == 1 
                 else (sorted_values[len(sorted_values)//2-1] + 
                      sorted_values[len(sorted_values)//2]) / 2)
        print(f"Median value:           {median:>15,.2f}")


if __name__ == "__main__":
    """
    To run examples:
    
    1. Uncomment the example function you want to run
    2. Replace API_KEY with your actual key
    3. Run: python example_usage.py
    
    Examples to try:
    """
    
    print("""
    Available examples:
    1. example_basic_usage() - Get valuations for all locations
    2. example_single_location() - Get valuation for one location
    3. example_location_hierarchy() - Show location structure
    4. example_date_comparison() - Compare two dates
    5. example_csv_export() - Export to CSV
    6. example_filter_by_value() - Find high-value locations
    7. example_analyze_sub_locations() - Analyze value distribution
    8. example_identify_imbalances() - Find unusual distributions
    9. example_summary_stats() - Generate statistics
    
    Uncomment one of the functions below to run it.
    """)
    
    # Uncomment one of these to run:
    # example_basic_usage()
    # example_single_location()
    # example_location_hierarchy()
    # example_date_comparison()
    # example_csv_export()
    # example_filter_by_value()
    # example_analyze_sub_locations()
    # example_identify_imbalances()
    # example_summary_stats()
