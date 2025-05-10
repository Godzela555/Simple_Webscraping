# 🏦 Largest Banks Web Scraper

This Python project scrapes data from an archived Wikipedia page listing the world's largest banks by market capitalization. It processes and transforms the data, converts USD values to multiple currencies (GBP, EUR, INR), and stores the result in both a CSV file and an SQLite database. It also includes sample SQL queries for basic analysis.

---

## 📌 Project Highlights

- 🔍 **Web scraping** with `BeautifulSoup` and `requests`
- 📊 **Data cleaning & transformation** using `pandas` and `numpy`
- 💱 **Currency conversion** using real-world exchange rates
- 🗃️ **Storage** in CSV and SQLite database formats
- 🧠 **Basic SQL queries** to demonstrate insights from the data
- 📝 **Logging system** to track script progress

---

## 🛠️ Tech Stack

- Python 3.11
- pandas
- numpy
- requests
- BeautifulSoup (bs4)
- SQLite3

---

## 🗂️ Project Structure

├── webscraping_banks.py          # Main script
├── exchange_rate.csv             # Currency rates
├── code_log.txt                  # Log of script progress
├── Largest_banks_data.csv        # Final output data (CSV)
├── Banks.db                      # SQLite database output
└── README.md                     # You’re reading it!
