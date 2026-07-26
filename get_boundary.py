import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Address to geocode
address = "Kampung Sungai Atas Baru, Matang, Kuching, Sarawak"

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
            print("FOUND COORDINATES:")
            print("Lat:", item.get('lat'))
            print("Lon:", item.get('lon'))
            print("Display Name:", item.get('display_name'))
        else:
            # Try a broader search: just "Kampung Sungai Atas Baru"
            print("Specific search failed, trying broader...")
            url2 = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote("Kampung Sungai Atas Baru") + "&format=json&limit=1&email=abdul.polisewa@outlook.com"
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'PolisewaMapApp/1.0 (abdul.polisewa@outlook.com)'})
            with urllib.request.urlopen(req2, context=ctx, timeout=10) as response2:
                data2 = json.loads(response2.read().decode('utf-8'))
                if data2:
                    item2 = data2[0]
                    print("FOUND COORDINATES (broad):")
                    print("Lat:", item2.get('lat'))
                    print("Lon:", item2.get('lon'))
                    print("Display Name:", item2.get('display_name'))
                else:
                    # Fallback to SMK Agama Matang area which is nearby
                    print("Broader search failed, trying fallback to nearby landmark...")
                    url3 = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote("SMK Agama Matang") + "&format=json&limit=1&email=abdul.polisewa@outlook.com"
                    req3 = urllib.request.Request(url3, headers={'User-Agent': 'PolisewaMapApp/1.0 (abdul.polisewa@outlook.com)'})
                    with urllib.request.urlopen(req3, context=ctx, timeout=10) as response3:
                        data3 = json.loads(response3.read().decode('utf-8'))
                        if data3:
                            item3 = data3[0]
                            print("FOUND FALLBACK:")
                            print("Lat:", item3.get('lat'))
                            print("Lon:", item3.get('lon'))
                            print("Display Name:", item3.get('display_name'))
                        else:
                            print("All geocoding attempts failed.")
except Exception as e:
    print("Error:", e)
