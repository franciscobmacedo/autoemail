from main import AutoEmail

import pandas as pd

df = pd.DataFrame({
        'stock': [1,2,3],
        'value': [1203,4034,3434],

    })

table = {'df': df, 'name': 'some_sales_data', 'max_len': ''}
# table = {}

body_text = "Today our sales increase here and decrease there mostly because of reasons. You can see it in the following image and in the atached pdf report"

AutoEmail('your_client_email@gmail.com', title='Sales Report', body_text=body_text, table=table)