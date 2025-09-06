# FITRS File Analysis Report

Comprehensive analysis of Financial Instrument Transparency System (FITRS) files.

Generated on: 2025-09-03 16:21:27

## 📊 Summary Statistics

- **Total Files Analyzed:** 38
- **Total Records:** 13,893,448
- **Unique Columns:** 41
- **File Types:** {'Unknown': 38}

### 🔗 Common Columns

Columns that appear in multiple files:

| Column Name | Appears in Files |
|-------------|------------------|
| TechRcrdId | 38 |
| FinInstrmClssfctn | 38 |
| FrDt | 38 |
| ToDt | 38 |
| Lqdty | 38 |
| ISIN | 35 |
| Desc | 35 |
| CritNm | 35 |
| CritVal | 35 |
| CritNm_2 | 34 |
| CritVal_2 | 34 |
| PreTradLrgInScaleThrshld_Amt | 34 |
| PstTradLrgInScaleThrshld_Amt | 34 |
| PreTradInstrmSzSpcfcThrshld_Amt | 34 |
| PstTradInstrmSzSpcfcThrshld_Amt | 34 |
| CritNm_3 | 22 |
| CritVal_3 | 22 |
| CritNm_4 | 22 |
| CritVal_4 | 22 |
| CritNm_5 | 22 |
| CritVal_5 | 22 |
| CritNm_6 | 19 |
| CritVal_6 | 19 |
| CritNm_7 | 15 |
| CritVal_7 | 15 |
| PreTradLrgInScaleThrshld_Nb | 15 |
| PstTradLrgInScaleThrshld_Nb | 15 |
| PreTradInstrmSzSpcfcThrshld_Nb | 15 |
| PstTradInstrmSzSpcfcThrshld_Nb | 15 |
| TtlNbOfTxsExctd | 8 |
| TtlVolOfTxsExctd | 8 |
| Id | 3 |
| Mthdlgy | 3 |
| AvrgDalyTrnvr | 3 |
| LrgInScale | 3 |
| AvrgDalyNbOfTxs | 3 |
| Id_2 | 3 |
| AvrgTxVal | 3 |
| StdMktSz | 3 |
| AvrgDalyNbOfTxs_2 | 3 |

## 📄 Individual File Analysis

### 📊 FULECR_20250830_C_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 28,469
- **Total Columns**: 16
- **File Size**: 2.2 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| Id | identifier | 0 | 100.0% | US78463V1070, US78463V1070, US78463V1070 |
| FinInstrmClssfctn | text | 0 | 100.0% | ETFS, ETFS, ETFS |
| FrDt | date | 1,288 | 95.5% | 2023-10-01, 2024-01-01, 2024-04-01 |
| ToDt | date | 1,288 | 95.5% | 2024-03-31, 2024-06-30, 2024-09-30 |
| Mthdlgy | text | 0 | 100.0% | SINT, SINT, SINT |
| TtlNbOfTxsExctd | numeric | 9,190 | 67.7% | 16374, 20141, 20322 |
| TtlVolOfTxsExctd | numeric | 9,190 | 67.7% | 700600217.49834, 629168379.16999, 794961311.63774 |
| Lqdty | boolean | 19,279 | 32.3% | false, true, false |
| AvrgDalyTrnvr | numeric | 19,279 | 32.3% | 11883.23961, 2593678.25046, 0 |
| LrgInScale | numeric | 19,279 | 32.3% | 3000000, 3000000, 3000000 |
| AvrgDalyNbOfTxs | numeric | 19,279 | 32.3% | 1.912, 28.93083, 0 |
| Id_2 | text | 19,287 | 32.2% | XCSE, BTFE, BTFE |
| AvrgTxVal | numeric | 26,841 | 5.7% | 76013.79745, 12724.47904, 43489.1869 |
| StdMktSz | numeric | 26,841 | 5.7% | 70000, 10000, 50000 |
| AvrgDalyNbOfTxs_2 | numeric | 28,374 | 0.3% | 0.61418, 10035.736, 10035.736 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "Id": "US78463V1070",
  "FinInstrmClssfctn": "ETFS",
  "FrDt": "2023-10-01",
  "ToDt": "2024-03-31",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "16374",
  "TtlVolOfTxsExctd": "700600217.49834",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "AvrgDalyNbOfTxs_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "Id": "US78463V1070",
  "FinInstrmClssfctn": "ETFS",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "20141",
  "TtlVolOfTxsExctd": "629168379.16999",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "AvrgDalyNbOfTxs_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "Id": "US78463V1070",
  "FinInstrmClssfctn": "ETFS",
  "FrDt": "2024-04-01",
  "ToDt": "2024-09-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "20322",
  "TtlVolOfTxsExctd": "794961311.63774",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "AvrgDalyNbOfTxs_2": ""
}
```

---

### 📊 FULECR_20250830_E_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 81,813
- **Total Columns**: 17
- **File Size**: 6.53 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| Id | identifier | 0 | 100.0% | US70975L1070, US69181V1070, US69181V1070 |
| FinInstrmClssfctn | text | 0 | 100.0% | SHRS, SHRS, SHRS |
| FrDt | date | 2,545 | 96.9% | 2024-04-01, 2023-10-01, 2024-01-01 |
| ToDt | date | 2,545 | 96.9% | 2024-09-30, 2024-03-31, 2024-06-30 |
| Mthdlgy | text | 0 | 100.0% | SINT, SINT, SINT |
| TtlNbOfTxsExctd | numeric | 26,394 | 67.7% | 1481, 2343, 3260 |
| TtlVolOfTxsExctd | numeric | 26,394 | 67.7% | 7579810.38813, 2213930.73668, 2934048.89022 |
| Lqdty | boolean | 55,419 | 32.3% | false, false, false |
| AvrgDalyTrnvr | numeric | 55,422 | 32.3% | 2667.15554, 5431.53343, 53.51798 |
| LrgInScale | numeric | 55,422 | 32.3% | 15000, 15000, 15000 |
| AvrgDalyNbOfTxs | numeric | 55,422 | 32.3% | 7, 27.8125, 0.20425 |
| Id_2 | text | 55,441 | 32.2% | FRAB, XSAT, FRAB |
| AvrgDalyNbOfTxs_2 | numeric | 55,542 | 32.1% | 0, 27.8125, 0.12462 |
| AvrgTxVal | numeric | 79,924 | 2.3% | 16762.64748, 2501.30641, 7745.8734 |
| StdMktSz | numeric | 79,924 | 2.3% | 10000, 10000, 10000 |
| Sttstcs | empty | 81,813 | 0.0% |  |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "Id": "US70975L1070",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2024-04-01",
  "ToDt": "2024-09-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "1481",
  "TtlVolOfTxsExctd": "7579810.38813",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "Sttstcs": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "Id": "US69181V1070",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2023-10-01",
  "ToDt": "2024-03-31",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "2343",
  "TtlVolOfTxsExctd": "2213930.73668",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "Sttstcs": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "Id": "US69181V1070",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "3260",
  "TtlVolOfTxsExctd": "2934048.89022",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": "",
  "Sttstcs": ""
}
```

---

### 📊 FULECR_20250830_R_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 2,454
- **Total Columns**: 16
- **File Size**: 0.2 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| Id | identifier | 0 | 100.0% | IT0005600280, SE0021486180, SE0021922580 |
| FinInstrmClssfctn | text | 0 | 100.0% | SHRS, SHRS, SHRS |
| FrDt | date | 690 | 71.9% | 2024-04-01, 2024-01-01, 2024-04-01 |
| ToDt | date | 690 | 71.9% | 2024-09-30, 2024-06-30, 2024-09-30 |
| Mthdlgy | text | 0 | 100.0% | SINT, SINT, SINT |
| TtlNbOfTxsExctd | numeric | 1,811 | 26.2% | 6, 622, 132 |
| TtlVolOfTxsExctd | numeric | 1,811 | 26.2% | 169.2, 5221.87319, 1689.04639 |
| Lqdty | boolean | 643 | 73.8% | false, false, false |
| AvrgDalyTrnvr | numeric | 643 | 73.8% | 65750.1192, 247.77778, 8461.72962 |
| LrgInScale | numeric | 643 | 73.8% | 30000, 15000, 15000 |
| AvrgDalyNbOfTxs | numeric | 643 | 73.8% | 7, 0.22223, 14.10088 |
| Id_2 | text | 648 | 73.6% | EXGM, ALXP, ALXP |
| AvrgDalyNbOfTxs_2 | numeric | 648 | 73.6% | 7, 0.22223, 16.28719 |
| AvrgTxVal | numeric | 2,438 | 0.7% | 2084.5517, 6988.84091, 3657.14884 |
| StdMktSz | numeric | 2,438 | 0.7% | 10000, 10000, 10000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "Id": "IT0005600280",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2024-04-01",
  "ToDt": "2024-09-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "6",
  "TtlVolOfTxsExctd": "169.2",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "Id": "SE0021486180",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "622",
  "TtlVolOfTxsExctd": "5221.87319",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "Id": "SE0021922580",
  "FinInstrmClssfctn": "SHRS",
  "FrDt": "2024-04-01",
  "ToDt": "2024-09-30",
  "Mthdlgy": "SINT",
  "TtlNbOfTxsExctd": "132",
  "TtlVolOfTxsExctd": "1689.04639",
  "Lqdty": "",
  "AvrgDalyTrnvr": "",
  "LrgInScale": "",
  "AvrgDalyNbOfTxs": "",
  "Id_2": "",
  "AvrgDalyNbOfTxs_2": "",
  "AvrgTxVal": "",
  "StdMktSz": ""
}
```

---

### 📊 FULNCR_20250830_C_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 1
- **Total Columns**: 15
- **File Size**: 0.0 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1 |
| ISIN | identifier | 0 | 100.0% | XS2675718998 |
| Desc | text | 0 | 100.0% | Debt ETC (Exchange traded commodity) |
| CritNm | text | 0 | 100.0% | SACL |
| CritVal | text | 0 | 100.0% | ETC |
| CritNm_2 | text | 0 | 100.0% | ISIN |
| CritVal_2 | identifier | 0 | 100.0% | XS2675718998 |
| FinInstrmClssfctn | text | 0 | 100.0% | ETCS |
| FrDt | date | 0 | 100.0% | 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 900000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 45000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 900000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 45000000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "XS2675718998",
  "Desc": "Debt ETC (Exchange traded commodity)",
  "CritNm": "SACL",
  "CritVal": "ETC",
  "CritNm_2": "ISIN",
  "CritVal_2": "XS2675718998",
  "FinInstrmClssfctn": "ETCS",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "900000",
  "PstTradLrgInScaleThrshld_Amt": "45000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "900000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "45000000"
}
```

---

### 📊 FULNCR_20250830_D_1of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 17
- **File Size**: 46.7 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | XS1273442480, USU9273ADE20, XS1968706520 |
| Desc | text | 29 | 100.0% | Corporate bond, Corporate bond, Corporate bond |
| CritNm | text | 29 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 29 | 100.0% | BOND5, BOND5, BOND5 |
| FinInstrmClssfctn | text | 0 | 100.0% | BOND, BOND, BOND |
| FrDt | date | 25,241 | 95.0% | 2024-01-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 25,241 | 95.0% | 2024-06-30, 2024-06-30, 2024-06-30 |
| TtlNbOfTxsExctd | numeric | 374,043 | 25.2% | 0, 46, 57 |
| TtlVolOfTxsExctd | numeric | 374,043 | 25.2% | 0.00000000000000000, 29748820.1571147578, 48017... |
| Lqdty | boolean | 233,016 | 53.4% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 344,652 | 31.1% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 344,652 | 31.1% | 3500000, 3500000, 3500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 344,652 | 31.1% | 500000, 600000, 600000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 344,652 | 31.1% | 2000000, 2000000, 2000000 |
| CritNm_2 | text | 497,153 | 0.6% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 497,153 | 0.6% | CH1240236740, CH1108675070, CH1108675310 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "XS1273442480",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "TtlNbOfTxsExctd": "0",
  "TtlVolOfTxsExctd": "0.00000000000000000",
  "Lqdty": "",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "USU9273ADE20",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "TtlNbOfTxsExctd": "46",
  "TtlVolOfTxsExctd": "29748820.1571147578",
  "Lqdty": "",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "XS1968706520",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-06-30",
  "TtlNbOfTxsExctd": "57",
  "TtlVolOfTxsExctd": "48017000.0000000000",
  "Lqdty": "",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_D_2of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 17
- **File Size**: 46.04 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | FR001400M8T2, FR001400M8T2, FR001400MA32 |
| Desc | text | 23 | 100.0% | Corporate bond, Corporate bond, Convertible bond |
| CritNm | text | 23 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 23 | 100.0% | BOND5, BOND5, BOND3 |
| FinInstrmClssfctn | text | 0 | 100.0% | BOND, BOND, BOND |
| FrDt | date | 27,220 | 94.6% | 2025-04-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 27,220 | 94.6% | 2025-06-30, 2024-12-31, 2024-03-31 |
| Lqdty | boolean | 207,794 | 58.4% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 343,463 | 31.3% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 343,463 | 31.3% | 3500000, 4000000, 4500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 343,463 | 31.3% | 600000, 700000, 700000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 343,463 | 31.3% | 2000000, 2500000, 2500000 |
| CritNm_2 | text | 496,558 | 0.7% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 496,558 | 0.7% | FR00140048S2, FR001400R1A2, FR001400R682 |
| TtlNbOfTxsExctd | numeric | 415,660 | 16.9% | 0, 0, 0 |
| TtlVolOfTxsExctd | numeric | 415,660 | 16.9% | 0.00000000000000000, 0.00000000000000000, 0.000... |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "FR001400M8T2",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2025-04-01",
  "ToDt": "2025-06-30",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "FR001400M8T2",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "3500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "600000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2000000",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "FR001400MA32",
  "Desc": "Convertible bond",
  "CritNm": "SACL",
  "CritVal": "BOND3",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-03-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

---

### 📊 FULNCR_20250830_D_3of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 17
- **File Size**: 46.62 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | XS2749349564, XS2749349564, XS2749349564 |
| Desc | text | 30 | 100.0% | Corporate bond, Corporate bond, Corporate bond |
| CritNm | text | 30 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 30 | 100.0% | BOND5, BOND5, BOND5 |
| FinInstrmClssfctn | text | 0 | 100.0% | BOND, BOND, BOND |
| FrDt | date | 28,471 | 94.3% | 2023-01-01, 2025-04-01, 2024-01-01 |
| ToDt | date | 28,471 | 94.3% | 2023-12-31, 2025-06-30, 2024-12-31 |
| PreTradLrgInScaleThrshld_Amt | numeric | 345,464 | 30.9% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 345,464 | 30.9% | 3500000, 3500000, 3500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 345,464 | 30.9% | 500000, 600000, 500000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 345,464 | 30.9% | 2000000, 2000000, 2000000 |
| Lqdty | boolean | 234,900 | 53.0% | false, false, false |
| CritNm_2 | text | 496,839 | 0.6% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 496,839 | 0.6% | XS2821784274, XS2821784514, XS2822525114 |
| TtlNbOfTxsExctd | numeric | 374,041 | 25.2% | 10, 0, 0 |
| TtlVolOfTxsExctd | numeric | 374,041 | 25.2% | 16707872.7843561564, 0.00000000000000000, 0.000... |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "XS2749349564",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "3500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "500000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2000000",
  "Lqdty": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "XS2749349564",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2025-04-01",
  "ToDt": "2025-06-30",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "Lqdty": "false",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "XS2749349564",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "3500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "600000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2000000",
  "Lqdty": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

---

### 📊 FULNCR_20250830_D_4of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 17
- **File Size**: 46.05 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | FR0013480167, FR0013480407, FR0013480407 |
| Desc | text | 58 | 100.0% | Corporate bond, Corporate bond, Corporate bond |
| CritNm | text | 58 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 58 | 100.0% | BOND5, BOND5, BOND5 |
| FinInstrmClssfctn | text | 0 | 100.0% | BOND, BOND, BOND |
| FrDt | date | 26,815 | 94.6% | 2024-01-01, 2024-01-01, 2022-01-01 |
| ToDt | date | 26,815 | 94.6% | 2024-12-31, 2024-03-31, 2022-12-31 |
| PreTradLrgInScaleThrshld_Amt | numeric | 343,258 | 31.4% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 343,258 | 31.4% | 3500000, 3500000, 4000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 343,258 | 31.4% | 600000, 600000, 700000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 343,258 | 31.4% | 2000000, 2000000, 2500000 |
| Lqdty | boolean | 208,255 | 58.4% | false, false, false |
| CritNm_2 | text | 496,554 | 0.7% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 496,554 | 0.7% | FR001400FV77, FR001400FW27, FR001400FYK7 |
| TtlNbOfTxsExctd | numeric | 415,422 | 16.9% | 3, 0, 0 |
| TtlVolOfTxsExctd | numeric | 415,422 | 16.9% | 374000.000000000000, 0.00000000000000000, 0.000... |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "FR0013480167",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "3500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "600000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2000000",
  "Lqdty": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "FR0013480407",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-01-01",
  "ToDt": "2024-03-31",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "Lqdty": "false",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "FR0013480407",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "3500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "600000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2000000",
  "Lqdty": "",
  "CritNm_2": "",
  "CritVal_2": "",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

---

### 📊 FULNCR_20250830_D_5of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 22,378
- **Total Columns**: 15
- **File Size**: 1.92 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | XS2398661319, XS2398661319, XS2398661319 |
| Desc | text | 0 | 100.0% | Corporate bond, Corporate bond, Corporate bond |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | BOND5, BOND5, BOND5 |
| FinInstrmClssfctn | text | 0 | 100.0% | BOND, BOND, BOND |
| FrDt | date | 3,535 | 84.2% | 2024-04-01, 2024-07-01, 2024-10-01 |
| ToDt | date | 3,535 | 84.2% | 2024-06-30, 2024-09-30, 2024-12-31 |
| Lqdty | boolean | 7,771 | 65.3% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 14,144 | 36.8% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 14,144 | 36.8% | 3500000, 3500000, 3500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 14,144 | 36.8% | 600000, 500000, 600000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 14,144 | 36.8% | 2000000, 2000000, 2000000 |
| CritNm_2 | text | 21,985 | 1.8% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 21,985 | 1.8% | XS2399365399, XS2451856269, XS2453375409 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "XS2398661319",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-04-01",
  "ToDt": "2024-06-30",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "XS2398661319",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-07-01",
  "ToDt": "2024-09-30",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "XS2398661319",
  "Desc": "Corporate bond",
  "CritNm": "SACL",
  "CritVal": "BOND5",
  "FinInstrmClssfctn": "BOND",
  "FrDt": "2024-10-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "",
  "PstTradLrgInScaleThrshld_Amt": "",
  "PreTradInstrmSzSpcfcThrshld_Amt": "",
  "PstTradInstrmSzSpcfcThrshld_Amt": "",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_E_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 115,762
- **Total Columns**: 17
- **File Size**: 12.74 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | CH0496484640, ANN5639Y5530, CH0011763080 |
| Desc | text | 0 | 100.0% | Debt ETN (Exchange traded notes), Debt ETN (Exc... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | ETN, ETN, SDRV |
| CritNm_2 | text | 114,636 | 1.0% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 114,636 | 1.0% | CH0496484640, ANN5639Y5530, CH0019046140 |
| FinInstrmClssfctn | text | 0 | 100.0% | ETNS, ETNS, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 9 | 100.0% | false, false, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2 | 100.0% | 900000, 900000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2 | 100.0% | 45000000, 45000000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2 | 100.0% | 900000, 900000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2 | 100.0% | 45000000, 45000000, 90000 |
| TtlNbOfTxsExctd | numeric | 115,760 | 0.0% | 0, 58 |
| TtlVolOfTxsExctd | numeric | 115,760 | 0.0% | 0.00000000000000000, 6405274.18600000000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "CH0496484640",
  "Desc": "Debt ETN (Exchange traded notes)",
  "CritNm": "SACL",
  "CritVal": "ETN",
  "CritNm_2": "ISIN",
  "CritVal_2": "CH0496484640",
  "FinInstrmClssfctn": "ETNS",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "900000",
  "PstTradLrgInScaleThrshld_Amt": "45000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "900000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "45000000",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "ANN5639Y5530",
  "Desc": "Debt ETN (Exchange traded notes)",
  "CritNm": "SACL",
  "CritVal": "ETN",
  "CritNm_2": "ISIN",
  "CritVal_2": "ANN5639Y5530",
  "FinInstrmClssfctn": "ETNS",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "900000",
  "PstTradLrgInScaleThrshld_Amt": "45000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "900000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "45000000",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "CH0011763080",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "CritNm_2": "",
  "CritVal_2": "",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "TtlNbOfTxsExctd": "",
  "TtlVolOfTxsExctd": ""
}
```

---

### 📊 FULNCR_20250830_F_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 340,242
- **Total Columns**: 29
- **File Size**: 53.23 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | BEEN20114540, BEEN20114540, BEEN25019280 |
| Desc | text | 0 | 100.0% | Stock dividend futures/forwards, Stock dividend... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD06, EQD06, EQD06 |
| CritNm_2 | text | 2,607 | 99.2% | UINS, UINS, UINS |
| CritVal_2 | identifier | 2,607 | 99.2% | BE0974320526, BE0974320526, BE0003797140 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2024-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2024-12-31, 2022-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 1,102 | 99.7% | 25000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 1,102 | 99.7% | 450000, 450000, 450000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 1,102 | 99.7% | 20000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 1,102 | 99.7% | 400000, 400000, 400000 |
| CritNm_3 | text | 208,695 | 38.7% | FSPD, FSPD, NCCO |
| CritVal_3 | text | 208,695 | 38.7% | TTFG, TTFG, EUR |
| CritNm_4 | text | 209,035 | 38.6% | DCSL, DCSL, TTMB |
| CritVal_4 | text | 209,035 | 38.6% | 21YNL----TTF---1, 21YNL----TTF---1, 1 |
| CritNm_5 | text | 212,497 | 37.5% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 212,497 | 37.5% | EUR, EUR, EUR |
| CritNm_6 | text | 229,131 | 32.7% | TTMB, TTMB, TTMB |
| CritVal_6 | text | 229,131 | 32.7% | 3, 2, 2 |
| CritNm_7 | text | 338,056 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 338,056 | 0.6% | 10, 10, 6 |
| PreTradLrgInScaleThrshld_Nb | numeric | 339,140 | 0.3% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 339,140 | 0.3% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 339,140 | 0.3% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 339,140 | 0.3% | 100000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "BEEN20114540",
  "Desc": "Stock dividend futures/forwards",
  "CritNm": "SACL",
  "CritVal": "EQD06",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0974320526",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "450000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "400000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "BEEN20114540",
  "Desc": "Stock dividend futures/forwards",
  "CritNm": "SACL",
  "CritVal": "EQD06",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0974320526",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "450000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "400000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "BEEN25019280",
  "Desc": "Stock dividend futures/forwards",
  "CritNm": "SACL",
  "CritVal": "EQD06",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0003797140",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "450000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "400000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

---

### 📊 FULNCR_20250830_H_1of3_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 21
- **File Size**: 68.47 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZ0JHV40BZ40, EZ0JHW066ZM0, EZ0JHW066ZM0 |
| Desc | text | 0 | 100.0% | Swaptions, Swaptions, Swaptions |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD05, IRD05, IRD05 |
| CritNm_2 | text | 56 | 100.0% | UTYP, UTYP, UTYP |
| CritVal_2 | text | 56 | 100.0% | XFSC, XFSC, XFSC |
| CritNm_3 | text | 368 | 99.9% | NCSW, NCSW, NCSW |
| CritVal_3 | text | 368 | 99.9% | EUR, EUR, EUR |
| CritNm_4 | text | 368 | 99.9% | TTMO, TTMO, TTMO |
| CritVal_4 | numeric | 368 | 99.9% | 1, 1, 1 |
| CritNm_5 | text | 99,902 | 80.0% | TTMS, TTMS, TTMS |
| CritVal_5 | numeric | 99,902 | 80.0% | 28, 7, 7 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZ0JHV40BZ40",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "1",
  "CritNm_5": "TTMS",
  "CritVal_5": "28",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZ0JHW066ZM0",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "1",
  "CritNm_5": "TTMS",
  "CritVal_5": "7",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZ0JHW066ZM0",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "1",
  "CritNm_5": "TTMS",
  "CritVal_5": "7",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

---

### 📊 FULNCR_20250830_H_2of3_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 21
- **File Size**: 68.48 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZ2NM0N22L64, EZ2NM0N22L64, EZ2NMGG7TN34 |
| Desc | text | 0 | 100.0% | Swaptions, Swaptions, Swaptions |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD05, IRD05, IRD05 |
| CritNm_2 | text | 48 | 100.0% | UTYP, UTYP, UTYP |
| CritVal_2 | text | 48 | 100.0% | XFSC, XFSC, XFSC |
| CritNm_3 | text | 365 | 99.9% | NCSW, NCSW, NCSW |
| CritVal_3 | text | 365 | 99.9% | EUR, EUR, AED |
| CritNm_4 | text | 365 | 99.9% | TTMO, TTMO, TTMO |
| CritVal_4 | numeric | 365 | 99.9% | 1, 1, 3 |
| CritNm_5 | text | 100,550 | 79.9% | TTMS, TTMS, TTMS |
| CritVal_5 | numeric | 100,550 | 79.9% | 6, 6, 8 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2024-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2024-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZ2NM0N22L64",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "1",
  "CritNm_5": "TTMS",
  "CritVal_5": "6",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZ2NM0N22L64",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "1",
  "CritNm_5": "TTMS",
  "CritVal_5": "6",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZ2NMGG7TN34",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "AED",
  "CritNm_4": "TTMO",
  "CritVal_4": "3",
  "CritNm_5": "TTMS",
  "CritVal_5": "8",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

---

### 📊 FULNCR_20250830_H_3of3_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 241,475
- **Total Columns**: 21
- **File Size**: 33.01 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZ1N5T3GVNL8, EZ1N5T3GVNL8, EZ1N5W9JTWC8 |
| Desc | text | 0 | 100.0% | Swaptions, Swaptions, Swaptions |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD05, IRD05, IRD05 |
| CritNm_2 | text | 19 | 100.0% | UTYP, UTYP, UTYP |
| CritVal_2 | text | 19 | 100.0% | XFSC, XFSC, XFSC |
| CritNm_3 | text | 145 | 99.9% | NCSW, NCSW, NCSW |
| CritVal_3 | text | 145 | 99.9% | EUR, EUR, EUR |
| CritNm_4 | text | 145 | 99.9% | TTMO, TTMO, TTMO |
| CritVal_4 | numeric | 145 | 99.9% | 5, 5, 4 |
| CritNm_5 | text | 48,090 | 80.1% | TTMS, TTMS, TTMS |
| CritVal_5 | numeric | 48,090 | 80.1% | 33, 33, 6 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2024-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZ1N5T3GVNL8",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "5",
  "CritNm_5": "TTMS",
  "CritVal_5": "33",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZ1N5T3GVNL8",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "5",
  "CritNm_5": "TTMS",
  "CritVal_5": "33",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZ1N5W9JTWC8",
  "Desc": "Swaptions",
  "CritNm": "SACL",
  "CritVal": "IRD05",
  "CritNm_2": "UTYP",
  "CritVal_2": "XFSC",
  "CritNm_3": "NCSW",
  "CritVal_3": "EUR",
  "CritNm_4": "TTMO",
  "CritVal_4": "4",
  "CritNm_5": "TTMS",
  "CritVal_5": "6",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000"
}
```

---

### 📊 FULNCR_20250830_I_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 4
- **Total Columns**: 13
- **File Size**: 0.0 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EU000A2QMW50, EU000A2QMW50, EU000A2QMW50 |
| Desc | text | 0 | 100.0% | Emission allowances - EUA, Emission allowances ... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EA01, EA01, EA01 |
| FinInstrmClssfctn | text | 0 | 100.0% | EMAL, EMAL, EMAL |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Nb | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 0 | 100.0% | 400000, 300000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 0 | 100.0% | 200000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EU000A2QMW50",
  "Desc": "Emission allowances - EUA",
  "CritNm": "SACL",
  "CritVal": "EA01",
  "FinInstrmClssfctn": "EMAL",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Nb": "100000",
  "PstTradLrgInScaleThrshld_Nb": "400000",
  "PreTradInstrmSzSpcfcThrshld_Nb": "100000",
  "PstTradInstrmSzSpcfcThrshld_Nb": "200000"
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EU000A2QMW50",
  "Desc": "Emission allowances - EUA",
  "CritNm": "SACL",
  "CritVal": "EA01",
  "FinInstrmClssfctn": "EMAL",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Nb": "100000",
  "PstTradLrgInScaleThrshld_Nb": "300000",
  "PreTradInstrmSzSpcfcThrshld_Nb": "100000",
  "PstTradInstrmSzSpcfcThrshld_Nb": "100000"
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EU000A2QMW50",
  "Desc": "Emission allowances - EUA",
  "CritNm": "SACL",
  "CritVal": "EA01",
  "FinInstrmClssfctn": "EMAL",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Nb": "100000",
  "PstTradLrgInScaleThrshld_Nb": "100000",
  "PreTradInstrmSzSpcfcThrshld_Nb": "100000",
  "PstTradInstrmSzSpcfcThrshld_Nb": "100000"
}
```

---

### 📊 FULNCR_20250830_J_1of1_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 86,545
- **Total Columns**: 23
- **File Size**: 12.55 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZ0LKWN8JY60, EZ03XH4JDY30, EZ03XH4JDY30 |
| Desc | text | 0 | 100.0% | Deliverable forwards, Interet Rate Futures/Forw... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | FEX02, IRD03, IRD03 |
| CritNm_2 | text | 6,473 | 92.5% | FNC1, UIRT, UIRT |
| CritVal_2 | text | 6,473 | 92.5% | CHF, EURI, EURI |
| CritNm_3 | text | 6,490 | 92.5% | FNC2, IRTC, IRTC |
| CritVal_3 | text | 6,490 | 92.5% | USD, 6MNTH, 6MNTH |
| CritNm_4 | text | 6,617 | 92.3% | TTMB, TTMB, TTMB |
| CritVal_4 | text | 6,617 | 92.3% | 3, 2, 1 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 10000000, 10000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 25000000, 25000000, 25000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 5000000, 5000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 20000000, 20000000, 20000000 |
| CritNm_5 | text | 85,750 | 0.9% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 85,750 | 0.9% | EUR, EUR, EUR |
| CritNm_6 | text | 85,764 | 0.9% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 85,764 | 0.9% | 1, 1, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZ0LKWN8JY60",
  "Desc": "Deliverable forwards",
  "CritNm": "SACL",
  "CritVal": "FEX02",
  "CritNm_2": "FNC1",
  "CritVal_2": "CHF",
  "CritNm_3": "FNC2",
  "CritVal_3": "USD",
  "CritNm_4": "TTMB",
  "CritVal_4": "3",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "25000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "20000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZ03XH4JDY30",
  "Desc": "Interet Rate Futures/Forward",
  "CritNm": "SACL",
  "CritVal": "IRD03",
  "CritNm_2": "UIRT",
  "CritVal_2": "EURI",
  "CritNm_3": "IRTC",
  "CritVal_3": "6MNTH",
  "CritNm_4": "TTMB",
  "CritVal_4": "2",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "10000000",
  "PstTradLrgInScaleThrshld_Amt": "25000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "20000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZ03XH4JDY30",
  "Desc": "Interet Rate Futures/Forward",
  "CritNm": "SACL",
  "CritVal": "IRD03",
  "CritNm_2": "UIRT",
  "CritVal_2": "EURI",
  "CritNm_3": "IRTC",
  "CritVal_3": "6MNTH",
  "CritNm_4": "TTMB",
  "CritVal_4": "1",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "10000000",
  "PstTradLrgInScaleThrshld_Amt": "25000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "20000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

---

### 📊 FULNCR_20250830_O_10of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.86 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000F2Q0ES7, DE000F2Q0EX7, DE000F2Q0F27 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 3,210 | 99.4% | UINS, UINS, UINS |
| CritVal_2 | identifier | 3,210 | 99.4% | GB00BP6MXD84, GB00BP6MXD84, DE0007037129 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2024-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,463 | 99.5% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,463 | 99.5% | 5500000, 5500000, 5500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,463 | 99.5% | 1000000, 1000000, 1000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,463 | 99.5% | 5000000, 5000000, 5000000 |
| CritNm_3 | text | 465,175 | 7.0% | IRTC, IRTC, IRTC |
| CritVal_3 | text | 465,175 | 7.0% | 3MNTH, 3MNTH, 3MNTH |
| CritNm_4 | text | 467,249 | 6.5% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 467,249 | 6.5% | 1, 1, 1 |
| CritNm_5 | text | 473,303 | 5.3% | TTMB, TTMB, TTMB |
| CritVal_5 | numeric | 473,303 | 5.3% | 1, 1, 1 |
| CritNm_6 | text | 474,981 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 474,981 | 5.0% | 4, 3, 3 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,537 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,537 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,537 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,537 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,799 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,799 | 0.6% | 6, 6, 6 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000F2Q0ES7",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB00BP6MXD84",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000F2Q0EX7",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB00BP6MXD84",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000F2Q0F27",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE0007037129",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_11of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.92 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000F16CML8, DE000F16CMZ8, DE000F16CN08 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 3,188 | 99.4% | UINS, UINS, UINS |
| CritVal_2 | identifier | 3,188 | 99.4% | FR0000120628, CH0009002962, GB0031348658 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,439 | 99.5% | 1500000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,439 | 99.5% | 5500000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,439 | 99.5% | 1000000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,439 | 99.5% | 5000000, 1000000, 1000000 |
| CritNm_3 | text | 467,102 | 6.6% | TTMB, TTMB, TTMB |
| CritVal_3 | text | 467,102 | 6.6% | 1, 1, 1 |
| CritNm_4 | text | 468,473 | 6.3% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 468,473 | 6.3% | 3, 3, 2 |
| CritNm_5 | text | 473,418 | 5.3% | TTMB, TTMB, TTMB |
| CritVal_5 | numeric | 473,418 | 5.3% | 3, 1, 1 |
| CritNm_6 | text | 475,097 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,097 | 5.0% | 1, 2, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,870 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,870 | 0.6% | 10, 9, 10 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000F16CML8",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0000120628",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000F16CMZ8",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "CH0009002962",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000F16CN08",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB0031348658",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_12of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 27
- **File Size**: 66.14 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000C76T169, DE000C76T219, DE000C76T2P9 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 722 | 99.9% | UINS, UINS, UINS |
| CritVal_2 | identifier | 722 | 99.9% | FR0010411983, FR0010411983, FR0010411983 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 30 | 100.0% | 25000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 30 | 100.0% | 1250000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 30 | 100.0% | 20000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 30 | 100.0% | 1000000, 1000000, 1000000 |
| CritNm_3 | text | 488,650 | 2.3% | FNC2, FNC2, FNC2 |
| CritVal_3 | text | 488,650 | 2.3% | AUD, EUR, EUR |
| CritNm_4 | text | 491,683 | 1.7% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 491,683 | 1.7% | 1, 2, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 499,970 | 0.0% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 499,970 | 0.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 499,970 | 0.0% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 499,970 | 0.0% | 100000, 100000, 100000 |
| CritNm_5 | text | 498,308 | 0.3% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 498,308 | 0.3% | EUR, EUR, EUR |
| CritNm_6 | text | 499,994 | 0.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 499,994 | 0.0% | 2, 1, 2 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000C76T169",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0010411983",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000C76T219",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0010411983",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000C76T2P9",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0010411983",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": ""
}
```

---

### 📊 FULNCR_20250830_O_13of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 90,477
- **Total Columns**: 27
- **File Size**: 12.48 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | NLEX01215709, NLEX01215709, NLEX01215899 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 1,919 | 97.9% | UINS, UINS, UINS |
| CritVal_2 | identifier | 1,919 | 97.9% | GB00B10RZP78, GB00B10RZP78, GB00B10RZP78 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2024-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2024-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 1,919 | 97.9% | 1500000, 1500000, 1500000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 1,919 | 97.9% | 5500000, 5500000, 5500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 1,919 | 97.9% | 1000000, 1000000, 1000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 1,919 | 97.9% | 5000000, 5000000, 5000000 |
| CritNm_3 | text | 74,020 | 18.2% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 74,020 | 18.2% | NCGG, NCGG, NCGG |
| CritNm_4 | text | 74,020 | 18.2% | DCSL, DCSL, DCSL |
| CritVal_4 | text | 74,020 | 18.2% | 37Y005053MH0000R, 37Y005053MH0000R, 37Y005053MH... |
| CritNm_5 | text | 74,020 | 18.2% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 74,020 | 18.2% | EUR, EUR, EUR |
| CritNm_6 | text | 74,020 | 18.2% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 74,020 | 18.2% | 1, 1, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 88,558 | 2.1% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 88,558 | 2.1% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 88,558 | 2.1% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 88,558 | 2.1% | 100000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "NLEX01215709",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB00B10RZP78",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "NLEX01215709",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB00B10RZP78",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "NLEX01215899",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "GB00B10RZP78",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

---

### 📊 FULNCR_20250830_O_1of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.39 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | BEEX00170510, BEEX00170650, BEEX00170700 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 1,316 | 99.7% | UINS, UINS, UINS |
| CritVal_2 | identifier | 1,316 | 99.7% | BE0974276082, BE0003565737, BE0003739530 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 558 | 99.9% | 25000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 558 | 99.9% | 1250000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 558 | 99.9% | 20000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 558 | 99.9% | 1000000, 1000000, 1000000 |
| CritNm_3 | text | 479,390 | 4.1% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 479,390 | 4.1% | BSLD, BSLD, BSLD |
| CritNm_4 | text | 482,547 | 3.5% | DCSL, DCSL, DCSL |
| CritVal_4 | text | 482,547 | 3.5% | 10YDE-RWENET---I, 10YDE-RWENET---I, 10YDE-RWENE... |
| CritNm_5 | text | 489,764 | 2.0% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 489,764 | 2.0% | EUR, EUR, EUR |
| CritNm_6 | text | 491,457 | 1.7% | TTMB, TTMB, TTMB |
| CritVal_6 | text | 491,457 | 1.7% | 2, 2, 2 |
| CritNm_7 | text | 496,823 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,823 | 0.6% | 2, 1, 10 |
| PreTradLrgInScaleThrshld_Nb | numeric | 499,442 | 0.1% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 499,442 | 0.1% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 499,442 | 0.1% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 499,442 | 0.1% | 100000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "BEEX00170510",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0974276082",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "BEEX00170650",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0003565737",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "BEEX00170700",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "BE0003739530",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

---

### 📊 FULNCR_20250830_O_2of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 68.11 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | NLEX01444010, NLEX01444150, NLEX01444200 |
| Desc | text | 0 | 100.0% | Stock index options, Stock index options, Stock... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD01, EQD01, EQD01 |
| CritNm_2 | text | 2,735 | 99.5% | UINS, UINS, UINS |
| CritVal_2 | identifier | 2,735 | 99.5% | NL0000000107, NL0000000107, NL0000000107 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2024-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,499 | 99.5% | 20000000, 20000000, 20000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,499 | 99.5% | 160000000, 160000000, 160000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,499 | 99.5% | 15000000, 15000000, 15000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,499 | 99.5% | 150000000, 150000000, 150000000 |
| CritNm_3 | text | 462,923 | 7.4% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 462,923 | 7.4% | BSLD, BSLD, BSLD |
| CritNm_4 | text | 466,110 | 6.8% | DCSL, DCSL, DCSL |
| CritVal_4 | text | 466,110 | 6.8% | 10YFR-RTE------C, 10YFR-RTE------C, 10YIT-GRTN-... |
| CritNm_5 | text | 473,458 | 5.3% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 473,458 | 5.3% | EUR, EUR, EUR |
| CritNm_6 | text | 475,121 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,121 | 5.0% | 2, 1, 2 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,501 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,501 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,501 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,501 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,864 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,864 | 0.6% | 1, 1, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "NLEX01444010",
  "Desc": "Stock index options",
  "CritNm": "SACL",
  "CritVal": "EQD01",
  "CritNm_2": "UINS",
  "CritVal_2": "NL0000000107",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "20000000",
  "PstTradLrgInScaleThrshld_Amt": "160000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "15000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "150000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "NLEX01444150",
  "Desc": "Stock index options",
  "CritNm": "SACL",
  "CritVal": "EQD01",
  "CritNm_2": "UINS",
  "CritVal_2": "NL0000000107",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "20000000",
  "PstTradLrgInScaleThrshld_Amt": "160000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "15000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "150000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "NLEX01444200",
  "Desc": "Stock index options",
  "CritNm": "SACL",
  "CritVal": "EQD01",
  "CritNm_2": "UINS",
  "CritVal_2": "NL0000000107",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "20000000",
  "PstTradLrgInScaleThrshld_Amt": "160000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "15000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "150000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_3of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.99 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | NLCBOE073S01, NLCBOE073SG1, NLCBOE073SL1 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 3,034 | 99.4% | UINS, UINS, UINS |
| CritVal_2 | identifier | 3,034 | 99.4% | DE000A0LD6E6, DE000CBK1001, DE000A0JBPG2 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,450 | 99.5% | 25000, 550000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,450 | 99.5% | 1250000, 3000000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,450 | 99.5% | 20000, 500000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,450 | 99.5% | 1000000, 2500000, 1000000 |
| CritNm_3 | text | 467,739 | 6.5% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 467,739 | 6.5% | BSLD, BSLD, BSLD |
| CritNm_4 | text | 470,977 | 5.8% | DCSL, DCSL, DCSL |
| CritVal_4 | text | 470,977 | 5.8% | 10YDE-RWENET---I, 10YDE-RWENET---I, 10YDE-RWENE... |
| CritNm_5 | text | 475,038 | 5.0% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 475,038 | 5.0% | EUR, EUR, EUR |
| CritNm_6 | text | 475,038 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,038 | 5.0% | 1, 2, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,550 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,550 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,550 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,550 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,772 | 0.7% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,772 | 0.7% | 1, 1, 2 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "NLCBOE073S01",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE000A0LD6E6",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "NLCBOE073SG1",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE000CBK1001",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "550000",
  "PstTradLrgInScaleThrshld_Amt": "3000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "500000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2500000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "NLCBOE073SL1",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE000A0JBPG2",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_4of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.95 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | ES0A06058242, ES0A06058382, ES0A06058382 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 3,282 | 99.3% | UINS, UINS, UINS |
| CritVal_2 | identifier | 3,282 | 99.3% | ES0109067019, ES0148396007, ES0148396007 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,491 | 99.5% | 25000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,491 | 99.5% | 1250000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,491 | 99.5% | 20000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,491 | 99.5% | 1000000, 1000000, 1000000 |
| CritNm_3 | text | 464,677 | 7.1% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 464,677 | 7.1% | RPSD, RPSD, RPSD |
| CritNm_4 | text | 467,186 | 6.6% | NCCO, NCCO, NCCO |
| CritVal_4 | text | 467,186 | 6.6% | EUR, EUR, EUR |
| CritNm_5 | text | 473,463 | 5.3% | TTMB, TTMB, TTMB |
| CritVal_5 | numeric | 473,463 | 5.3% | 1, 1, 1 |
| CritNm_6 | text | 475,106 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,106 | 5.0% | 2, 2, 3 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,509 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,509 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,509 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,509 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,891 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,891 | 0.6% | 1, 2, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "ES0A06058242",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "ES0109067019",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "ES0A06058382",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "ES0148396007",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "ES0A06058382",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "ES0148396007",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_5of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.93 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000F1NUFS3, DE000F1NUFX3, DE000F1NUG13 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock index options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD01 |
| CritNm_2 | text | 3,217 | 99.4% | UINS, UINS, UINS |
| CritVal_2 | identifier | 3,217 | 99.4% | ES0173516115, ES0173516115, DE0008469008 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,500 | 99.5% | 300000, 300000, 20000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,500 | 99.5% | 1500000, 1500000, 160000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,500 | 99.5% | 250000, 250000, 15000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,500 | 99.5% | 1250000, 1250000, 150000000 |
| CritNm_3 | text | 464,916 | 7.0% | TTMB, TTMB, TTMB |
| CritVal_3 | text | 464,916 | 7.0% | 1, 1, 1 |
| CritNm_4 | text | 466,896 | 6.6% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 466,896 | 6.6% | 2, 2, 3 |
| CritNm_5 | text | 473,421 | 5.3% | TTMB, TTMB, TTMB |
| CritVal_5 | numeric | 473,421 | 5.3% | 1, 1, 1 |
| CritNm_6 | text | 475,110 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,110 | 5.0% | 1, 1, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,500 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,500 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,500 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,500 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,807 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,807 | 0.6% | 1, 1, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000F1NUFS3",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "ES0173516115",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "300000",
  "PstTradLrgInScaleThrshld_Amt": "1500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "250000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1250000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000F1NUFX3",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "ES0173516115",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "300000",
  "PstTradLrgInScaleThrshld_Amt": "1500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "250000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1250000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000F1NUG13",
  "Desc": "Stock index options",
  "CritNm": "SACL",
  "CritVal": "EQD01",
  "CritNm_2": "UINS",
  "CritVal_2": "DE0008469008",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "20000000",
  "PstTradLrgInScaleThrshld_Amt": "160000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "15000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "150000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_6of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 27
- **File Size**: 66.73 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000F10EYF4, DE000F10EYK4, DE000F10EZ24 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock index options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD01 |
| CritNm_2 | text | 2,674 | 99.5% | UINS, UINS, UINS |
| CritVal_2 | identifier | 2,674 | 99.5% | DE0007030009, DE0007030009, EU0009658442 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 1,931 | 99.6% | 550000, 550000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 1,931 | 99.6% | 3000000, 3000000, 1500000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 1,931 | 99.6% | 500000, 500000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 1,931 | 99.6% | 2500000, 2500000, 1000000 |
| CritNm_3 | text | 475,135 | 5.0% | IRTC, IRTC, IRTC |
| CritVal_3 | text | 475,135 | 5.0% | 3MNTH, 3MNTH, 3MNTH |
| CritNm_4 | text | 477,011 | 4.6% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 477,011 | 4.6% | 4, 4, 3 |
| CritNm_5 | text | 481,969 | 3.6% | TTMB, TTMB, TTMB |
| CritVal_5 | numeric | 481,969 | 3.6% | 1, 1, 1 |
| CritNm_6 | text | 483,614 | 3.3% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 483,614 | 3.3% | 1, 2, 1 |
| PreTradLrgInScaleThrshld_Nb | numeric | 498,069 | 0.4% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 498,069 | 0.4% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 498,069 | 0.4% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 498,069 | 0.4% | 100000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000F10EYF4",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE0007030009",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "550000",
  "PstTradLrgInScaleThrshld_Amt": "3000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "500000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2500000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000F10EYK4",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE0007030009",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "550000",
  "PstTradLrgInScaleThrshld_Amt": "3000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "500000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "2500000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000F10EZ24",
  "Desc": "Stock index options",
  "CritNm": "SACL",
  "CritVal": "EQD01",
  "CritNm_2": "UINS",
  "CritVal_2": "EU0009658442",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

---

### 📊 FULNCR_20250830_O_7of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 67.35 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | SE0022712774, SE0022712824, SE0022712964 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 1,183 | 99.8% | UINS, UINS, UINS |
| CritVal_2 | identifier | 1,183 | 99.8% | SE0007100599, SE0007100599, SE0007100599 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 575 | 99.9% | 25000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 575 | 99.9% | 1250000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 575 | 99.9% | 20000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 575 | 99.9% | 1000000, 1000000, 1000000 |
| CritNm_3 | text | 479,505 | 4.1% | SBPD, SBPD, SBPD |
| CritVal_3 | text | 479,505 | 4.1% | DRYF, DRYF, DRYF |
| CritNm_4 | text | 482,582 | 3.5% | FSPD, FSPD, FSPD |
| CritVal_4 | text | 482,582 | 3.5% | DBCR, DBCR, DBCR |
| CritNm_5 | text | 489,851 | 2.0% | SSRF, SSRF, SSRF |
| CritVal_5 | text | 489,851 | 2.0% | CAPE, CAPE, CAPE |
| CritNm_6 | text | 491,511 | 1.7% | SRTC, SRTC, SRTC |
| CritVal_6 | text | 491,511 | 1.7% | 5TC, 5TC, 5TC |
| CritNm_7 | text | 496,875 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,875 | 0.6% | 10, 10, 10 |
| PreTradLrgInScaleThrshld_Nb | numeric | 499,425 | 0.1% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 499,425 | 0.1% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 499,425 | 0.1% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 499,425 | 0.1% | 100000, 100000, 100000 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "SE0022712774",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "SE0007100599",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "SE0022712824",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "SE0007100599",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "SE0022712964",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "SE0007100599",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": ""
}
```

---

### 📊 FULNCR_20250830_O_8of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 68.09 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | NLCBOE13FOR5, NLCBOE13FOW5, NLCBOE13FOW5 |
| Desc | text | 0 | 100.0% | Stock options, Stock options, Stock options |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, EQD03, EQD03 |
| CritNm_2 | text | 2,874 | 99.4% | UINS, UINS, UINS |
| CritVal_2 | identifier | 2,874 | 99.4% | DE000BAY0017, FR0000120404, FR0000120404 |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,509 | 99.5% | 1500000, 25000, 25000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,509 | 99.5% | 5500000, 1250000, 1250000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,509 | 99.5% | 1000000, 20000, 20000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,509 | 99.5% | 5000000, 1000000, 1000000 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,491 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,491 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,491 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,491 | 0.5% | 100000, 100000, 100000 |
| CritNm_3 | text | 465,138 | 7.0% | FSPD, FSPD, FSPD |
| CritVal_3 | text | 465,138 | 7.0% | BSLD, BSLD, BSLD |
| CritNm_4 | text | 468,313 | 6.3% | DCSL, DCSL, DCSL |
| CritVal_4 | text | 468,313 | 6.3% | 10YIT-GRTN-----B, 10YIT-GRTN-----B, 10YIT-GRTN-... |
| CritNm_5 | text | 473,263 | 5.3% | NCCO, NCCO, NCCO |
| CritVal_5 | text | 473,263 | 5.3% | EUR, EUR, EUR |
| CritNm_6 | text | 474,925 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 474,925 | 5.0% | 2, 1, 2 |
| CritNm_7 | text | 496,799 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,799 | 0.6% | 1, 10, 10 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "NLCBOE13FOR5",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "DE000BAY0017",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1500000",
  "PstTradLrgInScaleThrshld_Amt": "5500000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "5000000",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "NLCBOE13FOW5",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0000120404",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "NLCBOE13FOW5",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "FR0000120404",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_O_9of13_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 29
- **File Size**: 68.0 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | HU0010042666, HU0010042716, HU0010042856 |
| Desc | text | 0 | 100.0% | Stock options, Non-deliverable FX options, Non-... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | EQD03, FEX03, FEX03 |
| CritNm_2 | text | 3,066 | 99.4% | UINS, FNC1, FNC1 |
| CritVal_2 | identifier | 3,066 | 99.4% | HU0000153937, HUF, EUR |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2024-01-01, 2024-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2024-12-31, 2024-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 2,439 | 99.5% | 25000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 2,439 | 99.5% | 1250000, 25000000, 25000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 2,439 | 99.5% | 20000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 2,439 | 99.5% | 1000000, 20000000, 20000000 |
| CritNm_3 | text | 465,898 | 6.8% | FNC2, FNC2, FNC2 |
| CritVal_3 | text | 465,898 | 6.8% | HUF, JPY, JPY |
| CritNm_4 | text | 468,797 | 6.2% | TTMB, TTMB, TTMB |
| CritVal_4 | numeric | 468,797 | 6.2% | 1, 1, 1 |
| CritNm_5 | text | 475,125 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_5 | text | 475,125 | 5.0% | 4, 4, 1 |
| CritNm_6 | text | 475,166 | 5.0% | TTMB, TTMB, TTMB |
| CritVal_6 | numeric | 475,166 | 5.0% | 3, 2, 2 |
| PreTradLrgInScaleThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PstTradLrgInScaleThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| PstTradInstrmSzSpcfcThrshld_Nb | numeric | 497,561 | 0.5% | 100000, 100000, 100000 |
| CritNm_7 | text | 496,867 | 0.6% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 496,867 | 0.6% | 6, 7, 7 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "HU0010042666",
  "Desc": "Stock options",
  "CritNm": "SACL",
  "CritVal": "EQD03",
  "CritNm_2": "UINS",
  "CritVal_2": "HU0000153937",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "25000",
  "PstTradLrgInScaleThrshld_Amt": "1250000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "20000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "1000000",
  "CritNm_3": "",
  "CritVal_3": "",
  "CritNm_4": "",
  "CritVal_4": "",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "HU0010042716",
  "Desc": "Non-deliverable FX options",
  "CritNm": "SACL",
  "CritVal": "FEX03",
  "CritNm_2": "FNC1",
  "CritVal_2": "HUF",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "25000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "20000000",
  "CritNm_3": "FNC2",
  "CritVal_3": "HUF",
  "CritNm_4": "TTMB",
  "CritVal_4": "1",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "HU0010042856",
  "Desc": "Non-deliverable FX options",
  "CritNm": "SACL",
  "CritVal": "FEX03",
  "CritNm_2": "FNC1",
  "CritVal_2": "EUR",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "25000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "20000000",
  "CritNm_3": "FNC2",
  "CritVal_3": "JPY",
  "CritNm_4": "TTMB",
  "CritVal_4": "1",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "PreTradLrgInScaleThrshld_Nb": "",
  "PstTradLrgInScaleThrshld_Nb": "",
  "PreTradInstrmSzSpcfcThrshld_Nb": "",
  "PstTradInstrmSzSpcfcThrshld_Nb": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_R_1of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 15
- **File Size**: 54.25 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | CH1234574700, CH1237804690, CH1237835660 |
| Desc | text | 0 | 100.0% | Securitised derivatives, Securitised derivative... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FinInstrmClssfctn | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 60000, 60000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 50000, 50000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 90000, 90000, 90000 |
| CritNm_2 | text | 499,995 | 0.0% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 499,995 | 0.0% | DE000A0V9YT0, NO0010883010, NO0010825730 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "CH1234574700",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "CH1237804690",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "CH1237835660",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_R_2of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 15
- **File Size**: 54.25 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000HD0NYE2, DE000HD0NZ32, DE000HD0NZH2 |
| Desc | text | 0 | 100.0% | Securitised derivatives, Securitised derivative... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FinInstrmClssfctn | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 60000, 60000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 50000, 50000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 90000, 90000, 90000 |
| CritNm_2 | text | 499,996 | 0.0% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 499,996 | 0.0% | NO0010867542, NO0010883002, NO0010792112 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000HD0NYE2",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000HD0NZ32",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000HD0NZH2",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_R_3of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 15
- **File Size**: 54.25 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000MG2JYT4, DE000MG2JYY4, DE000MG2JZ54 |
| Desc | text | 0 | 100.0% | Securitised derivatives, Securitised derivative... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FinInstrmClssfctn | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 60000, 60000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 50000, 50000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 90000, 90000, 90000 |
| CritNm_2 | text | 499,991 | 0.0% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 499,991 | 0.0% | NO0010824444, NO0010792195, NO0010796105 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000MG2JYT4",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000MG2JYY4",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000MG2JZ54",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_R_4of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 15
- **File Size**: 54.25 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000GQ20ZD7, DE000GQ211F7, DE000GQ212J7 |
| Desc | text | 0 | 100.0% | Securitised derivatives, Securitised derivative... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FinInstrmClssfctn | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 1 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 60000, 60000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 50000, 50000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 90000, 90000, 90000 |
| CritNm_2 | text | 499,995 | 0.0% | ISIN, ISIN, ISIN |
| CritVal_2 | identifier | 499,995 | 0.0% | NO0010847817, NO0010867567, DE000A0V9YU8 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000GQ20ZD7",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000GQ211F7",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000GQ212J7",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_R_5of5_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 93,581
- **Total Columns**: 15
- **File Size**: 10.07 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | DE000MG0M4M9, DE000MG0M509, DE000MG0M5B9 |
| Desc | text | 0 | 100.0% | Securitised derivatives, Securitised derivative... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FinInstrmClssfctn | text | 0 | 100.0% | SDRV, SDRV, SDRV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2022-01-01, 2022-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2022-12-31, 2022-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, true, true |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 60000, 60000, 60000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 100000, 100000, 100000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 50000, 50000, 50000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 90000, 90000, 90000 |
| CritNm_2 | text | 93,579 | 0.0% | ISIN, ISIN |
| CritVal_2 | identifier | 93,579 | 0.0% | NO0010882129, NO0010883069 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "DE000MG0M4M9",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "DE000MG0M509",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "DE000MG0M5B9",
  "Desc": "Securitised derivatives",
  "CritNm": "SACL",
  "CritVal": "SDRV",
  "FinInstrmClssfctn": "SDRV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "60000",
  "PstTradLrgInScaleThrshld_Amt": "100000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "50000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "90000",
  "CritNm_2": "",
  "CritVal_2": ""
}
```

---

### 📊 FULNCR_20250830_S_1of4_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 25
- **File Size**: 79.62 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZ0JHW59N560, EZ0JJ5S5TP40, EZ0JJ5S5TP40 |
| Desc | text | 0 | 100.0% | Swaps and futures/forwards on swaps, Swaps and ... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD06, IRD06, IRD06 |
| CritNm_2 | text | 411 | 99.9% | INC1, INC1, INC1 |
| CritVal_2 | text | 411 | 99.9% | CHF, EUR, EUR |
| CritNm_3 | text | 411 | 99.9% | TTMB, TTMB, TTMB |
| CritVal_3 | text | 411 | 99.9% | 5, 1, 1 |
| CritNm_4 | text | 424 | 99.9% | UTYP, UTYP, UTYP |
| CritVal_4 | text | 424 | 99.9% | OSSC, XFSC, XFSC |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |
| CritNm_5 | text | 480,478 | 3.9% | UTYP, UTYP, UTYP |
| CritVal_5 | text | 480,478 | 3.9% | FFMC, FFMC, FFMC |
| CritNm_6 | text | 499,988 | 0.0% | DTYP, DTYP, DTYP |
| CritVal_6 | text | 499,988 | 0.0% | CASH, CASH, CASH |
| CritNm_7 | text | 499,988 | 0.0% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 499,988 | 0.0% | 2, 1, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZ0JHW59N560",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "CHF",
  "CritNm_3": "TTMB",
  "CritVal_3": "5",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZ0JJ5S5TP40",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "1",
  "CritNm_4": "UTYP",
  "CritVal_4": "XFSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZ0JJ5S5TP40",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "1",
  "CritNm_4": "UTYP",
  "CritVal_4": "XFSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_S_2of4_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 25
- **File Size**: 79.62 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZT2QPKMSLV2, EZT2QPKMSLV2, EZT2R5038YT2 |
| Desc | text | 0 | 100.0% | Swaps and futures/forwards on swaps, Swaps and ... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD06, IRD06, IRD06 |
| CritNm_2 | text | 430 | 99.9% | INC1, INC1, INC1 |
| CritVal_2 | text | 430 | 99.9% | EUR, EUR, EUR |
| CritNm_3 | text | 430 | 99.9% | TTMB, TTMB, TTMB |
| CritVal_3 | numeric | 430 | 99.9% | 2, 1, 17 |
| CritNm_4 | text | 438 | 99.9% | UTYP, UTYP, UTYP |
| CritVal_4 | text | 438 | 99.9% | OSSC, OSSC, OSSC |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2024-01-01, 2023-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2024-12-31, 2023-12-31 |
| Lqdty | boolean | 0 | 100.0% | true, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 1025000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 4025000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 55000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 3550000000, 9000000, 9000000 |
| CritNm_5 | text | 480,702 | 3.9% | UTYP, UTYP, UTYP |
| CritVal_5 | text | 480,702 | 3.9% | FFMC, FFMC, FFMC |
| CritNm_6 | text | 499,995 | 0.0% | DTYP, DTYP, DTYP |
| CritVal_6 | text | 499,995 | 0.0% | CASH, CASH, CASH |
| CritNm_7 | text | 499,995 | 0.0% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 499,995 | 0.0% | 9, 1, 10 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZT2QPKMSLV2",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "2",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "PreTradLrgInScaleThrshld_Amt": "1025000000",
  "PstTradLrgInScaleThrshld_Amt": "4025000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "55000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "3550000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZT2QPKMSLV2",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "1",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZT2R5038YT2",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "17",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_S_3of4_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 500,000
- **Total Columns**: 25
- **File Size**: 79.62 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZJ2GFKQGW75, EZJ2GFKQGW75, EZJ2GFKQGW75 |
| Desc | text | 0 | 100.0% | Swaps and futures/forwards on swaps, Swaps and ... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD06, IRD06, IRD06 |
| CritNm_2 | text | 434 | 99.9% | INC1, INC1, INC1 |
| CritVal_2 | text | 434 | 99.9% | EUR, EUR, EUR |
| CritNm_3 | text | 434 | 99.9% | TTMB, TTMB, TTMB |
| CritVal_3 | text | 434 | 99.9% | 8, 7, 7 |
| CritNm_4 | text | 442 | 99.9% | UTYP, UTYP, UTYP |
| CritVal_4 | text | 442 | 99.9% | OSSC, OSSC, OSSC |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2022-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2022-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |
| CritNm_5 | text | 480,560 | 3.9% | UTYP, UTYP, UTYP |
| CritVal_5 | text | 480,560 | 3.9% | FFMC, XFMC, FFMC |
| CritNm_6 | text | 499,993 | 0.0% | DTYP, DTYP, DTYP |
| CritVal_6 | text | 499,993 | 0.0% | CASH, CASH, CASH |
| CritNm_7 | text | 499,993 | 0.0% | TTMB, TTMB, TTMB |
| CritVal_7 | numeric | 499,993 | 0.0% | 1, 8, 5 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZJ2GFKQGW75",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "8",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2022-01-01",
  "ToDt": "2022-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZJ2GFKQGW75",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "7",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZJ2GFKQGW75",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "7",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

### 📊 FULNCR_20250830_S_4of4_fitrs_data.csv

- **Instrument Type**: Unknown
- **Total Rows**: 290,247
- **Total Columns**: 25
- **File Size**: 46.18 MB

#### Column Structure

| Column Name | Data Type | Null Count | Fill Rate % | Sample Values |
|-------------|-----------|------------|-------------|---------------|
| TechRcrdId | numeric | 0 | 100.0% | 1, 2, 3 |
| ISIN | identifier | 0 | 100.0% | EZFV5BSJ9D28, EZFV5H8C6V68, EZFV5H8C6V68 |
| Desc | text | 0 | 100.0% | Swaps and futures/forwards on swaps, Swaps and ... |
| CritNm | text | 0 | 100.0% | SACL, SACL, SACL |
| CritVal | text | 0 | 100.0% | IRD06, IRD06, IRD06 |
| CritNm_2 | text | 227 | 99.9% | INC1, INC1, INC1 |
| CritVal_2 | text | 227 | 99.9% | EUR, EUR, EUR |
| CritNm_3 | text | 227 | 99.9% | TTMB, TTMB, TTMB |
| CritVal_3 | text | 227 | 99.9% | 26, 5, 4 |
| CritNm_4 | text | 232 | 99.9% | UTYP, UTYP, UTYP |
| CritVal_4 | text | 232 | 99.9% | OSSC, IFSC, IFSC |
| FinInstrmClssfctn | text | 0 | 100.0% | DERV, DERV, DERV |
| FrDt | date | 0 | 100.0% | 2023-01-01, 2023-01-01, 2024-01-01 |
| ToDt | date | 0 | 100.0% | 2023-12-31, 2023-12-31, 2024-12-31 |
| Lqdty | boolean | 0 | 100.0% | false, false, false |
| PreTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 5000000, 5000000, 5000000 |
| PstTradLrgInScaleThrshld_Amt | numeric | 0 | 100.0% | 10000000, 10000000, 10000000 |
| PreTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 4000000, 4000000, 4000000 |
| PstTradInstrmSzSpcfcThrshld_Amt | numeric | 0 | 100.0% | 9000000, 9000000, 9000000 |
| CritNm_5 | text | 278,856 | 3.9% | UTYP, UTYP, UTYP |
| CritVal_5 | text | 278,856 | 3.9% | FFMC, FFMC, FFMC |
| CritNm_6 | text | 290,245 | 0.0% | DTYP, DTYP |
| CritVal_6 | text | 290,245 | 0.0% | PHYS, PHYS |
| CritNm_7 | text | 290,245 | 0.0% | TTMB, TTMB |
| CritVal_7 | numeric | 290,245 | 0.0% | 1, 1 |

#### First 3 Rows Sample

```json
// Row 1
{
  "TechRcrdId": "1",
  "ISIN": "EZFV5BSJ9D28",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "26",
  "CritNm_4": "UTYP",
  "CritVal_4": "OSSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 2
{
  "TechRcrdId": "2",
  "ISIN": "EZFV5H8C6V68",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "5",
  "CritNm_4": "UTYP",
  "CritVal_4": "IFSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

```json
// Row 3
{
  "TechRcrdId": "3",
  "ISIN": "EZFV5H8C6V68",
  "Desc": "Swaps and futures/forwards on swaps",
  "CritNm": "SACL",
  "CritVal": "IRD06",
  "CritNm_2": "INC1",
  "CritVal_2": "EUR",
  "CritNm_3": "TTMB",
  "CritVal_3": "4",
  "CritNm_4": "UTYP",
  "CritVal_4": "IFSC",
  "FinInstrmClssfctn": "DERV",
  "FrDt": "2024-01-01",
  "ToDt": "2024-12-31",
  "Lqdty": "false",
  "PreTradLrgInScaleThrshld_Amt": "5000000",
  "PstTradLrgInScaleThrshld_Amt": "10000000",
  "PreTradInstrmSzSpcfcThrshld_Amt": "4000000",
  "PstTradInstrmSzSpcfcThrshld_Amt": "9000000",
  "CritNm_5": "",
  "CritVal_5": "",
  "CritNm_6": "",
  "CritVal_6": "",
  "CritNm_7": "",
  "CritVal_7": ""
}
```

---

