from copy import deepcopy
from scripts.load_elasticsearch import (create_address,
                                        add_building_name,
                                        add_postcode,
                                        add_locality,
                                        add_street_details,
                                        add_number_details,
                                        add_level_details,
                                        add_flat_details,
                                        )


ROW_FIELDS = [
    "BUILDING_NAME",
    "FLAT_TYPE_CODE",
    "FLAT_NUMBER_PREFIX",
    "FLAT_NUMBER",
    "FLAT_NUMBER_SUFFIX",
    "LEVEL_TYPE_CODE",
    "LEVEL_NUMBER_PREFIX",
    "LEVEL_NUMBER",
    "LEVEL_NUMBER_SUFFIX",
    "NUMBER_FIRST_PREFIX",
    "NUMBER_FIRST",
    "NUMBER_FIRST_SUFFIX",
    "NUMBER_LAST_PREFIX",
    "NUMBER_LAST",
    "NUMBER_LAST_SUFFIX",
    "STREET_NAME",
    "STREET_TYPE_CODE",
    "LOCALITY_NAME",
    "POSTCODE",
]
ROW_RECORD = {key: "" for key in ROW_FIELDS}


def make_row_and_address_components():
    return deepcopy(ROW_RECORD), []


def test_empty_create_address():
    row, _ = make_row_and_address_components()
    assert create_address(row) == ""


def test_create_address():
    expected = "BUILDING, U A12B L C34D E123F-G78H FAKE STREET, SPRINGFIELD, 2000"
    row, _ = make_row_and_address_components()

    row["BUILDING_NAME"] = "BUILDING"
    row["FLAT_TYPE_CODE"] = "U"
    row["FLAT_NUMBER_PREFIX"] = "A"
    row["FLAT_NUMBER"] = 12
    row["FLAT_NUMBER_SUFFIX"] = "B"
    row["LEVEL_TYPE_CODE"] = "L"
    row["LEVEL_NUMBER_PREFIX"] = "C"
    row["LEVEL_NUMBER"] = 34
    row["LEVEL_NUMBER_SUFFIX"] = "D"
    row["NUMBER_FIRST_PREFIX"] = "E"
    row["NUMBER_FIRST"] = 123
    row["NUMBER_FIRST_SUFFIX"] = "F"
    row["NUMBER_LAST_PREFIX"] = "G"
    row["NUMBER_LAST"] = 78
    row["NUMBER_LAST_SUFFIX"] = "H"
    row["STREET_NAME"] = "FAKE"
    row["STREET_TYPE_CODE"] = "STREET"
    row["LOCALITY_NAME"] = "SPRINGFIELD"
    row["POSTCODE"] = 2000
    actual = create_address(row)
    print(actual)
    assert actual == expected


def test_add_empty_building_name():
    row, address_components = make_row_and_address_components()
    add_building_name(row, address_components)
    assert "".join(address_components) == ""


def test_add_building_name():
    row, address_components = make_row_and_address_components()
    building_name = "some building name"
    row["BUILDING_NAME"] = building_name
    add_building_name(row, address_components)
    assert "".join(address_components) == building_name + ", "


def test_add_empty_flat_details():
    row, address_components = make_row_and_address_components()
    add_flat_details(row, address_components)
    assert "".join(address_components) == ""


def test_add_flat_details():
    row, address_components = make_row_and_address_components()
    row["FLAT_TYPE_CODE"] = "U"
    row["FLAT_NUMBER_PREFIX"] = "B"
    row["FLAT_NUMBER"] = 12
    row["FLAT_NUMBER_SUFFIX"] = "C"
    add_flat_details(row, address_components)
    assert "".join(address_components) == "U B12C "


def test_add_empty_level_details():
    row, address_components = make_row_and_address_components()
    add_level_details(row, address_components)
    assert "".join(address_components) == ""


def test_add_level_details():
    row, address_components = make_row_and_address_components()
    row["LEVEL_TYPE_CODE"] = "L"
    row["LEVEL_NUMBER_PREFIX"] = "B"
    row["LEVEL_NUMBER"] = 81
    row["LEVEL_NUMBER_SUFFIX"] = "C"
    add_level_details(row, address_components)
    assert "".join(address_components) == "L B81C "


def test_add_empty_number_details():
    row, address_components = make_row_and_address_components()
    add_number_details(row, address_components)
    assert "".join(address_components) == ""


def test_add_fist_number_only():
    row, address_components = make_row_and_address_components()
    row["NUMBER_FIRST_PREFIX"] = "A"
    row["NUMBER_FIRST"] = 12
    row["NUMBER_FIRST_SUFFIX"] = "B"
    add_number_details(row, address_components)
    assert "".join(address_components) == "A12B "


def test_add_number_details():
    row, address_components = make_row_and_address_components()
    row["NUMBER_FIRST_PREFIX"] = "A"
    row["NUMBER_FIRST"] = 12
    row["NUMBER_FIRST_SUFFIX"] = "B"
    row["NUMBER_LAST_PREFIX"] = "C"
    row["NUMBER_LAST"] = 34
    row["NUMBER_LAST_SUFFIX"] = "D"
    add_number_details(row, address_components)
    assert "".join(address_components) == "A12B-C34D "


def test_add_empty_street_details():
    row, address_components = make_row_and_address_components()
    add_street_details(row, address_components)
    assert "".join(address_components) == ""


def test_add_street_details():
    row, address_components = make_row_and_address_components()
    row["STREET_NAME"] = "FAKE"
    row["STREET_TYPE_CODE"] = "STREET"
    add_street_details(row, address_components)
    assert "".join(address_components) == "FAKE STREET, "


def test_add_empty_locality():
    row, address_components = make_row_and_address_components()
    add_locality(row, address_components)
    assert "".join(address_components) == ""


def test_add_locality():
    row, address_components = make_row_and_address_components()
    row["LOCALITY_NAME"] = "SPRINGFIELD"
    add_locality(row, address_components)
    assert "".join(address_components) == "SPRINGFIELD, "


def test_add_empty_postcode():
    row, address_components = make_row_and_address_components()
    add_postcode(row, address_components)
    assert "".join(address_components) == ""


def test_add_non_numeric_postcode():
    row, address_components = make_row_and_address_components()
    row["POSTCODE"] = "hello"
    add_postcode(row, address_components)
    assert "".join(address_components) == ""


def test_postcode_postcode():
    row, address_components = make_row_and_address_components()
    row["POSTCODE"] = 2000
    add_postcode(row, address_components)
    assert "".join(address_components) == "2000"
