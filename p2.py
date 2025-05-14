#!/usr/bin/env python3

class TextColor:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


print(f"{TextColor.RED}{TextColor.RESET}")
print(f"{TextColor.BLUE} + -- --=[{TextColor.RED} simple.osint.builds v1.1.2 {TextColor.BLUE}   ]{TextColor.RESET}")
print(f"{TextColor.BLUE} + -- --=[{TextColor.RED} https://github.com/ghoste9624 {TextColor.BLUE}]{TextColor.RESET}")
print(f"{TextColor.BLUE} + -- --=[{TextColor.GREEN} phone.number.parser{TextColor.BLUE}           ]{TextColor.RESET}")
print(f"{TextColor.RED}{TextColor.RESET}")
italic_start = '\x1B[3m'
italic_end = '\x1B[0m'
text = "" + italic_start + "       country code (phone number)" + italic_end + ""
print(text)
print(f"{TextColor.RED}{TextColor.RESET}")
print(f"{TextColor.RED} {TextColor.RESET}")
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberFormat, parse
from geopy.geocoders import Nominatim

def parse_phone_number(phone_number_str, country_code=None):
    """Parses a phone number and attempts to get location info.

    Args:
        phone_number_str: The phone number as a string.
        country_code: Optional ISO 3166-1 alpha-2 country code (e.g., "US", "GB").

    Returns:
        A dictionary containing the extracted information or None if parsing fails.
    """
    try:
        # Parse the phone number
        phone_number = phonenumbers.parse(phone_number_str, country_code)

        # Get basic information
        country_code = phone_number.country_code
        national_number = phone_number.national_number

        # Validate the phone number
        is_valid = phonenumbers.is_valid_number(phone_number)

        # Get approximate location (country, region)
        region = geocoder.description_for_number(phone_number, "en")

        # Get location in English
        country = geocoder.country_name_for_number(phone_number, "en")

        # Get carrier (if available)
        phone_carrier = carrier.name_for_number(phone_number, "en")

        # Get timezone(s)
        timezones = timezone.time_zones_for_number(phone_number)

        # Attempt to get coordinates using geopy (requires a valid location)
        if region:
          geolocator = Nominatim(user_agent="phone_number_parser")
          location = geolocator.geocode(region)
          if location:
              latitude = location.latitude
              longitude = location.longitude
          else:
              latitude = None
              longitude = None
        else:
          latitude = None
          longitude = None

        return {
            "\033[36mpossible\033[32m": phonenumbers.is_possible_number(phone_number),
            "\033[36mvalid\033[32m": phonenumbers.is_valid_number(phone_number),
            "\033[36mnumber type\033[32m": phonenumbers.number_type(phone_number),
            "\033[36minternational\033[32m": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "\033[36mcountry code\033[32m": phone_number.country_code,
            "\033[36mnumber\033[32m": phone_number.national_number,
            "\033[36mnational\033[32m": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
            "\033[36mcountry\033[32m": country,
            "\033[36mtimezones\033[32m": timezone.time_zones_for_number(phone_number),
            "\033[36mlocation\033[32m": location,
            "\033[36mcarrier\033[32m": carrier.name_for_number(phone_number, "en"),
            "\033[36mlatitude\033[32m": latitude,
            "\033[36mlongitude\033[32m": longitude
        }

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"Error parsing phone number: {e}")
        return None

if __name__ == '__main__':
    phone_number_input = "+" + input("\033[36mEnter phone number\033[32m: ")
    result = parse_phone_number(phone_number_input)

    if result:
        print("\n\033[31mPhone Number Information:\n")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("Could not parse the phone number.")
