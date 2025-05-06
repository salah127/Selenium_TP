# Doctolib Scraper

This project is a Selenium-based web scraper designed to interact with the [Doctolib](https://www.doctolib.fr) website. It allows users to search for medical professionals based on specific criteria, extract relevant information, and save the results in a CSV file.

## Features

- Search for medical professionals based on:
  - Type of medical professional (e.g., "general practitioner").
  - Insurance type (e.g., "secteur 1").
  - Geographical location.
  - Availability dates.
  - Consultation type (in-person or teleconsultation).
  - Price range.
- Extract and save data such as:
  - Name, availability, consultation type, sector, address, and city.
- Export results to a CSV file.

## Requirements

Ensure you have the following installed:

- Python 3.8 or higher
- Google Chrome browser

### Python Dependencies

The required Python libraries are listed in `requirements.txt`. Install them using:

```bash
pip install -r [requirements.txt]
```
