# Test-PPT: Root Cause Analysis Report Tool

A simple desktop GUI tool (Tkinter) that reads an Excel file of issue records,
counts how often each root-cause category occurs, and shows a ranked bar chart
(most frequent cause first). The chart can be exported to a PowerPoint slide.

## Setup

```
py -m pip install -r requirements.txt
```

## Run

```
py main.py
```

## Usage

1. Click "Load Excel File" and select a spreadsheet.
2. Pick the column that contains the root-cause / issue category for each row.
3. Click "Preview" to see the ranked bar chart.
4. Click "Save as PPT" to export the chart to a PowerPoint slide.
