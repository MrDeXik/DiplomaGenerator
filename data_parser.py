import pandas as pd
import re

def weight_sort_key(val):
  val_str = str(val).strip()

  # 1. Assign sign priority: '+' goes last (1), '-' goes first (0)
  sign_priority = 1 if val_str.startswith("+") else 0

  # 2. Extract the numeric value from the string (e.g., "-30 kg" -> 30)
  match = re.search(r"\d+", val_str)
  numeric_val = int(match.group(0)) if match else 0

  return (sign_priority, numeric_val)

def parse_data(source_file) -> pd.DataFrame:
    sheets_dict = pd.read_excel(source_file, sheet_name=None, header=None)

    all_parsed_data = []

    for age_category, df_raw in sheets_dict.items():
        i = 0
        while i < len(df_raw):
            row = df_raw.iloc[i]
            
            if any(re.search(r"[+-]?\d+\d+ kg", str(val).strip()) for val in row.values):
                category =  re.split(r"([-+])", str(row.values[0]).strip(), maxsplit=1)
                weight_cat = (category[1] + category[2]).strip()
                i += 2

                while i < len(df_raw):
                    row = df_raw.iloc[i]
                    if row.isna().all():
                        break

                    if int(str(row.iloc[0]).split(".")[0]) > 3:
                        i += 1
                        continue

                    all_parsed_data.append({
                        "Age category": re.split(r"[MW]U", age_category)[0].strip(),
                        "Weight category": weight_cat,
                        "Placement": row.iloc[0],
                        "Name": str(row.iloc[2]).strip() + " " + str(row.iloc[3]).strip(),
                        "Club": row.iloc[4],
                    })
                    i+= 1
            i += 1

    df = pd.DataFrame(all_parsed_data, columns=["Age category", "Weight category", "Placement", "Name", "Club"])
    df["_weight_sort"] = df["Weight category"].map(weight_sort_key)
    df.sort_values(by=["Age category", "_weight_sort", "Placement"], inplace=True, ignore_index=True)
    df.drop(columns=["_weight_sort"], inplace=True)
    return df