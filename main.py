from modules import analyzer
import os


def main():
    file = input("Enter file name: ")
    if os.path.exists(file) == False:
        print(f"{file} does not exist.")

    passport_analyzer = analyzer.PassportMachineReadableZoneAnalyzer(file)
    passport_analyzer.parse()

if __name__ == "__main__":
    main()