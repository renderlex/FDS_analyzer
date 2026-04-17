# FDS Data Analyzer — User Manual (English)

> **FDS Analyzer** is a desktop tool for loading, visualising, and exporting Fire Dynamics Simulator (FDS) output data. It automatically detects critical threshold crossings for each sensor and parameter, displays interactive charts, and exports professional Word (.docx) reports.

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [Launching the Application](#2-launching-the-application)
3. [Interface Overview](#3-interface-overview)
4. [Language Switching (EN / UA)](#4-language-switching-en--ua)
5. [Step-by-Step Workflow](#5-step-by-step-workflow)
   - 5.1 [Select Input File](#51-select-input-file)
   - 5.2 [Configure Column Mapping (optional)](#52-configure-column-mapping-optional)
   - 5.3 [Bulk Column Assignment (optional)](#53-bulk-column-assignment-optional)
   - 5.4 [Run Analysis](#54-run-analysis)
   - 5.5 [Interpreting Charts](#55-interpreting-charts)
   - 5.6 [Summary Table](#56-summary-table)
   - 5.7 [Export to Word](#57-export-to-word)
6. [Supported Parameters](#6-supported-parameters)
7. [Input File Format](#7-input-file-format)
8. [Unknown Parameters](#8-unknown-parameters)
9. [Troubleshooting](#9-troubleshooting)
10. [Technical Specifications](#10-technical-specifications)

---

## 1. Requirements

| Item | Details |
|------|---------|
| OS | Windows 10 / 11 (64-bit) |
| Python | 3.9 or newer (if running from source) |
| Dependencies | `pandas`, `matplotlib`, `python-docx` (see `requirements.txt`) |
| Input formats | `.txt`, `.csv` (FDS output with two-row header) |
| Output formats | `.docx` (Word report) |

To install dependencies from source:

```
pip install -r requirements.txt
```

---

## 2. Launching the Application

**From source:**

```
python app_gui.py
```

**Portable executable (if compiled):**  
Double-click `FDS_Analyzer.exe` in the `FDS_Analyzer_Portable` folder.

---

## 3. Interface Overview

```
┌────────────────────────────────────────────────[ EN ]─┐
│  1. Select FDS input file (.txt or .csv):              │
│  [ file path entry field                 ] [Browse...] │
│                                                        │
│  [ Configure Column Mapping        ]  ← orange button  │
│  [ Bulk Column Assignment          ]  ← red button     │
│                                                        │
│  [ Run Analysis and Display Charts ]  ← green button   │
│  [ Export Data to Word (.docx)     ]  ← blue button    │
│                                                        │
│  Status: Waiting for file selection...                  │
│ ┌──────────────────────────────────────────────────┐  │
│ │  (scrollable chart area)                         │  │
│ └──────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

| Button | Colour | Purpose |
|--------|--------|---------|
| **EN / UA** (top-right) | Gray | Switch interface language |
| **Browse…** | Default | Open file picker |
| **Configure Column Mapping** | Orange | Map each file column to a parameter |
| **Bulk Column Assignment** | Red | Assign a whole group of numbered columns at once |
| **Run Analysis and Display Charts** | Green | Process data and draw charts |
| **Export Data to Word (.docx)** | Blue | Save charts + summary table to a Word document |

---

## 4. Language Switching (EN / UA)

Click the **EN** button (top-right corner) to switch the UI to English.  
The button label then changes to **UA** — click it again to revert to Ukrainian.

All UI elements update immediately:
- Window title, labels, buttons, and status bar
- Dialog windows opened **after** the switch
- **Chart axis labels, titles, and legend text** — these are applied at analysis time, so re-run the analysis after switching languages to regenerate charts in the new language
- **Word document** — always uses the language that was active when "Export to Word" was clicked

---

## 5. Step-by-Step Workflow

### 5.1 Select Input File

1. Click **Browse…** next to the file path field.
2. In the file picker, navigate to your FDS output file and select it.
3. Supported extensions: `.txt`, `.csv`.
4. The full path appears in the entry field and the status bar turns green.

> **Note:** Selecting a new file resets any previously configured column mapping.

---

### 5.2 Configure Column Mapping (optional)

Use this if the program cannot automatically recognise your column names (non-standard format).

1. Click **Configure Column Mapping** (orange).
2. A dialog lists every data column found in the file.
3. For each column, choose the corresponding parameter from the drop-down list  
   (e.g. `Temp1 (C)` → `Temp: Temperature`).
4. Leave a column as **"-- Do not use --"** to ignore it.
5. Click **Confirm** to save.

---

### 5.3 Bulk Column Assignment (optional)

Use this when you have many columns of the same type (e.g. 50 temperature sensors).

1. Click **Bulk Column Assignment** (red).
2. The dialog groups columns that share the same name pattern  
   (e.g. `Temp 01 (C)`, `Temp 02 (C)`, … are one group).
3. For each group, pick the parameter from the drop-down.
4. Click **Show all columns** to preview the full list for a group.
5. Click **Confirm** — all columns in the selected groups are mapped at once.

---

### 5.4 Run Analysis

Click **Run Analysis and Display Charts** (green).

The program will:
1. Load the input file.
2. Apply column mapping (automatic or manual).
3. Detect the first moment each sensor crosses its critical threshold.
4. Draw one chart per sensor/parameter combination.
5. Build a summary table below the charts.
6. Enable the **Export to Word** button.

A progress message is shown in the status bar throughout.
<img width="1578" height="381" alt="Знімок екрана 2026-04-17 232718" src="https://github.com/user-attachments/assets/a98fa49b-003b-411c-9d42-396284e0aa73" />

---

### 5.5 Interpreting Charts

Each chart shows:

| Element | Meaning |
|---------|---------|
| **Blue curve** | Measured parameter value over time |
| **Orange dashed line** | Critical threshold for that parameter |
| **Red label below chart** | Timestamp (in seconds) when the threshold was first crossed |
| **Legend** | Sensor name and critical threshold value |

- X-axis: **Time (s)**
- Y-axis: **Parameter name (unit)**
- Charts are scrollable — use the scrollbar on the right.
- Each chart has a navigation toolbar (zoom, pan, save).

---

### 5.6 Summary Table

Below all charts, a summary table is automatically displayed:

| Column | Content |
|--------|---------|
| **Parameter** | Name of the measured quantity |
| **Sensor** | Sensor number |
| **Critical Value** | Threshold value (with units) |
| **Time Reached (s)** | First crossing time in seconds, or "Not reached" |

---

### 5.7 Export to Word

1. Click **Export Data to Word (.docx)** (blue).
2. Choose the save location and filename in the file-save dialog.
3. The Word document is created with:
   - Title: `FDS Data Analysis Report: <filename>`
   - Creation timestamp
   - All charts as high-resolution images (300 dpi)
   - Summary table with the same data as shown on screen
4. The document language matches the UI language active at export time.

---

## 6. Supported Parameters

The application automatically recognises the following FDS parameter codes:

| Code | English Name | Unit | Critical Value | Direction |
|------|-------------|------|---------------|-----------|
| `Temp` | Temperature | °C | 60.0 | above |
| `Visio` | Visibility | m | 20.0 | below |
| `TP` | Heat Flux | kW/m² | 20.0 | above |
| `KK` | Oxygen | kg/m³ | 0.15 | below |
| `OV` | Carbon Monoxide | kg/m³ | 0.015 | above |
| `DV` | Carbon Dioxide | kg/m³ | 0.05 | above |

**Direction** means:
- `above` — critical when the value **exceeds** the threshold.
- `below` — critical when the value **falls below** the threshold.

---

## 7. Input File Format

FDS output files must have **two header rows**:

```
Row 1:  units (e.g.  s,     C,     C,     m,     m)
Row 2:  labels (e.g. ,   Temp01, Temp02, Visio01, Visio02)
```

Example (CSV):
```csv
s,C,C,m,m
,Temp01,Temp02,Visio01,Visio02
0.0,20.1,19.8,35.2,36.0
1.0,20.5,20.0,34.9,35.5
...
```

- The first column must be simulation time (unit `s`).
- Column names should follow the pattern `<ParamCode><Number>` (e.g. `Temp01`, `Visio03`).
- If your file uses a different naming scheme, use the **Column Mapping** feature.

---

## 8. Unknown Parameters

If the file contains parameter codes not in the built-in list, the program will prompt you:

1. A dialog appears listing each unknown code.
2. For each code provide:
   - **Full name** — display name for charts and reports
   - **Units** — measurement unit (type or pick from the drop-down)
   - **Critical value** — threshold number
   - **Direction** — `>` (above) or `<` (below)
3. Click **Confirm** to include these parameters in the analysis.

User-defined parameters are kept for the current session only.

---

## 9. Troubleshooting

| Problem | Solution |
|---------|---------|
| No charts appear after analysis | Use **Configure Column Mapping** to manually assign columns to parameters |
| "No data found" message | Check that the file has at least two header rows and numeric data |
| Charts have wrong parameter names | Make sure column names follow the `<Code><Number> (unit)` format, or use column mapping |
| Word export fails | Ensure you have write permission to the chosen folder; close the file if it is already open |
| Application is slow with large files | Large files (>10 MB) can take several seconds; wait for the status bar to show "complete" |
| Text in charts is still in the wrong language | Switch language, then click **Run Analysis** again to regenerate charts |

---

## 10. Technical Specifications

| Item | Value |
|------|-------|
| GUI framework | Python `tkinter` |
| Plotting | `matplotlib` (TkAgg backend) |
| Data processing | `pandas` |
| Word export | `python-docx` |
| Chart export resolution | 300 dpi |
| Supported Windows | Windows 10 / 11 (64-bit) |
| Interface languages | Ukrainian (default), English |

---

*FDS Data Analyzer — version 1.0*  
*For Ukrainian documentation see README.txt*

