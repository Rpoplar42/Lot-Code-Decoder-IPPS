"""
Lot Code Decoder for IPPS
Supports: Procter & Gamble (P&G) and Georgia Pacific (GP)

"""

from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Brand → Manufacturer mapping
# Dictionary to map the brands to the manufacturers 
# ---------------------------------------------------------------------------
BRAND_TO_MANUFACTURER = {
    # P&G brands
    "bounty":       "P&G",
    "charmin":      "P&G",
    "puffs":        "P&G",
    "vicks":        "P&G",
    "tide":         "P&G",
    "pampers":      "P&G",
    # Georgia Pacific brands
    "sparkle":      "Georgia Pacific",
    "angel soft":   "Georgia Pacific",
    "quilted northern": "Georgia Pacific",
    "brawny":       "Georgia Pacific",
    "dixie":        "Georgia Pacific",
    "vanity fair":  "Georgia Pacific",
}

# ---------------------------------------------------------------------------
# P&G plant identifiers (longer codes checked first to avoid partial matches)
# Simple Dictionary composed of tuples that can be expanded with more plants
# ---------------------------------------------------------------------------
PG_PLANTS = [
    ("U019", "Oxnard"),
    ("U017", "Cape Girardeau"),
    ("U020", "Green Bay"),
    ("U011", "Mehoopany"),
    ("U018", "Albany"),
    ("4555", "Box Elder"),
    ("XX",   "Oxnard"),
    ("BE",   "Box Elder"),
    ("GB",   "Green Bay"),
    ("C",    "Cape Girardeau"),
    ("M",    "Mehoopany"),
    ("A",    "Albany"),
]

# ---------------------------------------------------------------------------
# Georgia Pacific plant identifiers
# Simple dictionary with plants matched to identifiers for GP
# ---------------------------------------------------------------------------
GP_PLANTS = {
    "PAL": "Palatka",
    "CRO": "Crossett",
    "SAV": "Savannah",
    "NAH": "Naheola",
    "PLT": "Plattsburgh",
    "PTH": "Port Hudson",
    "COP": "COP (Unknown)",
    "GB":  "Green Bay",
    "HAL": "Halsey",
    "WAU": "Wauna",
    "MSK": "Muskogee",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_manufacturer(brand: str) -> str | None:
    return BRAND_TO_MANUFACTURER.get(brand.strip().lower())


def _age_string(produced: datetime, reference: datetime) -> str:
    delta = reference - produced
    days = delta.days
    if days < 0:
        return f"{abs(days)} day(s) in the future"
    if days == 0:
        return "produced today"
    weeks, rem = divmod(days, 7)
    if days < 7:
        return f"{days} day(s) old"
    if weeks < 8:
        return f"{weeks} week(s), {rem} day(s) old"
    months = days // 30
    return f"~{months} month(s) old ({days} days)"


# ---------------------------------------------------------------------------
# P&G decoder, takes in the lot code and the reference date
# ---------------------------------------------------------------------------
def decode_pg(lot_code: str, reference_date: datetime) -> dict:
    code = lot_code.strip()

    if len(code) < 4:
        raise ValueError(f"P&G lot code too short: '{lot_code}'")

    # Year: first digit
    year_digit = code[0]
    if not year_digit.isdigit():
        raise ValueError(f"Expected digit for year, got '{year_digit}'")
    year = 2020 + int(year_digit)  # 4→2024, 5→2025, etc.

    # Julian date: next 3 digits
    julian_str = code[1:4]
    if not julian_str.isdigit():
        raise ValueError(f"Expected 3-digit Julian date, got '{julian_str}'")
    julian_day = int(julian_str)
    produced = datetime(year, 1, 1) + timedelta(days=julian_day - 1)

    # Plant: remaining characters — try each identifier in order
    remainder = code[4:]
    plant = None
    for identifier, plant_name in PG_PLANTS:
        if remainder.startswith(identifier):
            plant = plant_name
            break

    if plant is None:
        plant = f"Unknown ('{remainder}')"

    return {
        "manufacturer": "Procter & Gamble",
        "lot_code": lot_code,
        "date_produced": produced.strftime("%B %d, %Y"),
        "plant": plant,
        "age": _age_string(produced, reference_date),
    }


# ---------------------------------------------------------------------------
# Georgia Pacific decoder
# ---------------------------------------------------------------------------

def decode_gp(lot_code: str, reference_date: datetime) -> dict:
    # Strip spaces for parsing but keep original for display
    code = lot_code.replace(" ", "")

    if len(code) < 6:
        raise ValueError(f"GP lot code too short: '{lot_code}'")

    # Date: first 6 digits — MMDDYY
    date_str = code[:6]
    if not date_str.isdigit():
        raise ValueError(f"Expected 6-digit date (MMDDYY), got '{date_str}'")
    produced = datetime.strptime(date_str, "%m%d%y")

    # Plant: next 2–3 letters
    remainder = code[6:].upper()
    plant = None
    # Try 3-letter codes first, then 2-letter
    for length in (3, 2):
        candidate = remainder[:length]
        if candidate in GP_PLANTS:
            plant = GP_PLANTS[candidate]
            break

    if plant is None:
        plant = f"Unknown ('{remainder[:3]}')"

    return {
        "manufacturer": "Georgia Pacific",
        "lot_code": lot_code,
        "date_produced": produced.strftime("%B %d, %Y"),
        "plant": plant,
        "age": _age_string(produced, reference_date),
    }


# ---------------------------------------------------------------------------
# Main public interface
# ---------------------------------------------------------------------------

def decode(brand: str, reference_date_str: str, lot_code: str) -> dict: 
    manufacturer = get_manufacturer(brand)
    if manufacturer is None:
        raise ValueError(
            f"Unknown brand '{brand}'. Add it to BRAND_TO_MANUFACTURER or "
            "specify the manufacturer directly."
        )

    try:
        reference_date = datetime.strptime(reference_date_str.strip(), "%m/%d/%Y")
    except ValueError:
        raise ValueError(
            f"Invalid reference date '{reference_date_str}'. Use MM/DD/YYYY format."
        )

    if manufacturer == "P&G":
        return decode_pg(lot_code, reference_date)
    elif manufacturer == "Georgia Pacific":
        return decode_gp(lot_code, reference_date)
    else:
        raise ValueError(f"No decoder implemented for manufacturer '{manufacturer}'")


def print_result(result: dict) -> None:
    """Pretty-print a decode result."""
    print("-" * 40)
    for key, value in result.items():
        label = key.replace("_", " ").title()
        print(f"  {label:<18} {value}")
    print("-" * 40)


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------

KNOWN_BRANDS = sorted(BRAND_TO_MANUFACTURER.keys())

def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"  {label}{suffix}: ").strip()
    return value if value else default


def cli():
    print("\n" + "=" * 50)
    print("  IPPS Lot Code Decoder")
    print("=" * 50)
    print(f"  Known brands: {', '.join(KNOWN_BRANDS)}")
    print("  Type 'quit' or 'q' at any prompt to exit.")
    print("  Press Enter with no input to re-use the last reference date.")
    print("=" * 50)

    last_date = datetime.today().strftime("%m/%d/%Y")

    while True:
        print()

        # Brand
        brand = prompt("Brand")
        if brand.lower() in ("quit", "q", ""):
            break

        # Reference date (default = last used or today)
        date_input = prompt("Reference date (MM/DD/YYYY)", default=last_date)
        if date_input.lower() in ("quit", "q"):
            break
        last_date = date_input  # remember for next round

        # Lot code
        lot_code = prompt("Lot code")
        if lot_code.lower() in ("quit", "q", ""):
            break

        # Decode
        try:
            result = decode(brand, last_date, lot_code)
            print()
            print_result(result)
        except ValueError as e:
            print(f"\n  ⚠  Error: {e}")

        # Ask to decode another code for the same brand/date
        while True:
            another = input("\n  Decode another lot code for the same brand & date? (y/n): ").strip().lower()
            if another == "y":
                lot_code = prompt("Lot code")
                if lot_code.lower() in ("quit", "q", ""):
                    break
                try:
                    result = decode(brand, last_date, lot_code)
                    print()
                    print_result(result)
                except ValueError as e:
                    print(f"\n  ⚠  Error: {e}")
            else:
                break

    print("\n  Goodbye!\n")


if __name__ == "__main__":
    cli()
