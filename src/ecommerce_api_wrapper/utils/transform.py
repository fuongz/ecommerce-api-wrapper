import re


def remove_alphabets_regex(input_string):
    return re.sub(r"[a-zA-Z]", "", input_string)


def convert_to_number(s: str) -> int:
    if not s:
        return 0
    s = s.strip().upper()
    number_part = ""
    multiplier = 1

    for char in s:
        if char.isdigit() or char == ".":
            number_part += char
        elif char == "K":
            multiplier = 1_000
            break
        elif char == "M":
            multiplier = 1_000_000
            break
        elif char == "B":
            multiplier = 1_000_000_000
            break

    if not number_part:
        return 0

    return int(float(number_part) * multiplier)


def calculate_discount(price, original_price):
    if original_price is None:
        return 0
    return round((original_price - price) / original_price * 100, 2)


def convert_string_to_slug(input_string: str, separator="-") -> str:
    return input_string.lower().replace(" ", separator)


def is_valid_rp_jt_format(currency_string):
    """
    Checks if a string matches the format 'Rp[digits],[digits]jt'
    or 'Rp[digits]jt'.

    Examples of valid formats:
    'Rp29,9jt'
    'Rp10jt'
    'Rp0,5jt'
    'Rp123,456jt'
    'Rp123jt'

    Args:
      currency_string: The string to validate.

    Returns:
      True if the string matches the format, False otherwise.
    """
    # Regex pattern:
    # ^          - Start of the string
    # Rp         - Matches the literal characters 'Rp' (case-sensitive)
    # \d+        - Matches one or more digits (0-9) for the main number part
    # (?:,\d+)?  - Optional non-capturing group for the decimal part:
    #    ,       -   Matches a literal comma
    #    \d+     -   Matches one or more digits after the comma
    # jt         - Matches the literal characters 'jt' (case-insensitive due to re.IGNORECASE)
    # $          - End of the string
    pattern = r"^Rp\d+(?:,\d+)?jt$"

    # re.match() checks for a match only at the beginning of the string.
    # re.IGNORECASE makes 'jt' match 'JT', 'Jt', etc.
    if re.match(pattern, currency_string, re.IGNORECASE):
        return True
    else:
        return False


def convert_currency_string_to_int(currency_string):
    if not currency_string and currency_string == "":
        return None

    if is_valid_rp_jt_format(currency_string):
        cleaned_string = currency_string.replace("Rp", "").strip()
        if cleaned_string.lower().endswith("jt"):
            numeric_part_str = cleaned_string[:-2].replace(",", ".")
            try:
                # Convert to float and multiply by 1 million
                value_in_millions = float(numeric_part_str)
                return value_in_millions * 1_000_000
            except ValueError:
                print(
                    f"Error: Could not parse numeric part '{numeric_part_str}' from '{currency_string}'."
                )
                return None

    # Remove non-numeric character
    numeric_string = remove_alphabets_regex(currency_string)

    # Remove dot thousands separators
    numeric_string = numeric_string.replace(".", "")

    # Remove comma separators
    numeric_string = numeric_string.replace(",", ".")

    try:
        # Convert the cleaned string to an integer
        return int(numeric_string)
    except ValueError:
        # Handle cases where the string might not be a valid number after cleaning
        print(
            f"Error: Could not convert '{currency_string}' to an integer. Invalid format."
        )
        return None


def convert_rb_string_to_numeric(rb_string):
    if not rb_string and rb_string == "":
        return None
    # Remove the '+' character if present
    cleaned_string = rb_string.split(" ")[0].replace("+", "")

    # Use regex to find a number followed by 'rb' (case-insensitive)
    match = re.match(r"(\d+)rb", cleaned_string, re.IGNORECASE)

    if match:
        # Extract the numeric part (e.g., '1', '5')
        numeric_part = int(match.group(1))
        # Multiply by 1000 as 'rb' represents 'thousand'
        return numeric_part * 1000
    else:
        try:
            # Convert the cleaned string to an integer
            return int(cleaned_string)
        except ValueError:
            # Handle cases where the string might not be a valid number after cleaning
            print(
                f"Error: Could not convert '{rb_string}' to an integer. Invalid format."
            )
            return None
