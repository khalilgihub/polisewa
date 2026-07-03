#!/usr/bin/env python3
"""
Plus Code to Coordinate Converter
Converts Full or Short Plus Codes (Open Location Codes) to geographic coordinates.
"""

import sys
import argparse
import urllib.request
import urllib.parse
import json
import ssl
import re
import openlocationcode.openlocationcode as openlocationcode

def geocode_reference(address):
    """
    Geocodes a reference address/locality to retrieve its latitude and longitude.
    Uses OpenStreetMap Nominatim API, matching the setup in get_boundary.py.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(address) + "&format=json&limit=1&email=abdul.polisewa@outlook.com"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'PolisewaMapApp/1.0 (abdul.polisewa@outlook.com)'
        }
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            res_data = response.read().decode('utf-8')
            data = json.loads(res_data)
            if data:
                item = data[0]
                return float(item.get('lat')), float(item.get('lon')), item.get('display_name')
    except Exception as e:
        raise RuntimeError(f"Geocoding request failed for reference '{address}': {e}")
    
    return None

def extract_plus_code_and_reference(text):
    """
    Extracts the plus code token (containing '+') and the reference address from the input string.
    Returns (plus_code, reference_address).
    """
    tokens = text.split()
    plus_code_token = None
    
    for token in tokens:
        # Clean token from common punctuation at the ends (like commas, semicolons)
        clean_token = token.strip(',;')
        if '+' in clean_token:
            plus_code_token = clean_token
            break
            
    if plus_code_token:
        # Extract everything else as reference address
        # Replace the first occurrence of plus_code_token (or its uncleaned version) in text
        # to preserve commas and formatting of the rest
        ref_text = text.replace(plus_code_token, '').strip(', ')
        # Clean up punctuation and spacing
        ref_text = re.sub(r'^[\s,]+|[\s,]+$', '', ref_text)
        ref_text = re.sub(r'\s*,\s*', ', ', ref_text)
        
        # Remove trailing/leading comma/punctuation on plus_code_token itself
        plus_code_token = plus_code_token.strip(',;')
        return plus_code_token.upper(), ref_text
        
    return None, text

def convert_plus_code(input_str):
    """
    Main logic to convert a plus code input (full or short + reference) to coordinates.
    """
    plus_code, reference = extract_plus_code_and_reference(input_str)
    
    if not plus_code:
        raise ValueError("No Plus Code (containing '+') found in the input.")
        
    # Check if the plus code itself is valid Open Location Code
    if not openlocationcode.isValid(plus_code):
        raise ValueError(f"'{plus_code}' is not a valid Open Location Code.")
        
    # If it is a full plus code, decode it directly
    if openlocationcode.isFull(plus_code):
        decoded = openlocationcode.decode(plus_code)
        return {
            "plus_code": plus_code,
            "type": "full",
            "latitude": decoded.latitudeCenter,
            "longitude": decoded.longitudeCenter,
            "latitude_bounds": [decoded.latitudeLo, decoded.latitudeHi],
            "longitude_bounds": [decoded.longitudeLo, decoded.longitudeHi],
            "reference_used": None,
            "resolved_reference_display": None
        }
        
    # If it is a short code, we need a reference locality
    if openlocationcode.isShort(plus_code):
        if not reference:
            raise ValueError(f"'{plus_code}' is a short Plus Code and requires a reference locality (e.g. 'MPVW+MX, Kuching').")
            
        # Geocode reference locality to get reference lat/lon
        geo_result = geocode_reference(reference)
        if not geo_result:
            raise ValueError(f"Could not geocode the reference locality: '{reference}'")
            
        ref_lat, ref_lon, ref_display = geo_result
        
        # Recover full OLC using reference coordinates
        full_code = openlocationcode.recoverNearest(plus_code, ref_lat, ref_lon)
        
        # Decode the recovered full code
        decoded = openlocationcode.decode(full_code)
        return {
            "plus_code": plus_code,
            "full_plus_code": full_code,
            "type": "short",
            "latitude": decoded.latitudeCenter,
            "longitude": decoded.longitudeCenter,
            "latitude_bounds": [decoded.latitudeLo, decoded.latitudeHi],
            "longitude_bounds": [decoded.longitudeLo, decoded.longitudeHi],
            "reference_used": reference,
            "resolved_reference_display": ref_display,
            "reference_coordinates": [ref_lat, ref_lon]
        }
        
    raise ValueError(f"Plus Code '{plus_code}' is neither a valid full nor short code.")

def print_result(result, use_json):
    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 50)
        print("PLUS CODE RESOLVED SUCCESSFULLY")
        print("=" * 50)
        print(f"Input Plus Code: {result['plus_code']}")
        if result['type'] == 'short':
            print(f"Short Code Type: Resolved via reference")
            print(f"Reference Query: {result['reference_used']}")
            print(f"Resolved Ref:    {result['resolved_reference_display']}")
            print(f"Ref Coordinates: Lat {result['reference_coordinates'][0]:.6f}, Lon {result['reference_coordinates'][1]:.6f}")
            print(f"Full Plus Code:  {result['full_plus_code']}")
        else:
            print(f"Code Type:       Full (Absolute)")
        
        print("-" * 50)
        print(f"Latitude:        {result['latitude']:.6f}")
        print(f"Longitude:       {result['longitude']:.6f}")
        print(f"Lat Bounds:      [{result['latitude_bounds'][0]:.6f}, {result['latitude_bounds'][1]:.6f}]")
        print(f"Lon Bounds:      [{result['longitude_bounds'][0]:.6f}, {result['longitude_bounds'][1]:.6f}]")
        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Plus Code (Open Location Code) to latitude and longitude coordinates. "
                    "Supports full plus codes, or short plus codes with reference location."
    )
    parser.add_argument(
        "input",
        nargs="*",
        help="The Plus Code to convert (e.g., '8Q7XMPVW+MX' or 'MPVW+MX, Kuching')."
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output the result in raw JSON format (useful for scripting/integration)."
    )
    
    args = parser.parse_args()
    
    # If arguments are provided on command line, run once and exit
    if args.input:
        input_str = " ".join(args.input)
        try:
            result = convert_plus_code(input_str)
            print_result(result, args.json)
        except Exception as e:
            if args.json:
                print(json.dumps({"error": str(e)}), file=sys.stderr)
            else:
                print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Otherwise, enter an interactive loop
    if not args.json:
        print("Entering interactive mode. Press Ctrl+C or type 'exit'/'quit' to exit.")
        
    while True:
        try:
            user_input = input("\nEnter Plus Code (e.g. '8Q7XMPVW+MX' or 'MPVW+MX, Kuching'): ").strip()
            if not user_input:
                continue
            if user_input.lower() in ('exit', 'quit'):
                break
                
            result = convert_plus_code(user_input)
            print_result(result, args.json)
        except (KeyboardInterrupt, EOFError):
            if not args.json:
                print("\nExiting interactive mode.")
            break
        except Exception as e:
            if args.json:
                print(json.dumps({"error": str(e)}), file=sys.stderr)
            else:
                print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
