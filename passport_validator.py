import passporteye
import os


def main():
    file = input("Enter file name: ")
    if os.path.exists(file) == False:
        print(f"{file} does not exist.")

    mrz = get_mrz_data(file)

        
def get_mrz_data(file):
    mrz_data = passporteye.read_mrz(file)
    mrz_data = mrz_data.to_dict()
    return mrz_data


if __name__ == "__main__":
    main()