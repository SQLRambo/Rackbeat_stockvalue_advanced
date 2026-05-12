# Rackbeat Location Valuation Project - File Summary

## Overview

This project provides Python scripts to connect to the Rackbeat API and retrieve stock valuations per location, including values from all nested sub-locations. The API's Valuation Report endpoint only returns the value for the specified location, so this project recursively fetches sub-locations and aggregates the values.

## Project Files

### Core Scripts

#### 1. **rackbeat_valuation.py** ⭐ START HERE
The main script with all the core functionality.

**What it does:**
- Connects to Rackbeat API using your API key
- Fetches all locations and their hierarchies
- Recursively retrieves sub-locations at any nesting level
- Gets valuation reports for each location
- Aggregates values to show total per location including sub-locations
- Outputs results to console and JSON file

**How to use:**
```python
API_KEY = "YOUR_API_KEY_HERE"
python rackbeat_valuation.py
```

**Contains:**
- `RackbeatClient` - API client with methods for:
  - `get_locations()` - Get all locations
  - `get_location_children()` - Get sub-locations of a location
  - `get_valuation_report()` - Get valuation for a location
  - `get_all_descendants()` - Recursively get all sub-locations

- `LocationValuationAggregator` - Aggregates valuations:
  - `get_location_value_with_subs()` - Get total for one location
  - `get_all_top_level_valuations()` - Get all top-level locations

---

#### 2. **rackbeat_valuation_advanced.py** 🚀 ADVANCED
Extended version with configuration file support and more features.

**Additional Features:**
- Configuration file support (config.ini)
- Filtering by specific locations
- Excluding specific locations
- Multiple output formats (JSON, CSV, or both)
- Detailed logging
- Report generation with formatting

**How to use:**
```bash
# Copy configuration template
cp config.ini.example config.ini

# Edit config.ini with your settings
# Then run:
python rackbeat_valuation_advanced.py
```

**Contains:**
- `ConfigManager` - Reads and manages config.ini
- `AdvancedLocationValuationAggregator` - Extended aggregator with filtering
- `ReportGenerator` - Generates JSON, CSV, and console reports

---

### Configuration & Setup

#### 3. **config.ini.example**
Template configuration file.

**What to customize:**
- `api_key` - Your Rackbeat API key (required)
- `date_to` - Optional specific date for valuation
- `format` - Output format: json, csv, or both
- `filter_locations` - Process only specific locations
- `exclude_locations` - Skip certain locations
- `log_level` - Logging verbosity

**Usage:**
```bash
cp config.ini.example config.ini
# Edit config.ini with your settings
```

---

#### 4. **requirements.txt**
Python package dependencies.

**Contains:** `requests>=2.28.0`

**Installation:**
```bash
pip install -r requirements.txt
```

---

### Documentation

#### 5. **README.md** 📖 COMPREHENSIVE
Full documentation covering:
- Problem description and solution
- Installation instructions
- Setup requirements
- How to get your API key
- Usage examples
- Output format explanation
- Available classes and methods
- Error handling and troubleshooting
- Customization options
- Scheduling for automated runs

**Read this for:** Complete understanding of what the script does and how to use it.

---

#### 6. **QUICKSTART.md** ⚡ FAST START
Quick 5-step guide to get started immediately.

**Includes:**
- Step 1: Prerequisites check
- Step 2: Install dependencies
- Step 3: Basic usage (simple script)
- Step 4: Advanced usage (with config)
- Step 5: Understanding output
- Common troubleshooting
- Quick task examples

**Read this for:** Getting up and running in 5 minutes.

---

### Examples & Learning

#### 7. **example_usage.py** 💡 LEARN BY EXAMPLE
Nine complete examples showing how to use the library in different ways.

**Includes Examples For:**
1. Basic usage - Get all location valuations
2. Single location - Get one location with subs
3. Location hierarchy - Show structure without valuations
4. Date comparison - Compare two dates
5. CSV export - Export to CSV format
6. Filter by value - Find high-value locations
7. Analyze distribution - How value splits between main/sub
8. Identify imbalances - Find unusual distributions
9. Summary statistics - Aggregate statistics

**How to use:**
- Open the file
- Uncomment one example function
- Add your API key
- Run: `python example_usage.py`

---

## Quick Start Paths

### 🏃 Super Quick (2 minutes)
1. Read: **QUICKSTART.md** (Step 1-2)
2. Set up: Copy API key into **rackbeat_valuation.py**
3. Run: `python rackbeat_valuation.py`

### 👨‍💻 Developer (10 minutes)
1. Read: **QUICKSTART.md**
2. Install: `pip install -r requirements.txt`
3. Try: **example_usage.py**
4. Copy and modify examples for your use case

### 🔧 Full Setup (30 minutes)
1. Read: **README.md**
2. Install: `pip install -r requirements.txt`
3. Setup: Copy and configure **config.ini**
4. Run: `python rackbeat_valuation_advanced.py`
5. Schedule: Set up automated runs with cron/Task Scheduler

---

## File Relationships

```
┌─ rackbeat_valuation.py ◄─── CORE LIBRARY
│  └─ RackbeatClient (API calls)
│  └─ LocationValuationAggregator (Aggregation logic)
│  └─ Location (Data model)
│
├─ rackbeat_valuation_advanced.py (extends core)
│  ├─ ConfigManager (reads config.ini)
│  ├─ AdvancedLocationValuationAggregator (extends core aggregator)
│  └─ ReportGenerator (formats output)
│
├─ config.ini (configuration file)
└─ config.ini.example (template)

example_usage.py (imports core library)
```

---

## Typical Workflow

### Setup (One-time)
```bash
1. pip install -r requirements.txt
2. Add API key to rackbeat_valuation.py
3. Test: python rackbeat_valuation.py
```

### Daily Use (With config)
```bash
1. cp config.ini.example config.ini
2. Edit config.ini with your API key
3. python rackbeat_valuation_advanced.py
4. Check output files in ./reports
```

### Integration (In your code)
```python
from rackbeat_valuation import RackbeatClient, LocationValuationAggregator

client = RackbeatClient("YOUR_API_KEY")
agg = LocationValuationAggregator(client)
valuations = agg.get_all_top_level_valuations()

# Process valuations...
```

---

## Key Concepts

### Locations Hierarchy
```
Rackbeat allows nested locations:
  
  Lager Sjælland (parent)
    ├─ Zone A (child)
    │   └─ Shelf A1 (grandchild)
    └─ Zone B (child)

The Valuation Report only shows value for the queried location.
This script automatically includes all descendants.
```

### Valuation Aggregation
```
Main location value:           50,000
Sub-location values:           
  - Zone A:                    30,000
  - Zone B:                    20,000
────────────────────────────────────
Total (what we calculate):   100,000
```

### Output Formats

**Console:** Human-readable table
**JSON:** Machine-readable with all details
**CSV:** Spreadsheet-compatible

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "No module named 'requests'" | `pip install -r requirements.txt` |
| "API key error" | Add real API key to script |
| "No locations found" | Check filter settings in config |
| "Authorization failed" | Verify API key in Rackbeat settings |
| "Script is slow" | Normal with many locations; run off-peak |

---

## Next Steps

1. **Immediate:** Run `python rackbeat_valuation.py` with your API key
2. **Quick:** Read **QUICKSTART.md** for common tasks
3. **Full:** Read **README.md** for all capabilities
4. **Learning:** Check **example_usage.py** for code examples
5. **Advanced:** Customize **config.ini** and **rackbeat_valuation_advanced.py**

---

## Need Help?

- **Getting API key:** Rackbeat account → Settings → API
- **API documentation:** https://developer.rackbeat.com/
- **Script errors:** Check console output and error messages
- **Rackbeat support:** https://helpdesk.rackbeat.com/

---

## Project Structure

```
project-root/
├── rackbeat_valuation.py                 (Main script)
├── rackbeat_valuation_advanced.py        (Advanced with config)
├── example_usage.py                      (9 usage examples)
├── config.ini.example                    (Config template)
├── requirements.txt                      (Dependencies)
├── README.md                             (Full documentation)
├── QUICKSTART.md                         (Quick start guide)
└── FILE_SUMMARY.md                       (This file)
```

---

**Last Updated:** 2024-05-08
**Version:** 1.0
**Status:** Ready for production use

Good luck! 🚀
