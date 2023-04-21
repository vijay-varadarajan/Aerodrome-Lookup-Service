from project import (
    get_country_code,
    get_airports_country,
    get_region_code,
    get_airports_region,
    get_airports_city,
    search,
)
import pytest


def test_get_country_code():
    assert get_country_code("India") == ("IN", "India")
    assert get_country_code("IN") == ("IN", "India")
    assert get_country_code("  Un it ed St at es") == ("US", "United States")
    assert get_country_code(" america  ") == ("US", "United States")
    assert get_country_code("Lithu") == ("LT", "Lithuania")
    assert get_country_code("abcd ") == (None, None)
    assert get_country_code("1234") == (None, None)


def test_get_airports_country():
    assert get_airports_country(" US") == 29409
    assert get_airports_country("us  ") == 29409
    assert get_airports_country("IN") == 582
    assert get_airports_country("Lt") == 68
    assert get_airports_country("LT") == 68
    assert get_airports_country("12") == 0


def test_get_region_code():
    assert get_region_code("Washington ", "US") == ("US-WA", "Washington")
    assert get_region_code("  Tamilnadu", "IN") == ("IN-TN", "Tamil Nadu")
    assert get_region_code("taM i l naDU", "IN") == ("IN-TN", "Tamil Nadu")
    assert get_region_code("kaunas ", "LT") == ("LT-KU", "Kaunas County")
    assert get_region_code("Washington", "IN") == (None, None)
    assert get_region_code("123abc", "US") == (None, None)


def test_get_airports_region():
    assert get_airports_region("IN-TN") == 31
    assert get_airports_region("in-tN") == 31
    assert get_airports_region("US-WA") == 689
    assert get_airports_region("LT-ku") == 10
    assert get_airports_region("2345") == 0
    assert get_airports_region(None) == 0


def test_get_airports_final():
    assert get_airports_city("Lt-ku", " Kaunas  ") == [
        {
            "name": "Kaunas International Airport",
            "type": "medium_airport",
            "gps code": "EYKA",
        },
        {"name": "Kaunas Gamykla Airfield", "type": "closed", "gps code": "EYKG"},
        {
            "name": "S. Darius and S. GirÄ—nas Airfield",
            "type": "small_airport",
            "gps code": "EYKS",
        },
    ]

    assert get_airports_city("IN-TN", "C H e n n A I") == [
        {
            "name": "Chennai Military Hospital Helipad",
            "type": "heliport",
            "gps code": "",
        },
        {
            "name": "Chennai International Airport",
            "type": "large_airport",
            "gps code": "VOMM",
        },
        {
            "name": "Tambaram Air Force Station",
            "type": "small_airport",
            "gps code": "VOTX",
        },
    ]

    assert get_airports_city("US-DE", "Christiana") == [
        {"name": "Eagle Run Heliport", "type": "closed", "gps code": ""}
    ]

    assert get_airports_city("US-DE", "123abc") == None
    assert get_airports_city("IN-tn", "Seattle") == None
    assert get_airports_city("Delaware", " Christiana ") == None
