import pandas as pd

# Load your Excel file
df = pd.read_excel("data/data_uet_vnu.xlsx")  # Replace with your actual file path

# Open a text file to write the output
with open("output.txt", "w", encoding="utf-8") as f:
    for i in range(len(df)):
        f.write(f"{df.loc[i, 'title']}\n")
        f.write(f"{df.loc[i, 'content']}\n\n")
