#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import fitz
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def get_fields(file):
    field_data = {}
    pdf = fitz.open(file)
    for page in pdf:
        widgets = page.widgets()
        for widget in widgets:
            field_name = widget.field_name
            field_value = widget.field_value #Joyval
            if field_name in field_data:
                field_data[field_name].append(field_value)
            else:
                field_data[field_name] = [field_value]

    # make the DataFrame
    df = pd.DataFrame(field_data)

    # Replace non-filled values with NaN
    df.replace('', np.nan, inplace=True)

    return df

def get_input_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Select the input PDF file
    input_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return input_file_path

def get_output_directory():
    root = tk.Tk()
    root.withdraw() 

    # Open a file dialog to select the output directory
    output_directory = filedialog.askdirectory()
    return output_directory

def write_to_csv(df, output_path, filename):
    # Full outputs
    full_path = f"{output_path}/{filename}.csv"

    # Write DataFrame to CSV
    df.to_csv(full_path, index=False)

# Main idea
pdf_form_name = input("Specify which of the following: CFOG, MSRS_GSAP, NFOGQ, PRO_PAC, PAS, as an input you are trying to convert")

input_file_path = get_input_file()
fields_df = get_fields(input_file_path)

output_path = get_output_directory()
filename = f"{pdf_form_name}_{fields_df['ID'][0]}_output"

write_to_csv(fields_df, output_path, filename)

