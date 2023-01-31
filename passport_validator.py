import passporteye
import os


def main():
    file = "passport-images/passport3.png"
    if os.path.exists(file) == False:
        print(f"{file} does not exist.")

    mrz = get_mrz_data(file)
    pass_info = get_passport_info(mrz["raw_text"])
    clean_data(*pass_info)

        
def get_mrz_data(file):
    mrz_data = passporteye.read_mrz(file)
    mrz_data = mrz_data.to_dict()
    return mrz_data


def get_passport_info(mrz):
    """
    PassportEye can get this info on its own. However, it's sometimes wrong.
    Its reading of the mrz raw_text is much better, so I'm using that and
    implementing my own reading algorithm according to ICAO standards.
    """
    mrz = mrz.splitlines()
    doc_type = mrz[0][0:2]
    country = mrz[0][2:5]
    name = mrz[0][5:36]
    pass_number = mrz[1][0:9]
    pass_num_check = digit_check(mrz[1][9], pass_number)
    nationality = mrz[1][10:13]
    birth_date = mrz[1][13:19]
    birth_date_check = digit_check(mrz[1][19], birth_date)
    sex = mrz[1][20]
    valid_exp_date = mrz[1][21:27]
    valid_exp_date_check = digit_check(mrz[1][27], valid_exp_date)
    optional_data = mrz[1][28:36]


    return (doc_type, country, name, pass_number, 
            pass_num_check, nationality, birth_date, 
            birth_date_check, sex, valid_exp_date, 
            valid_exp_date_check, optional_data)

    

def digit_check(d_check, sequence):
    sequence = [int(n) for n in sequence]
    d_check = int(d_check)
    weighting = [7, 3, 1]
    result = []
    for i, digit in enumerate(sequence):
        result.append(digit * weighting[i % len(weighting)])
        
    result = sum(result) % 10
    return (result == d_check)



if __name__ == "__main__":
    main()
 