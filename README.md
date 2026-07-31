# Lot Code Decoder
A Python command-line tool for decoding product lot codes used in the IPPS system. Given a brand name, form submission date, and lot code, the tool returns the manufacturer, production date, manufacturing plant, and product age.

---

## Supported Manufacturers
| Manufacturer | Example Brands |
|---|---|
| Procter & Gamble | Bounty, Charmin, Puffs |
| Georgia Pacific | Sparkle, Angel Soft, Brawny |
| Kimberly-Clark | Kleenex, Scott, Cottonelle, Huggies, Kotex |

---

## How It Works

### P&G Lot Codes
P&G lot codes encode the year, Julian date, and plant identifier.

Example: `5116CCB03`
- `5` → 2025
- `116` → Julian day 116 = April 26th
- `C` → Cape Girardeau plant

Some P&G codes have an extra digit between the date and the plant letters (e.g. `60176AYG16`). The decoder skips any leading non-letter characters before matching the plant identifier, so this still resolves correctly to Albany.

**Known P&G plant codes:**
| Code | Plant |
|---|---|
| `U019` | Oxnard |
| `U017` | Cape Girardeau |
| `U020` | Green Bay |
| `U011` | Mehoopany |
| `U018` | Albany |
| `4555` | Box Elder |
| `XX` | Oxnard |
| `BE` | Box Elder |
| `GB` | Green Bay |
| `C` | Cape Girardeau |
| `M` | Mehoopany |
| `A` | Albany |

**Known P&G brands:**
`bounty`, `charmin`, `puffs`, `vicks`, `tide`, `pampers`

### Georgia Pacific Lot Codes
Georgia Pacific lot codes encode the date in MM/DD/YY format followed by a plant identifier.

Example: `043025 MSKT2501552`
- `043025` → April 30, 2025
- `MSK` → Muskogee plant

**Known Georgia Pacific plant codes:**
| Code | Plant |
|---|---|
| `PAL` | Palatka |
| `CRO` | Crossett |
| `SAV` | Savannah |
| `NAH` | Naheola |
| `PLT` | Plattsburgh |
| `PTH` | Port Hudson |
| `COP` | COP (Unknown) |
| `GB` | Green Bay |
| `HAL` | Halsey |
| `WAU` | Wauna |
| `MSK` | Muskogee |

**Known Georgia Pacific brands:**
`sparkle`, `angel soft`, `quilted northern`, `brawny`, `dixie`, `vanity fair`

### Kimberly-Clark Lot Codes
Kimberly-Clark codes start with one or more plant letters, followed by a year and Julian date. There are three sub-formats:

**Standard, single-digit year**
Example: `MT6045`
- `MT` → Marinette plant
- `6` → 2026
- `045` → Julian day 45 = February 14th

**Standard, two-digit year**
Used when the year digits would otherwise start with `2` or `3` (to avoid ambiguity with the single-digit format). This convention holds through 2029; it will need to be revisited once single-digit years reach 2030+.

Example: `MO26045`
- `MO` → Mobile plant
- `26` → 2026
- `045` → Julian day 45 = February 14th

Extra trailing characters after the Julian day (e.g. a shift or line code) are ignored. Internal spaces anywhere in the code (e.g. `CE26 082 03 15:29`) are also stripped out before parsing, so formatting inconsistencies don't break decoding.

**Mexico format**
Mexico-produced codes use a `DD/MM/YY` date format instead of a Julian date, and may include additional space-separated codes that are ignored.

Example: `RA LHA 23/11/25`
- `R` → Mexico plant (the rest of the leading letters, like the trailing `A` in `RA`, and any other tokens like `LHA`, are ignored)
- `23/11/25` → November 23, 2025 (day/month/year order)

**Known Kimberly-Clark plant codes:**
| Code | Plant |
|---|---|
| `MO` | Mobile |
| `MT` | Marinette |
| `C` | Chester |
| `H` | Canada |
| `R` | Mexico |
| `B` | Beach Island |
| `J` | Jenks |

**Known Kimberly-Clark brands:**
`kleenex`, `scott`, `cottonelle`, `viva`, `huggies`, `pull-ups`, `goodnites`, `poise`, `depend`, `kotex`

---

## Testing with the Command Line Interface
Run the interactive CLI:
```
python lot_code_decoder.py
```
You will be prompted to enter:
1. Brand name (e.g. `Bounty`, `Sparkle`, `Kleenex`)
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
    "kleenex":   "Kimberly-Clark",
    "your brand": "Manufacturer Name",  # add here
    ...
}
```

## Adding New Plants
Each manufacturer has its own plant lookup near the top of the file (`PG_PLANTS`, `GP_PLANTS`, `KC_PLANTS`). Add new plant identifiers there:
- `PG_PLANTS` and `KC_PLANTS` are ordered lists of `(identifier, plant_name)` tuples — list longer/more specific identifiers before shorter ones that could be a false-match prefix (e.g. `"MO"` before a hypothetical bare `"M"`).
- `GP_PLANTS` is a simple dictionary, since GP identifiers don't have that prefix-collision risk.

---

## Requirements
- Python 3.10 or newer
- No external libraries required — uses only the Python standard library
