import pdfplumber
import pandas as pd
import numpy as np

def make_pkl(filename = "ExamSeatingArrangement.pdf", output="seating_arrangement.pkl"):
    dfs = []
    columns = None

    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
            })

            if table:
                if columns is None:
                    columns = [col.replace("\n", " ").strip() for col in table[0]]
                    data = table[1:]
                else:
                    data = table

                df = pd.DataFrame(data, columns=columns)
                df = df.map(lambda x: x.replace("\n", " ").strip() if isinstance(x, str) else x, na_action="ignore")
                dfs.append(df)

    # combine all pages
    final_df = pd.concat(dfs, ignore_index=True)

    final_df = final_df.replace("", np.nan)
    final_df = final_df.ffill()

    final_df.to_pickle(output)