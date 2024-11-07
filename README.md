# Room Price Processor

A Python application to load room pricing data from a JSON file, calculate total prices (including taxes) for each room, find the cheapest room, and save the results to a new JSON file.

## Table of Contents
- [Requirements](#Requirements)
- [Setup](#Setup)
- [Usage](#Usage)
- [Logging](#logging)

## Requirements

- Python 3.6 or higher
- `json` and `logging` libraries (included in the Python standard library)

## Setup

1. **Clone the repository**:
    ```bash
    git clone git@github.com:shpilieveoialexander/room-price-processor.git
    cd room-price-processor
    ```

2. **Install dependencies** (optional if using additional packages):
   This script only uses standard libraries, so no additional dependencies are required.

3. **Prepare Input Data**:
   Ensure you have a `data.json` file in the root directory with the following structure:
   ```json
   {
       "assignment_results": [
           {
               "shown_price": {
                   "room_type_1": "100.00",
                   "room_type_2": "120.50"
               },
               "net_price": {
                   "room_type_1": "90.00",
                   "room_type_2": "110.50"
               },
               "number_of_guests": 2,
               "ext_data": {
                   "taxes": "{\"tax1\": \"10.00\", \"tax2\": \"5.00\"}"
               }
           }
       ]
   }
4. **File structure** :
```room-price-processor/
├── main.py             # Main script file with classes and functions
├── data.json           # Input data file (provide your own)
├── output.json         # Generated output with the cheapest room and total prices
├── app.log             # Log file recording application process and errors
└── README.md           # Instructions for setup and usage
```

## Usage
```
python main.py
```