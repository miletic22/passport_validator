import os
from passport_validators import analyzer
from passport_validators import face_detection

def main():
    file = input("Enter file name: ")
    if os.path.exists(file) == False:
        print(f"{file} does not exist.")

    passport_analyzer = analyzer.PassportMachineReadableZoneAnalyzer(file)
    passport_analyzer.parse()

    face_detection.recognize_passport_face(file)


if __name__ == "__main__":
    main()