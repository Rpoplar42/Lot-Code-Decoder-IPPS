# Lot Code Decoder

A Python command-line tool for decoding product lot codes used in the IPPS system. Given a brand name, form submission date, and lot code, the tool returns the manufacturer, production date, manufacturing plant, and product age.

---

## Supported Manufacturers

| Manufacturer | Example Brands |
|---|---|
| Procter & Gamble | Bounty, Charmin, Puffs |
| Georgia Pacific | Sparkle, Angel Soft, Brawny |
| Kimberly-Clark | *(in progress)* |

---

## How It Works

### P&G Lot Codes
P&G lot codes encode the year, Julian date, and plant identifier.

Example: `5116CCB03`
- `5` → 2025
- `116` → Julian day 116 = April 26th
- `C` → Cape Girardeau plant

### Georgia Pacific Lot Codes
Georgia Pacific lot codes encode the date in MM/DD/YY format followed by a plant identifier.

Example: `043025 MSKT2501552`
- `043025` → April 30, 2025
- `MSK` → Muskogee plant

---

## Testing with the Command Line Interface

Run the interactive CLI:

```
python lot_code_decoder.py
```

You will be prompted to enter:
1. Brand name (e.g. `Bounty`, `Sparkle`)
2. Reference date in MM/DD/YYYY format (defaults to today)
3. Lot code

Example output:
```
  Manufacturer       Procter & Gamble
  Lot Code           5116CCB03
  Date Produced      April 26, 2025
  Plant              Cape Girardeau
  Age                5 week(s), 6 day(s) old
```

You can decode multiple lot codes for the same brand and date without re-entering information each time.

---

## Adding New Brands

Open `lot_code_decoder.py` and add the brand to the `BRAND_TO_MANUFACTURER` dictionary at the top of the file:

```python
BRAND_TO_MANUFACTURER = {
    "bounty":    "P&G",
    "sparkle":   "Georgia Pacific",
    "your brand": "Manufacturer Name",  # add here
    ...
}
```

---

## Requirements

- Python 3.10 or newer
- No external libraries required — uses only the Python standard library
