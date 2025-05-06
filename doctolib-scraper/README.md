# Doctolib Scraper

This project is a web scraper designed to interact with the Doctolib website, allowing users to search for healthcare practitioners based on specific criteria and filters. The scraper extracts useful information and generates consultation sheets for each doctor in CSV format.

## Project Structure

```
doctolib-scraper
├── src
│   ├── app.py                # Main entry point of the application
│   ├── utils
│   │   ├── filters.py        # Functions to apply filters based on user input
│   │   ├── scraper.py        # Web scraping logic using Selenium
│   │   └── csv_writer.py     # Functions to write data to CSV format
├── requirements.txt          # List of dependencies
└── README.md                 # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd doctolib-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command in your terminal:

```
python src/app.py
```

### Input Parameters

When prompted, provide the following parameters:

- **Maximum number of results**: The maximum number of healthcare practitioners to display (e.g., first 10 doctors).
- **Availability period**: Start and end date in DD/MM/YYYY format.
- **Medical request**: Type of practitioner you are looking for (e.g., "dermatologist", "general practitioner").
- **Type of insurance**: Choose from sector 1, sector 2, or non-contracted.
- **Type of consultation**: Specify whether the consultation is remote or in-person.
- **Price range**: Minimum and maximum price in €.
- **Geographical filter**: Free keyword in the address (e.g., "rue de Vaugirard", "75015", "Boulogne"), with options to include or exclude certain areas.

### Output

The scraper will generate a CSV file containing the consultation sheets for each doctor based on the specified criteria.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.