import passporteye
import pycountry
import re

class PassportMachineReadableZoneAnalyzer():
    def __init__(self, file):
        self.file = file
    
    def get_mrz_data(self, file):
        mrz_data = passporteye.read_mrz(file)
        mrz_data = mrz_data.to_dict()
        return mrz_data
    def get_passport_info(self, mrz):
        """
        PassportEye can get this info on its own. However, it's sometimes wrong.
        Its reading of the mrz raw_text is much better, so I'm using that and
        implementing my own reading algorithm according to ICAO 9303 standards.
        """
        mrz = mrz.splitlines()
        doc_type = mrz[0][0:2]
        country = mrz[0][2:5]
        name = mrz[0][5:36]
        pass_number = mrz[1][0:9]
        pass_num_check = self.digit_check(mrz[1][9], pass_number)
        nationality = mrz[1][10:13]
        birth_date = mrz[1][13:19] # YYMMDD
        birth_date_check = self.digit_check(mrz[1][19], birth_date)
        sex = mrz[1][20]
        valid_exp_date = mrz[1][21:27]
        valid_exp_date_check = self.digit_check(mrz[1][27], valid_exp_date)
        optional_data = mrz[1][28:36]

        return (
            doc_type, country, name, pass_number, 
            pass_num_check, nationality, birth_date, 
            birth_date_check, sex, valid_exp_date, 
            valid_exp_date_check, optional_data
        )

    def digit_check(self, d_check, sequence):
        character_keys = {
            "<": 0, "A": 10, "B": 11, 
            "C": 12, "D": 13, "E": 14,
            "F": 15, "G": 16, "H": 17, 
            "I": 18, "J": 19, "K": 20,
            "L": 21, "M": 22, "N": 23, 
            "O": 24, "P": 25, "Q": 26, 
            "R": 27, "S": 28, "T": 29, 
            "U": 30, "V": 31, "W": 32,
            "X": 33, "Y": 34, "Z": 35 
        }
        updated_sequence = []
        for char in sequence:
            if char.isdigit():
                updated_sequence.append(char)
            else:
                updated_sequence.append(character_keys.get(char))
        d_check = int(d_check)

        weighting = [7, 3, 1]
        result = []
        for i, digit in enumerate(updated_sequence):
            result.append(int(digit) * weighting[i % len(weighting)])
        result = sum(result) % 10

        return (result == d_check)
    
    def clean_data (
            self, doc_type, country, name, pass_number, 
            pass_num_check, nationality, birth_date, 
            birth_date_check, sex, valid_exp_date, 
            valid_exp_date_check, optional_data
        ):
        
        if "P" in doc_type:
            doc_type = "Passport"
        else:
            doc_type = "Not a passport"

        country = re.match(r"\w+", country).group(0)
        try: # Sometimes the extracted country cannot be found, e.g. extracts "D<<"
            country = pycountry.countries.search_fuzzy(country)
        except LookupError:
            country = "Unknown"
        else:
            country = re.search("(?<=official_name=').+(?=')", str(country))
            country = country.group()
            if len(country) > 20:
                country = "Unknown"

        letter_groups = re.findall(r"\w+", name)
        name = letter_groups[1], letter_groups[0]
        
        year, month, day = re.findall(r"\d{2}", birth_date)
        birth_date = f"{month}/{day}/{year}"
        
        if sex == "F":
            sex = "Female"
        elif sex == "M":
            sex = "Male"
        else:
            sex = "Other"
    
        year, month, day = re.findall(r"\d{2}", valid_exp_date)
        valid_exp_date = f"{month}/{day}/{year}"
        
        return (self, doc_type, country, name, pass_number, 
            pass_num_check, nationality, birth_date, 
            birth_date_check, sex, valid_exp_date, 
            valid_exp_date_check, optional_data
            )
    
        # actually changed only: self, doc_type, country, name, birth_date, sex, valid_exp_date, 

    def print_passport_data(self, dummy, doc_type, country, name, pass_number, 
                            pass_num_check, nationality, birth_date, 
                            birth_date_check, sex, valid_exp_date, 
                            valid_exp_date_check, optional_data):
        result = f"NAME: {name[1]}\n" \
                f"SURNAME: {name[0]}\n" \
                f"DOCUMENT TYPE: {doc_type}\n" \
                f"NATIONALITY: {country}\n" \
                f"PASS NUMBER: {pass_number} ({pass_num_check})\n" \
                f"BIRTH DATE: {birth_date} ({birth_date_check})\n" \
                f"SEX: {sex}\n" \
                f"EXP. DATE: {valid_exp_date} ({valid_exp_date_check})\n" \
                f"OPT. DATA: {optional_data}"
        print(result)
    def parse(self):
        
        self.mrz = self.get_mrz_data(self.file)
        self.pass_info = self.get_passport_info(self.mrz["raw_text"])
        self.data = self.clean_data(*self.pass_info)
        self.print_passport_data(*self.data)



def main():
    ... 

if __name__ == "__main__":
    main()