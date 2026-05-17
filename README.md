# RM Insight

RM Insight is a Python desktop application that cleans and summarises raw Genesys email export data into a structured Excel report.

The app was built to reduce manual spreadsheet work by taking raw Genesys CSV exports, extracting priority values from email subject lines, calculating workload and average handle time metrics, and exporting a clean agent-level summary.

This project demonstrates practical data handling, cleaning, transformation, aggregation, and reporting using Python.

## Overview

Raw Genesys email exports can contain useful operational reporting data, but the information is not always ready to use straight away.

For example:

- Agent names may need to be cleaned
- Priority values are embedded inside the email subject line
- Handle time is stored as raw seconds
- The data needs to be grouped by agent and priority
- Only selected agents may need to be included in the final report

RM Insight automates this process and produces a cleaner Excel output that can be used for workload review and reporting.

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
| `Media Type` |
| `Remote` |
| `Date` |
| `Duration` |
| `Direction` |
| `Queue` |
| `Wrap-up` |
| `External Tag` |

These additional columns can remain in the file. The app focuses on the fields required for the summary report.

## Example Input

Example Genesys subject values:

````text
P1 - 1129000010 - Urgent Power Outage
P2 - 1129000011 - Water Leak Reported
P3 - 1129000012 - Broken Door Handle
P3.5 - 1129000013 - Air Conditioner Fault
P4 - 1129000014 - General Repair Request
P5 - 1129000015 - Follow Up Request
P5 (within 7 days) - 1129000016 - Scheduled Maintenance Query
