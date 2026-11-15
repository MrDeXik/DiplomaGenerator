import pandas as pd
from reportlab.lib import pagesizes, units
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
import os
import json

def print_diplomas(dataframe: pd.DataFrame, output_file: str, printCombined: bool = True, firstPlaceOnly: bool = False) -> None:
    # Measured from the BOTTOM-LEFT corner of the paper to the middle of the text (x, y) in millimeters
    name_x_pos = 105 * units.mm
    name_y_pos = 120 * units.mm
    placement_x_pos = 105 * units.mm
    placement_y_pos = 85 * units.mm
    age_cat_x_pos = 55 * units.mm
    age_cat_y_pos = 60 * units.mm
    weight_cat_x_pos = 90 * units.mm
    weight_cat_y_pos = 40 * units.mm
    pdfmetrics.registerFont(ttfonts.TTFont('Arial-Bold', 'arialbd.ttf'))

    tracking_file = "printed_categories.json"
    if os.path.exists(tracking_file):
        with open(tracking_file, "r", encoding="utf-8") as f:
            # Load as a Python set for fast lookups
            printed_categories = set(json.load(f))
    else:
        printed_categories = set()

    c = canvas.Canvas(output_file, pagesize=pagesizes.portrait(pagesizes.A4)) # portrait - vertical, landscape - horizontal
    if printCombined:
        title = "All Competitors"
    else:
        title = "Winners" if firstPlaceOnly else "Second Place and Third Place"
    c.setTitle(title)

    printed_count = 0
    for (age_cat, weight_cat), group in dataframe.groupby(
        ["Age category", "Weight category"]
    ):
        category_key = f"{age_cat} | {weight_cat} | {"Winners" if firstPlaceOnly else "All"}"
        if category_key in printed_categories:
            continue

        print(f"Printing category: {category_key}")
        age_cat = str(age_cat).strip()
        weight_cat = str(weight_cat).strip()
        for i, row in group.iterrows():
            c.setFont("Arial-Bold", 42)
            c.drawCentredString(name_x_pos, name_y_pos - 25 * units.mm if firstPlaceOnly else name_y_pos, row["Name"])
            if not firstPlaceOnly:
                c.setFont("Arial-Bold", 35)
                c.drawCentredString(placement_x_pos, placement_y_pos, row["Placement"])
            c.setFont("Arial-Bold", 20)
            c.drawCentredString(age_cat_x_pos + c.stringWidth(age_cat, "Arial-Bold", 20) / 2, age_cat_y_pos, age_cat)
            c.drawCentredString(weight_cat_x_pos + c.stringWidth(weight_cat, "Arial-Bold", 20) / 2, weight_cat_y_pos, weight_cat)
            c.showPage()
            printed_count += 1

        printed_categories.add(category_key)
        with open(tracking_file, "w", encoding="utf-8") as f:
            json.dump(list(printed_categories), f, ensure_ascii=False, indent=4)
    c.save()
    print(f"Successfully generated {output_file} with {printed_count} names!")

    # os.startfile(output_file, 'print')