# Quick Start Guide

Follow these steps to get the Rackbeat location valuation script running.

## Step 1: Prerequisites

- **Python 3.7 or higher** installed on your system
- **Your Rackbeat Bearer token** (from your account settings)
- Internet connection

## Step 2: Install Dependencies

Open your terminal/command prompt in this directory and run:

```bash
pip install -r requirements.txt
```

This installs the `requests` library needed for API calls.

## Step 3: Basic Usage (Simple Script)

### For quick testing without configuration:

1. Run the script:
   ```bash
   python rackbeat_valuation.py
   ```
2. When prompted with `Enter Rackbeat Bearer token:`, paste your token
3. Press Enter (the token input is hidden)

### What you'll see:
- A formatted table in the console showing location names and values
- A JSON file created: `rackbeat_valuations.json` with detailed data

---

## Step 4: Advanced Usage (With Configuration File)

For more control over output formats, filtering, and logging:

1. Copy the example configuration:
   ```bash
   cp config.ini.example config.ini
   ```
   (On Windows: use `copy config.ini.example config.ini`)

2. Optional: Edit `config.ini` and add your API key if you do not want to be prompted every run:
   ```ini
   [rackbeat]
   api_key = YOUR_API_KEY_HERE
   ```

3. Customize other settings as needed:
   ```ini
   # Output format: json, csv, or both
   format = both
   
   # Filter to specific locations (optional)
   filter_locations = 1004, 1003
   ```

4. Run the advanced script:
   ```bash
   python rackbeat_valuation_advanced.py
   ```

### Available configuration options:

| Section | Key | Description | Example |
|---------|-----|-------------|---------|
| rackbeat | api_key | Your Rackbeat Bearer token | YOUR_KEY |
| rackbeat | date_to | Report date (YYYY-MM-DD) | 2024-05-08 |
| output | format | Output format | json, csv, or both |
| output | output_directory | Where to save files | ./reports |
| locations | filter_locations | Only process these locations | 1004, 1003 |
| locations | exclude_locations | Skip these locations | 1005, 1006 |
| logging | log_level | Debug verbosity | INFO, DEBUG, WARNING |
| logging | log_file | Log file path | rackbeat_valuation.log |

---

## Step 5: Understanding the Output

### Console Output Shows:

```
📍 Lager Sjælland (Location #1004)
------------------------------------------------------------
  Main Location Value:      50,000.00

  Sub-Locations:
      • Lager A........................  25,000.00
      • Lager B........................  15,000.00

  TOTAL (incl. sub-locations)................ 95,000.00
```

### JSON File Contains:
- All location data with full details
- Item-level breakdown (if enabled)
- Timestamp and date of report
- Grand total value

### CSV File Contains:
- Simple tabular format
- One row per location
- Suitable for Excel/spreadsheet import

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
**Solution:** Run `pip install -r requirements.txt` again

### "ERROR: Bearer token is required"
**Solution:** 
- Run the script again
- Paste a valid Rackbeat Bearer token when prompted

### "Authorization Failed"
**Solution:**
- Verify your Bearer token is correct
- Check it hasn't expired in your Rackbeat account settings
- Ensure API access is enabled for your user

### "No locations found"
**Solution:**
- Your account might have no locations set up
- Check filter settings in config.ini
- Verify you have permission to view locations

### Script is slow
**Solution:**
- This is normal with many locations due to API calls
- Each location requires a separate API request
- Run during off-peak hours for better performance

---

## Common Tasks

### Export only specific locations:

Edit `config.ini`:
```ini
[locations]
filter_locations = 1004, 1003, 1002
```

### Get valuation as of a specific date:

Edit `config.ini`:
```ini
[rackbeat]
date_to = 2024-05-08
```

### Generate CSV only (not JSON):

Edit `config.ini`:
```ini
[output]
format = csv
```

### Save reports to a specific folder:

Edit `config.ini`:
```ini
[output]
output_directory = C:/Reports/Rackbeat
```

---

## Next Steps

1. **Test with basic script first** - `python rackbeat_valuation.py`
2. **Configure advanced script** - Copy and edit `config.ini`
3. **Set up automated runs** - Use cron (Linux) or Task Scheduler (Windows)
4. **Integrate with other systems** - Parse the JSON output in your tools

---

## Getting Help

### Documentation:
- [Rackbeat API Docs](https://developer.rackbeat.com/)
- [README.md](README.md) - Full documentation
- Check console error messages - they're usually helpful!

### For Issues:
1. Check the troubleshooting section above
2. Review the error message in detail
3. Check your API key is correct
4. Verify your internet connection
5. Contact Rackbeat support if API-related

---

**Enjoy!** 🚀

The script handles complex location hierarchies automatically - just add your API key and run it!
