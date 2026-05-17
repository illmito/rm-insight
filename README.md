# RM Insight

RM Insight is a Python desktop application that cleans and summarises raw Genesys email export data into a structured Excel report.

The app was built to reduce manual spreadsheet work by taking raw Genesys CSV exports, cleaning the data, extracting priority values from email subject lines, calculating workload and average handle time metrics, and exporting a clean agent-level summary.

This project demonstrates practical data handling, data cleaning, transformation, aggregation, reporting automation, and GUI development using Python.

---

## Project Goal

The goal of RM Insight is to turn raw Genesys email interaction data into a clean reporting output with minimal manual spreadsheet handling.

Raw Genesys exports contain useful reporting data, but the information is not always ready for analysis straight away. Agent names may need cleaning, priority values can be embedded inside subject lines, and handle time values need to be grouped and summarised before they are useful for reporting.

RM Insight provides a repeatable process for preparing this data and producing a cleaner Excel summary that can be used for workload review and operational reporting.

---

## What This Project Demonstrates

This project shows how Python can be used to take raw operational data and turn it into a structured reporting output.

It demonstrates:

- Importing raw CSV data
- Validating required columns
- Cleaning inconsistent text fields
- Extracting structured values from free-text subject lines
- Classifying email records by priority
- Aggregating data by agent
- Calculating workload totals
- Calculating average handle time metrics
- Exporting cleaned results to Excel
- Building a simple GUI for non-technical users

---

## Before and After

### Raw Input

The input is a Genesys CSV export where each row represents an email interaction.

The raw data can include fields such as:

- Agent or user information
- Email subject line
- Queue
- Direction
- Wrap-up result
- Handle time
- Date and time of the interaction

Some of this information needs to be cleaned or transformed before it can be used for reporting.

Examples of raw data issues:

- Agent names may include extra queue or transfer text
- Priority values are stored inside the email subject line
- Handle time is stored as raw seconds
- The data needs to be grouped before it becomes useful
- Only selected agents may need to be included in the final report

### Cleaned Output

RM Insight produces an Excel summary showing:

- Agent name
- Count of emails by priority
- Total priority workload
- Average handle time by priority
- Overall average handle time
- Final total / average summary row

---

## Features

- Upload raw Genesys email CSV exports
- Validate that required columns are present
- Clean the `Users` field to identify the relevant agent
- Extract priority values from the `Subject` field using regular expressions
- Recognise priority levels including:
  - P1
  - P2
  - P3
  - P3.5
  - P4
  - P5
  - P5 within 7 days
- Convert raw handle time from seconds into readable time format
- Calculate job counts by priority
- Calculate average handle time by priority
- Calculate total jobs per agent
- Calculate overall average handle time
- Select relevant agents before exporting
- Add a final `TOTAL / TOTAL AVG` summary row
- Export the final result to Excel
- Includes an in-app help window explaining required fields and common issues

---

## Input Data

The app expects a CSV file exported from Genesys email data.

The required columns are:

| Column | Purpose |
|---|---|
| `Users` | Identifies the agent who handled the email |
| `Subject` | Used to extract the priority value |
| `Total Handle` | Used to calculate average handle time |

The raw Genesys export may also include additional columns such as:

| Column |
|---|
| `Full Export Completed` |
| `Partial Result Timestamp` |
| `Filters` |
| `Media Type` |
| `Remote` |
| `Date` |
| `Duration` |
| `Direction` |
| `Queue` |
| `Wrap-up` |
| `External Tag` |

These additional columns can remain in the CSV file. The current version of the app focuses on the fields required for the summary report.

---

## Example Input

Example Genesys email subject values:

```text
P1 - 1129000010 - Urgent Power Outage
P2 - 1129000011 - Water Leak Reported
P3 - 1129000012 - Broken Door Handle
P3.5 - 1129000013 - Air Conditioner Fault
P4 - 1129000014 - General Repair Request
P5 - 1129000015 - Follow Up Request
P5 (within 7 days) - 1129000016 - Scheduled Maintenance Query
General enquiry - 1129000017 - No priority listed
```

---

## Priority Detection

The app scans the `Subject` field and classifies each record into a priority group.

Recognised values:

| Subject Value | Output Value |
|---|---|
| `P1` | `P1` |
| `P2` | `P2` |
| `P3` | `P3` |
| `P3.5` | `P3.5` |
| `P4` | `P4` |
| `P5` | `P5` |
| `P5 (within 7 days)` | `P5 7D` |

If no priority is detected, the record is marked as `Nil`.

---

## Example Output

The exported Excel file includes a cleaned summary similar to this:

| RM AGENT | P1 | P2 | P3 | P3.5 | P4 | P5 | P5 7D | P Total | Average Total Handle |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Alex Johnson | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 4 | 0:05:28 |
| Brianna Smith | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 5 | 0:04:47 |
| Chloe Martin | 0 | 0 | 1 | 1 | 2 | 0 | 0 | 4 | 0:05:12 |
| TOTAL / TOTAL AVG | 1 | 3 | 3 | 1 | 3 | 1 | 1 | 13 | 0:05:09 |

The final exported report also includes average handle time columns for each individual priority.

---

## How It Works

1. The user uploads a Genesys CSV export.
2. The app checks that the required columns exist.
3. The `Users` field is cleaned so the relevant agent name is retained.
4. The `Subject` field is scanned for priority values.
5. The `Total Handle` field is converted into numeric values.
6. The data is grouped by agent.
7. Priority counts and average handle times are calculated.
8. The user selects which agents to include.
9. A final total / average summary row is added.
10. The final report is exported to Excel.

---

## Tech Stack

- Python
- pandas
- NumPy
- Tkinter
- Regular Expressions
- Excel export via pandas

---

## Data Skills Demonstrated

This project demonstrates an end-to-end data preparation workflow:

- CSV ingestion
- Data validation
- Data cleaning
- Text parsing
- Regex-based classification
- Data transformation
- Grouping and aggregation
- Average handle time calculation
- Time format conversion
- Excel report generation
- Basic GUI workflow design
- Error handling and user feedback

---

## Mock Data

This repository includes mock Genesys email export data for demonstration and testing.

The mock dataset contains:

- Fake agent names
- Fake customer email addresses
- Fake reference numbers
- Fake email subject lines
- Fake priority values
- Fake handle time values
- Genesys-style export columns

No real customer, employee, or workplace data is included.

Recommended mock data file:

```text
mock_genesys_email_data_1200.csv
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/rm-insight.git
cd rm-insight
```

Install the required Python packages:

```bash
pip install pandas numpy openpyxl
```

Run the app:

```bash
python Rm_insight_work_.py
```

---

## Usage

1. Open the app.
2. Click `Upload CSV`.
3. Select a Genesys email export CSV file.
4. Click `Process`.
5. Select the relevant agents to include in the final report.
6. Click `Save`.
7. Choose where to save the Excel output.

---

## Notes

This project uses mock or anonymised data for demonstration purposes.

No real customer, employee, or operational data should be committed to this repository.

The current version of the app is designed for CSV exports that include the required columns:

```text
Users
Subject
Total Handle
```

---

## Project Purpose

This project was created as a practical example of using Python to clean and summarise raw operational data.

It is intended to showcase data handling and reporting automation skills for data analyst, reporting, and business operations roles.

RM Insight shows how a manual spreadsheet process can be turned into a repeatable Python workflow that improves consistency, reduces manual handling, and produces cleaner reporting outputs.
