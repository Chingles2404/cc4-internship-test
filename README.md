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

Although Part 2 stated to "extract the list of restaurants", the list of data needed seems to imply to extract a list of events, which is what I decided to do, since it would make more sense to have one entry per event than putting the information for multiple events into one entry.

I decided to modify the event titles when populating the `restaurant_events.csv` file to ensure the entire title is within a cell by removing newline characters and commas.

I discovered that there were some restaurants with a non-English rating text. Although I could guess what the text means based on the aggregate rating and recompute the ranges for each text from it, I decided not to do it. This is because Part 3's instructions stated which rating texts to include, which I interpreted to mean that the rating texts must be exactly equivalent to one of the listed texts, rahter than the meaning of the text to be equivalent to the meaning of one of the listed texts.

## Summary for Consideration of Cloud Services
TBA

## Architecture Diagram
TBA