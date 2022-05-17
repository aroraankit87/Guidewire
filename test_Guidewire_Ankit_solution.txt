import unittest
import io
import pytest
from Guidewire_Ankit_solution import validate_phone_number, format_phone_number, clean_data, process_data


class Test_Guidewire_Ankit_solution:
    # #This test validates phone numbers
    @pytest.mark.parametrize("number", [1234567890, 99887766554422, "99887766"])
    def test_validate_phone_number(self, number):
        # check for 10 digits number
        # check for 12 digits number
        # check for 8 digits number passed as string
        result = validate_phone_number(number)
        if len(str(number)) != 10:
            assert result == False
        else:
            assert result == True

    @pytest.mark.parametrize("number", ["1234567890", "(123)4567890", "(123)-456-7890"])
    def test_format_phone_number(self, number):
        # check for standard phone conversion
        # check for standard phone conversion when parenthesis are present
        # check for standard phone conversion where parenthesis and dashes are present
        result = format_phone_number(number)
        assert result == '123-456-7890'

    @pytest.mark.parametrize("number", [" 1234567890", "1234567890 ", "123 456 7890"])
    def test_clean_data(self, number):
        # check for spaces as a prefix in phone number
        # check for spaces as a suffix in phone number
        # check for spaces in the middle of the phone number
        result = clean_data(number)
        assert result == '123-456-7890'

    @pytest.mark.parametrize("csv_data", [b'Liptak, Quinton, (653)-889-7235, yellow, 70703',
                                          b'Quinton Liptak, yellow, 70703, 653 889 7235, ',
                                          b'Quinton, Liptak, 70703, 6538897235, yellow'])
    def test_process_data_errors(self, csv_data):
        # read_csv understands binary stream a well, use it to test subset of data instead of whole file.
        binaryStream = io.BytesIO(csv_data)
        results = process_data(binaryStream)
        assert len(results["errors"]) == 0
        # 1 Lastname, Firstname, (703)-742-0996, color, zipcode
        # 2 Firstname Lastname, color, zipcode, 703 955 0373
        # 3 Firstname, Lastname, zipcode, 646 111 0101, color
        # 4 Error

    @pytest.mark.parametrize("csv_data", [b'last_name, first_name, (653)-889-7235, yellow, 70703'])
    def test_process_data_entries(self, csv_data):
        binaryStream = io.BytesIO(csv_data)
        result = process_data(binaryStream)
        expected_json = {
            "entries": [
                {
                    "color": "yellow",
                    "firstname": "Quinton",
                    "lastname": "Liptak",
                    "phonenumber": "653-889-7235",
                    "zipcode": 70703
                }
            ],
            "errors": []
        }
        assert result != expected_json