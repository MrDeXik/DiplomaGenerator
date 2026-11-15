from data_parser import parse_data
from printer import print_diplomas
import sys
from pathlib import Path

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        # If it's an .exe, use the folder where the .exe file actually lives
        BASE_DIR = Path(sys.executable).parent
    else:
        # If it's a normal script, use the script's folder
        BASE_DIR = Path(__file__).resolve().parent

    source_file = BASE_DIR / "export.xlsx"
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    try:
        df = parse_data(source_file)
        print(f"Found {len(df)} competitors in total.")
    except Exception as e:
        print(f"Error occurred while parsing data: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    print("Select export mode:")
    print("  [1] Separate files (1st place vs. rest)")
    print("  [2] Single combined file (all together)")

    mode = input("Enter your choice (1 or 2): ").strip()

    try:
        if mode not in ["1", "2"]:
            raise ValueError("Invalid mode selected. Please choose either 1 or 2.")

        if mode == "1":
            print_diplomas(df[df["Placement"] == "1. místo"], output_file=f"{output_dir}/print_names_first.pdf", printCombined=False, firstPlaceOnly=True)
            print_diplomas(df[df["Placement"] != "1. místo"], output_file=f"{output_dir}/print_names_rest.pdf", printCombined=False, firstPlaceOnly=False)
            print("Success: Generated separate PDF files!")
        elif mode == "2":
            print_diplomas(df, output_file=f"{output_dir}/print_names.pdf", printCombined=True)
            print("Success: Generated single combined PDF file!")
    except Exception as e:
        print(f"Error occurred while printing data: {e}")
        input("Press Enter to exit...")
        sys.exit(1)    

    input("Press Enter to exit...")