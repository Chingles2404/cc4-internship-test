# CC4 Data Engineer Internship Tech Test
## Running the Code
Ensure the following files are in the same directory:
- `Country-Code.xlsx`
- `main.py`

Run `main.py`

## Decisions
I decided to get `restaurant_data.json` from the URL instead of downloading the file and using it locally to prevent the data from potentially being edited by users.

I used the `pandas` and `openpyxl` libraries to read `Country-Code.xlsx`. I minimised the usage of these libraries by processing the data and putting it in a dictionary instead of using Pandas' DataFrame.

I realised that there was a country code 17 that was not in `Country-Code.xlsx`. After looking through `restaurant_data.json`, I discovered that the city names for all entries with country code 17 were "Dummy". As such, I assumed that those entries were not real restaurants and thus excluded them to prevent data from being skewed.
