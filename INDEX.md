
# 📦 Rackbeat Location Valuation Project

A complete Python solution for connecting to Rackbeat API and retrieving stock valuations per location, automatically including all nested sub-locations.

---

## 📂 Project Contents

### 🚀 **START HERE**
- **[QUICKSTART.md](QUICKSTART.md)** ⚡ Get running in 5 minutes
  - Prerequisites check
  - Installation steps
  - Basic and advanced setup
  - Quick troubleshooting

---

### 💻 **Main Scripts**

1. **[rackbeat_valuation.py](rackbeat_valuation.py)** ⭐ MAIN SCRIPT
   - Core functionality (no configuration needed)
   - Simple to use - just add your API key
   - Outputs to console and JSON file
   - Classes: `RackbeatClient`, `LocationValuationAggregator`, `Location`

2. **[rackbeat_valuation_advanced.py](rackbeat_valuation_advanced.py)** 🚀 ADVANCED
   - Configuration file support (config.ini)
   - Multiple output formats (JSON, CSV, both)
   - Location filtering and exclusion
   - Detailed logging
   - Classes: `ConfigManager`, `AdvancedLocationValuationAggregator`, `ReportGenerator`

3. **[example_usage.py](example_usage.py)** 💡 LEARN BY EXAMPLE
   - 9 complete working examples
   - Shows how to use the library in different ways
   - Copy and modify for your needs

---

### ⚙️ **Configuration**

- **[config.ini.example](config.ini.example)** 📋 Configuration Template
  - Copy to `config.ini` and customize
  - Settings for API key, output formats, filtering, logging
  - Detailed comments explaining each option

- **[requirements.txt](requirements.txt)** 📦 Python Dependencies
  - Install with: `pip install -r requirements.txt`
  - Only requires: `requests` library

---

### 📖 **Documentation**

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡ FAST START (5-10 minutes)
   - Step-by-step setup
   - Basic and advanced usage
   - Understanding the output
   - Common tasks
   - Troubleshooting

2. **[README.md](README.md)** 📚 FULL DOCUMENTATION (Comprehensive)
   - Problem description
   - Complete API reference
   - All available options
   - Customization examples
   - Error handling details
   - Scheduling for automation

3. **[FILE_SUMMARY.md](FILE_SUMMARY.md)** 🗂️ FILE DESCRIPTIONS
   - What each file does
   - How files relate to each other
   - Three workflow options
   - Quick reference guide

4. **[INDEX.md](INDEX.md)** 📑 YOU ARE HERE
   - This file
   - Overview of all project files
   - Quick navigation guide

---

## 🎯 Quick Navigation

### I want to...
- **Get started quickly** → [QUICKSTART.md](QUICKSTART.md)
- **Understand the full capabilities** → [README.md](README.md)
- **See working code examples** → [example_usage.py](example_usage.py)
- **Learn about all files** → [FILE_SUMMARY.md](FILE_SUMMARY.md)
- **Set up advanced features** → [config.ini.example](config.ini.example)

### I'm a...
- **Complete beginner** → Read QUICKSTART.md Steps 1-3
- **Python developer** → Run example_usage.py and read the code
- **System admin** → Set up config.ini and use rackbeat_valuation_advanced.py
- **DevOps engineer** → Schedule rackbeat_valuation_advanced.py with cron/Task Scheduler

---

## 📋 Files at a Glance

| File | Purpose | Start With? |
|------|---------|-----------|
| rackbeat_valuation.py | Main script with core logic | ✅ Yes |
| rackbeat_valuation_advanced.py | Advanced with config support | Later |
| example_usage.py | 9 working examples | If you want examples |
| config.ini.example | Configuration template | If using advanced |
| requirements.txt | Python dependencies | Yes, run pip install |
| QUICKSTART.md | Fast start guide | ✅ Yes |
| README.md | Full documentation | Yes, after QUICKSTART |
| FILE_SUMMARY.md | Detailed file descriptions | If curious |
| INDEX.md | This file | You're reading it |

---

## ⚡ 3-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit rackbeat_valuation.py
# Find: API_KEY = "YOUR_API_KEY_HERE"
# Replace with your actual Rackbeat API key

# 3. Run
python rackbeat_valuation.py
```

**Result:** Console output + `rackbeat_valuations.json` file created

---

## 🔄 Full Setup (10 minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Copy configuration
cp config.ini.example config.ini

# 3. Edit config.ini with your API key and settings

# 4. Run advanced version
python rackbeat_valuation_advanced.py
```

**Result:** JSON + CSV files in `./reports` directory

---

## 🎓 Learning Path

1. **First Time?**
   - Read: QUICKSTART.md (sections 1-3)
   - Do: Add API key to rackbeat_valuation.py
   - Run: `python rackbeat_valuation.py`

2. **Want Advanced Features?**
   - Read: QUICKSTART.md (section 4)
   - Do: Copy config.ini.example → config.ini
   - Run: `python rackbeat_valuation_advanced.py`

3. **Want Custom Solutions?**
   - Read: example_usage.py
   - Read: Code comments in rackbeat_valuation.py
   - Code: Your own script using the classes

4. **Want Full Details?**
   - Read: README.md (complete reference)
   - Read: FILE_SUMMARY.md (file relationships)

---

## 🐍 Python Classes Available

### RackbeatClient
```python
from rackbeat_valuation import RackbeatClient

client = RackbeatClient("YOUR_API_KEY")
locations = client.get_locations()
report = client.get_valuation_report(1004)
children = client.get_all_descendants(1004)
```

### LocationValuationAggregator
```python
from rackbeat_valuation import LocationValuationAggregator

agg = LocationValuationAggregator(client)
valuations = agg.get_all_top_level_valuations()
one_location = agg.get_location_value_with_subs(location)
```

### Location (Data Model)
```python
location.number       # Location number
location.name         # Location name
location.parent_id    # Parent location ID (None if top-level)
location.is_top_level()  # Check if it's a top-level location
```

---

## 🆘 Quick Help

### Common Issues

**"ModuleNotFoundError: No module named 'requests'"**
```bash
pip install -r requirements.txt
```

**"Please set your Rackbeat API key"**
- Open rackbeat_valuation.py
- Find `API_KEY = "YOUR_API_KEY_HERE"`
- Replace with your actual key from Rackbeat

**"Authorization Failed"**
- Verify your API key is correct
- Check API is enabled in your Rackbeat account
- See Rackbeat documentation for API access

**"No locations found"**
- Check you have locations set up in Rackbeat
- Check filter settings if using config.ini
- Verify user has permission to view locations

---

## 📞 Support Resources

- **Rackbeat API Docs:** https://developer.rackbeat.com/
- **Rackbeat Support:** https://helpdesk.rackbeat.com/
- **Python Requests:** https://docs.python-requests.org/
- **This Project README:** [README.md](README.md)

---

## 🎁 What This Project Does

```
Problem: Rackbeat's Valuation Report endpoint only shows value 
         for the specified location, not sub-locations

Solution: This script:
  1. Gets all locations
  2. For each location, recursively fetches ALL sub-locations
  3. Gets valuation for main location + all sub-locations
  4. Totals and aggregates the values
  5. Exports in your chosen format (JSON/CSV)

Result: You get total value per location INCLUDING all nested sub-locations!
```

---

## ✨ Features

- ✅ Recursive sub-location fetching
- ✅ Automatic value aggregation
- ✅ Multiple output formats (JSON, CSV)
- ✅ Location filtering and exclusion
- ✅ Date-specific valuations
- ✅ Detailed logging
- ✅ Configuration file support
- ✅ Console + file output
- ✅ Easy to integrate into your code
- ✅ Fully documented with examples

---

## 🚀 Ready to Go?

### Beginner: Read QUICKSTART.md → Run Script → Done ✅

### Developer: Read example_usage.py → Integrate Code → Automate 🔄

### Advanced: Setup config.ini → Run Advanced Script → Schedule 📅

---

**Questions?** Check the README.md or example_usage.py - they cover everything!

**Ready?** Start with [QUICKSTART.md](QUICKSTART.md) 👉

---

*Rackbeat Location Valuation Project*
*Version 1.0 - May 2024*
