# FIRDS Files Analysis Report

**Financial Instruments Reference Data System (FIRDS) Analysis**

Generated on: 2025-09-01 20:29:37

This report analyzes FIRDS CSV files containing instrument reference data for different instrument types (C, D, E, F, H, I, J, S, R, O).

## Executive Summary

- **Instrument Types Found**: C, D, E, F, H, I, J, O, R, S
- **Total Files Analyzed**: 29
- **Total Unique Columns**: 118
- **Common Columns Across All Types**: 14

## File-by-File Analysis

### 📊 FULINS_C_20250830_01of01_firds_data.csv

- **Instrument Type**: C
- **Total Rows**: 131,369
- **Total Columns**: 17

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 22 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 111,888 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 110,160 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 120,965 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 131,368 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "JE00B23SZL05",
  "FinInstrmGnlAttrbts_FullNm": "STANLIB FUNDS LIMITED B Class Shares",
  "FinInstrmGnlAttrbts_ShrtNm": "STAB FUND/GBL PROPERTY FD-B USD",
  "FinInstrmGnlAttrbts_ClssfctnTp": "CBCGXQ",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930015FR83PHHI2P68",
  "TradgVnRltdAttrbts_Id": "XMSM",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2009-07-02T15:10:08.8Z",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2009-07-02T15:10:08.8Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2009-07-02T15:10:08.8Z",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2018-10-15",
  "TechAttrbts_RlvntTradgVn": "XMSM",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null
}

// Row 2
{
  "Id": "HK0405033157",
  "FinInstrmGnlAttrbts_FullNm": "Yuexiu Real Estate Investment Registered Units o.N.",
  "FinInstrmGnlAttrbts_ShrtNm": "YUEXIU REIT/UT HKD",
  "FinInstrmGnlAttrbts_ClssfctnTp": "CBCIXS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HKD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2549008XUNG8VP1T2O94",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2011-05-23T05:00:00Z",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-07-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null
}

// Row 3
{
  "Id": "HK0405033157",
  "FinInstrmGnlAttrbts_FullNm": "Yuexiu Real Estate Investment Registered Units o.N.",
  "FinInstrmGnlAttrbts_ShrtNm": "YUEXIU REIT/UT HKD",
  "FinInstrmGnlAttrbts_ClssfctnTp": "CBCIXS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HKD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2549008XUNG8VP1T2O94",
  "TradgVnRltdAttrbts_Id": "FRAV",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2023-05-21T22:00:00Z",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-13",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null
}

// Row 4
{
  "Id": "HK0435036626",
  "FinInstrmGnlAttrbts_FullNm": "Sunlight Real Est.Investm.Tr. Registered Units o.N.",
  "FinInstrmGnlAttrbts_ShrtNm": "SUNLIGHT REIT/UT HKD",
  "FinInstrmGnlAttrbts_ClssfctnTp": "CBCIXS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HKD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2549006X8RGGALXRKK48",
  "TradgVnRltdAttrbts_Id": "BERB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2007-04-18T06:00:00Z",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2020-06-18",
  "TechAttrbts_RlvntTradgVn": "BERB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null
}

// Row 5
{
  "Id": "HK0435036626",
  "FinInstrmGnlAttrbts_FullNm": "Sunlight Real Est.Investm.Tr. Registered Units o.N.",
  "FinInstrmGnlAttrbts_ShrtNm": "SUNLIGHT REIT/UT HKD",
  "FinInstrmGnlAttrbts_ClssfctnTp": "CBCIXS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HKD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2549006X8RGGALXRKK48",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2011-05-23T05:00:00Z",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-07",
  "TechAttrbts_RlvntTradgVn": "BERB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null
}

```

---

### 📊 FULINS_D_20250830_01of03_firds_data.csv

- **Instrument Type**: D
- **Total Rows**: 500,000
- **Total Columns**: 33

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 87,205 | N/A |  |
| DebtInstrmAttrbts_TtlIssdNmnlAmt | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_MtrtyDt | object | 0 | N/A |  |
| DebtInstrmAttrbts_NmnlValPerUnit | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fxd | float64 | 29,008 | N/A |  |
| DebtInstrmAttrbts_DebtSnrty | object | 231,117 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 465,191 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 288,280 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,882 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN | object | 489,635 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit | object | 470,992 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val | float64 | 470,992 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd | float64 | 470,992 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 402,980 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm | object | 484,678 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx | object | 496,680 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 424,960 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,996 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 427,468 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 496,248 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "XS2911096670",
  "FinInstrmGnlAttrbts_FullNm": "IILM 4.15 09/04/25",
  "FinInstrmGnlAttrbts_ShrtNm": "INTERNATIONAL I/1ASST BKD 20250904",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DAFCFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "222100ET1519GMWAGQ46",
  "TradgVnRltdAttrbts_Id": "BTFE",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-10-02T10:39:15.452Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-04T04:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "220000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-09-04",
  "DebtInstrmAttrbts_NmnlValPerUnit": "200000.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "4.15",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "LU",
  "TechAttrbts_PblctnPrd_FrDt": "2024-10-03",
  "TechAttrbts_RlvntTradgVn": "BTFE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_DlvryTp": null
}

// Row 2
{
  "Id": "XS3142892853",
  "FinInstrmGnlAttrbts_FullNm": "IILM 4.46 11/06/25",
  "FinInstrmGnlAttrbts_ShrtNm": "INTERNATIONAL I/4.46ASST BKD 202511",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DAFCFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "222100ET1519GMWAGQ46",
  "TradgVnRltdAttrbts_Id": "BTFE",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-08T14:18:30.644Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-11-06T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "420000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-11-06",
  "DebtInstrmAttrbts_NmnlValPerUnit": "200000.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "4.46",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "LU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-12",
  "TechAttrbts_RlvntTradgVn": "BTFE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_DlvryTp": null
}

// Row 3
{
  "Id": "XS0253493349",
  "FinInstrmGnlAttrbts_FullNm": "CBREEZ 5.29 05/08/26 BOND",
  "FinInstrmGnlAttrbts_ShrtNm": "CRC BREEZE FINA/5.29 ASST BKD MT JT",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DAFGAB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900CGVR2G2INYJ134",
  "TradgVnRltdAttrbts_Id": "BTFE",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-01-12T16:45:10.754Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-05-08T00:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "300000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2026-05-08",
  "DebtInstrmAttrbts_NmnlValPerUnit": "344.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "5.29",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "LU",
  "TechAttrbts_PblctnPrd_FrDt": "2023-10-07",
  "TechAttrbts_RlvntTradgVn": "BTFE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_DlvryTp": null
}

// Row 4
{
  "Id": "XS0107289323",
  "FinInstrmGnlAttrbts_FullNm": "THAMES 6  1/2  02/09/32 BOND",
  "FinInstrmGnlAttrbts_ShrtNm": "THAMES WATER PL/6.5 ASST BKD MT JT",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DAFGCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "GBP",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "213800ESMPQ4RQ7G8351",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-07-03T19:29:15Z",
  "TradgVnRltdAttrbts_TermntnDt": "2032-02-09T00:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "200000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2034-02-09",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "6.5",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_DlvryTp": null
}

// Row 5
{
  "Id": "XS0107289323",
  "FinInstrmGnlAttrbts_FullNm": "THAMES 6  1/2  02/09/32 BOND",
  "FinInstrmGnlAttrbts_ShrtNm": "THAMES WATER PL/6.5 ASST BKD MT JT",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DAFGCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "GBP",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "213800ESMPQ4RQ7G8351",
  "TradgVnRltdAttrbts_Id": "BTFE",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-04-19T14:58:43.166Z",
  "TradgVnRltdAttrbts_TermntnDt": "2034-02-09T23:59:59.999Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "200000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2034-02-09",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "6.5",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_DlvryTp": null
}

```

---

### 📊 FULINS_D_20250830_02of03_firds_data.csv

- **Instrument Type**: D
- **Total Rows**: 500,000
- **Total Columns**: 41

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 59,844 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 17,445 | N/A |  |
| DebtInstrmAttrbts_TtlIssdNmnlAmt | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_MtrtyDt | object | 0 | N/A |  |
| DebtInstrmAttrbts_NmnlValPerUnit | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fxd | float64 | 813 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 60,683 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 486,451 | N/A |  |
| DebtInstrmAttrbts_DebtSnrty | object | 494,107 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 496,913 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 496,913 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 496,913 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 490,393 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 488,244 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 487,837 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,996 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm | object | 499,257 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit | object | 499,187 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val | float64 | 499,187 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd | float64 | 499,187 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 499,994 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 499,997 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx | object | 499,997 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN | object | 499,933 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,980 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000MG41W86",
  "FinInstrmGnlAttrbts_FullNm": "Discount Zertifikate Walt Disney emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./ZERO DIZ 20251230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DEAYRS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-09T10:30:57Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-19T22:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "250000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-12-30",
  "DebtInstrmAttrbts_NmnlValPerUnit": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US2546871060",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-11",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_DebtSnrty": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 2
{
  "Id": "DE000MG41W94",
  "FinInstrmGnlAttrbts_FullNm": "Discount Zertifikate Walt Disney emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./ZERO DIZ 20251230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DEAYRS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-09T10:30:57Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-19T22:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "250000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-12-30",
  "DebtInstrmAttrbts_NmnlValPerUnit": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US2546871060",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-11",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_DebtSnrty": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 3
{
  "Id": "DE000MG41WA5",
  "FinInstrmGnlAttrbts_FullNm": "Discount Zertifikate Walt Disney emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./ZERO DIZ 20251230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DEAYRS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-09T10:30:57Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-19T22:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "250000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-12-30",
  "DebtInstrmAttrbts_NmnlValPerUnit": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US2546871060",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-11",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_DebtSnrty": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 4
{
  "Id": "DE000MG41WB3",
  "FinInstrmGnlAttrbts_FullNm": "Discount Zertifikate Walt Disney emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./ZERO DIZ 20251230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DEAYRS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-09T10:30:58Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-19T22:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "200000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-12-30",
  "DebtInstrmAttrbts_NmnlValPerUnit": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US2546871060",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-11",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_DebtSnrty": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 5
{
  "Id": "DE000MG41WC1",
  "FinInstrmGnlAttrbts_FullNm": "Discount Zertifikate Walt Disney emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./ZERO DIZ 20251230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DEAYRS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-09T10:30:58Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-19T22:00:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "200000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2025-12-30",
  "DebtInstrmAttrbts_NmnlValPerUnit": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US2546871060",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-11",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_DebtSnrty": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

```

---

### 📊 FULINS_D_20250830_03of03_firds_data.csv

- **Instrument Type**: D
- **Total Rows**: 314,646
- **Total Columns**: 41

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 1 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 1 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 254,932 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 55,654 | N/A |  |
| DebtInstrmAttrbts_TtlIssdNmnlAmt | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_MtrtyDt | object | 0 | N/A |  |
| DebtInstrmAttrbts_NmnlValPerUnit | float64 | 0 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm | object | 300,764 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit | object | 286,456 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val | float64 | 286,456 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd | float64 | 286,456 | N/A |  |
| DebtInstrmAttrbts_DebtSnrty | object | 120,416 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 248,000 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fxd | float64 | 28,190 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx | object | 311,445 | N/A |  |
| DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN | object | 303,539 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 287,533 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 305,043 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 304,753 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 312,527 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 314,445 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 314,445 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 314,645 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 314,598 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 314,598 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 314,598 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct | object | 314,580 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 314,459 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI | object | 306,241 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 314,644 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "XS2303819689",
  "FinInstrmGnlAttrbts_FullNm": "TAURUS 2021-1 UK DESIGNATED ACTIVITY COMPANY £36,000,000 Class C Commercial Mortgage Backed Floating Rate Notes due 2031",
  "FinInstrmGnlAttrbts_ShrtNm": "TAURUS 2021-1 U/MBS 22001231  SUB",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DGFXFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "GBP",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "635400SG2ZVJCYHITE32",
  "TradgVnRltdAttrbts_Id": "XEYE",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2031-05-17T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "36000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2031-05-17",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": "SONIA",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": "DAYS",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": "165.0",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-21",
  "TechAttrbts_RlvntTradgVn": "XEYE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_IntrstRate_Fxd": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 2
{
  "Id": "XS2303819929",
  "FinInstrmGnlAttrbts_FullNm": "TAURUS 2021-1 UK DESIGNATED ACTIVITY COMPANY £56,000,000 Class D Commercial Mortgage Backed Floating Rate Notes due 2031",
  "FinInstrmGnlAttrbts_ShrtNm": "TAURUS 2021-1 U/MBS 22001231  SUB",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DGFXFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "GBP",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "635400SG2ZVJCYHITE32",
  "TradgVnRltdAttrbts_Id": "XEYE",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2031-05-17T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "56000000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2031-05-17",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": "SONIA",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": "DAYS",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": "260.0",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-21",
  "TechAttrbts_RlvntTradgVn": "XEYE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_IntrstRate_Fxd": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 3
{
  "Id": "XS2303820349",
  "FinInstrmGnlAttrbts_FullNm": "TAURUS 2021-1 UK DESIGNATED ACTIVITY COMPANY £33,129,000 Class E Commercial Mortgage Backed Floating Rate Notes due 2031",
  "FinInstrmGnlAttrbts_ShrtNm": "TAURUS 2021-1 U/MBS 22001231  SUB",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DGFXFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "GBP",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "635400SG2ZVJCYHITE32",
  "TradgVnRltdAttrbts_Id": "XEYE",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-03-02T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2031-05-17T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "33129000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2031-05-17",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": "SONIA",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": "DAYS",
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": "1.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": "365.0",
  "DebtInstrmAttrbts_DebtSnrty": "SNDB",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-21",
  "TechAttrbts_RlvntTradgVn": "XEYE",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DebtInstrmAttrbts_IntrstRate_Fxd": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 4
{
  "Id": "XS2360362789",
  "FinInstrmGnlAttrbts_FullNm": "FASTNET SECURITIES 16 DAC €1,407,650,000 Class A2 Residential Mortgage Backed Fixed then Floating Rate Notes due 2058",
  "FinInstrmGnlAttrbts_ShrtNm": "FASTNET SECURIT/MBS 20581218  SUB  ",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DGFXFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "213800IETRQMSPQAQP65",
  "TradgVnRltdAttrbts_Id": "XMSM",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-07-21T14:37:09.92Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-07-21T14:37:09.92Z",
  "TradgVnRltdAttrbts_TermntnDt": "2058-12-14T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "1407650000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2058-12-14",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DebtInstrmAttrbts_DebtSnrty": "SBOD",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-08-13",
  "TechAttrbts_RlvntTradgVn": "XMSM",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2021-07-21T14:37:09.92Z",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.25",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 5
{
  "Id": "XS2360364645",
  "FinInstrmGnlAttrbts_FullNm": "FASTNET SECURITIES 16 DAC €1,001,699,000 Class A3 Residential Mortgage Backed Fixed then Floating Rate Notes due 2058",
  "FinInstrmGnlAttrbts_ShrtNm": "FASTNET SECURIT/.35MBS 20581218  SU",
  "FinInstrmGnlAttrbts_ClssfctnTp": "DGFXFR",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "213800IETRQMSPQAQP65",
  "TradgVnRltdAttrbts_Id": "XMSM",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-07-21T14:37:09.92Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-07-21T14:37:09.92Z",
  "TradgVnRltdAttrbts_TermntnDt": "2058-12-14T23:59:00Z",
  "DebtInstrmAttrbts_TtlIssdNmnlAmt": "1001699000.0",
  "DebtInstrmAttrbts_MtrtyDt": "2058-12-14",
  "DebtInstrmAttrbts_NmnlValPerUnit": "100000.0",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd": null,
  "DebtInstrmAttrbts_DebtSnrty": "SBOD",
  "TechAttrbts_RlvntCmptntAuthrty": "IE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-08-13",
  "TechAttrbts_RlvntTradgVn": "XMSM",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2021-07-21T14:37:09.92Z",
  "DebtInstrmAttrbts_IntrstRate_Fxd": "0.35",
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx": null,
  "DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

```

---

### 📊 FULINS_E_20250830_01of02_firds_data.csv

- **Instrument Type**: E
- **Total Rows**: 500,000
- **Total Columns**: 28

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 353,316 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 191,019 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 182,736 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 488,165 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,974 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,884 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 337,134 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 326,090 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 499,995 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 499,995 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 499,995 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI | object | 499,997 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "NL00150001S5",
  "FinInstrmGnlAttrbts_FullNm": "Kingfish Co NV/The SHRS",
  "FinInstrmGnlAttrbts_ShrtNm": "Kingfish Zeelan/Sh Vtg FPd",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ECVUFB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "9845004WD3997B9F1061",
  "TradgVnRltdAttrbts_Id": "EBLX",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2022-11-11T07:30:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "TechAttrbts_RlvntCmptntAuthrty": "NO",
  "TechAttrbts_PblctnPrd_FrDt": "2022-11-19",
  "TechAttrbts_RlvntTradgVn": "MERK",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null
}

// Row 2
{
  "Id": "NL00150001S5",
  "FinInstrmGnlAttrbts_FullNm": "Kingfish Co NV/The SHRS",
  "FinInstrmGnlAttrbts_ShrtNm": "Kingfish Zeelan/Sh Vtg FPd",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ECVUFB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "9845004WD3997B9F1061",
  "TradgVnRltdAttrbts_Id": "ENTW",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-05-22T06:30:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "TechAttrbts_RlvntCmptntAuthrty": "NO",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-23",
  "TechAttrbts_RlvntTradgVn": "MERK",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null
}

// Row 3
{
  "Id": "NL00150001S5",
  "FinInstrmGnlAttrbts_FullNm": "Kingfish Co NV/The SHRS",
  "FinInstrmGnlAttrbts_ShrtNm": "Kingfish Zeelan/Sh Vtg FPd",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ECVUFB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "9845004WD3997B9F1061",
  "TradgVnRltdAttrbts_Id": "ERFQ",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2022-09-08T06:41:02.727Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "TechAttrbts_RlvntCmptntAuthrty": "NO",
  "TechAttrbts_PblctnPrd_FrDt": "2022-09-09",
  "TechAttrbts_RlvntTradgVn": "MERK",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null
}

// Row 4
{
  "Id": "NL00150001S5",
  "FinInstrmGnlAttrbts_FullNm": "The Kingfish Company N.V. Aandelen aan toonder EO -,01",
  "FinInstrmGnlAttrbts_ShrtNm": "Kingfish Zeelan/Sh Vtg FPd",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ECVUFB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "9845004WD3997B9F1061",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-05-04T05:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "TechAttrbts_RlvntCmptntAuthrty": "NO",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-07",
  "TechAttrbts_RlvntTradgVn": "MERK",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null
}

// Row 5
{
  "Id": "NL00150001S5",
  "FinInstrmGnlAttrbts_FullNm": "The Kingfish Company N.V. Aandelen aan toonder EO -,01",
  "FinInstrmGnlAttrbts_ShrtNm": "Kingfish Zeelan/Sh Vtg FPd",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ECVUFB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "9845004WD3997B9F1061",
  "TradgVnRltdAttrbts_Id": "FRAV",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-05-21T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "TechAttrbts_RlvntCmptntAuthrty": "NO",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-13",
  "TechAttrbts_RlvntTradgVn": "MERK",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null
}

```

---

### 📊 FULINS_E_20250830_02of02_firds_data.csv

- **Instrument Type**: E
- **Total Rows**: 94,963
- **Total Columns**: 24

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 1,616 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 280 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 1,752 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 94,744 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 94,518 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 94,508 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 94,105 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI | object | 94,956 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 94,962 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 94,962 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 94,962 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000FA1V883",
  "FinInstrmGnlAttrbts_FullNm": "Société Générale Effekten GmbHBO.C.Z 27.03.26 Infineon",
  "FinInstrmGnlAttrbts_ShrtNm": "SG EFFEKTEN/ZT 20260327 INFINE BARR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "EYCYMS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900W18LQJJN6SJ336",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-28T22:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-29T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-03-19T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE0006231004",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null
}

// Row 2
{
  "Id": "DE000FA1V883",
  "FinInstrmGnlAttrbts_FullNm": "Capped Bonus-Zertifikat auf Infineon Technologies AG",
  "FinInstrmGnlAttrbts_ShrtNm": "SG EFFEKTEN/ZT 20260327 INFINE BARR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "EYCYMS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900W18LQJJN6SJ336",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-29T07:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-29T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-03-19T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE0006231004",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-02",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null
}

// Row 3
{
  "Id": "DE000FA1V891",
  "FinInstrmGnlAttrbts_FullNm": "Société Générale Effekten GmbHBO.C.Z 30.12.25 K+S",
  "FinInstrmGnlAttrbts_ShrtNm": "SG EFFEKTEN/ZT 20251230 K+S AG BARR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "EYCYMS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900W18LQJJN6SJ336",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-28T22:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-29T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-18T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000KSAG888",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null
}

// Row 4
{
  "Id": "DE000FA1V891",
  "FinInstrmGnlAttrbts_FullNm": "Capped Bonus-Zertifikat auf K+S Aktiengesellschaft",
  "FinInstrmGnlAttrbts_ShrtNm": "SG EFFEKTEN/ZT 20251230 K+S AG BARR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "EYCYMS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900W18LQJJN6SJ336",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-29T07:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-29T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-18T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000KSAG888",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-02",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null
}

// Row 5
{
  "Id": "DE000FA1V8A0",
  "FinInstrmGnlAttrbts_FullNm": "Société Générale Effekten GmbHBO.C.Z 26.09.25 Hensoldt",
  "FinInstrmGnlAttrbts_ShrtNm": "SG EFFEKTEN/ZT 20250926 HENSOL BARR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "EYCYMS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900W18LQJJN6SJ336",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-28T22:00:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-29T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-18T21:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000HAG0005",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null
}

```

---

### 📊 FULINS_F_20250830_01of01_firds_data.csv

- **Instrument Type**: F
- **Total Rows**: 46,984
- **Total Columns**: 70

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 2 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 24 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct | object | 46,904 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct | object | 46,904 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 38,626 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 38,948 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct | object | 46,980 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct | object | 46,980 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct | object | 46,949 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct | object | 46,949 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct | object | 46,949 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct | object | 46,911 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct | object | 46,911 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 43,030 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 42,232 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 43,511 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 43,265 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 46,498 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 46,498 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct | object | 46,919 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct | object | 46,919 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct | object | 46,919 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 44,254 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 44,254 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 45,642 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct | object | 41,565 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct | object | 41,565 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct | object | 41,565 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 13,081 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct | object | 46,968 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct | object | 46,968 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct | object | 46,756 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct | object | 46,926 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct | object | 46,926 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct | object | 46,699 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct | object | 46,699 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct | object | 46,981 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct | object | 46,981 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 46,904 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 46,904 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 46,904 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct | object | 46,321 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct | object | 46,321 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct | object | 46,321 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct | object | 46,876 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct | object | 46,876 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct | object | 46,876 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 46,932 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 45,894 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 45,892 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 46,944 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 46,944 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 46,893 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 46,893 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 46,933 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000C28S352",
  "FinInstrmGnlAttrbts_FullNm": "FALM SI 20250922 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20250922",
  "FinInstrmGnlAttrbts_ClssfctnTp": "FCACSX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "True",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-01-15T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-22T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-22",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct": "AGRI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct": "DIRY",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "FUTR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-09-03",
  "TechAttrbts_RlvntTradgVn": "XEER",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null
}

// Row 2
{
  "Id": "DE000C28U9C8",
  "FinInstrmGnlAttrbts_FullNm": "FABT SI 20250924 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20250924",
  "FinInstrmGnlAttrbts_ClssfctnTp": "FCACSX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "True",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-02-01T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-24T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-24",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct": "AGRI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct": "DIRY",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "FUTR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-02-02",
  "TechAttrbts_RlvntTradgVn": "XEER",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null
}

// Row 3
{
  "Id": "DE000C28U9E4",
  "FinInstrmGnlAttrbts_FullNm": "FASM SI 20250924 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20250924",
  "FinInstrmGnlAttrbts_ClssfctnTp": "FCACSX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "True",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-02-01T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-24T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-24",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct": "AGRI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct": "DIRY",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "FUTR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-02-02",
  "TechAttrbts_RlvntTradgVn": "XEER",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null
}

// Row 4
{
  "Id": "DE000C28U9F1",
  "FinInstrmGnlAttrbts_FullNm": "FAWH SI 20250924 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20250924",
  "FinInstrmGnlAttrbts_ClssfctnTp": "FCACSX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "True",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-02-01T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-24T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-24",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct": "AGRI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct": "DIRY",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "FUTR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-02-02",
  "TechAttrbts_RlvntTradgVn": "XEER",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null
}

// Row 5
{
  "Id": "DE000C28VFS9",
  "FinInstrmGnlAttrbts_FullNm": "FALM SI 20251020 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20251020",
  "FinInstrmGnlAttrbts_ClssfctnTp": "FCACSX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "True",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-02-13T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-10-20T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-10-20",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct": "AGRI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct": "DIRY",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "FUTR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-09-03",
  "TechAttrbts_RlvntTradgVn": "XEER",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null
}

```

---

### 📊 FULINS_H_20250830_01of02_firds_data.csv

- **Instrument Type**: H
- **Total Rows**: 500,000
- **Total Columns**: 42

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 2,819 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 15 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 7,594 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,310 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 224,400 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 496,875 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 496,234 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 496,233 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 497,979 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 497,776 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 499,997 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Ccy | object | 499,931 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 496,490 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 497,801 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 499,861 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 499,861 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 496,341 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 496,221 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 484,019 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 284,247 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 284,247 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 300,228 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd | float64 | 499,597 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI | object | 499,988 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd | float64 | 499,999 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZ1QS2X4HGQ3",
  "FinInstrmGnlAttrbts_FullNm": "Credit Option Index_Swaption EZQ41P4DCR25 EUR 20251119",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Idx Swt EUR 20251119",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HCIAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-26T02:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-11-19T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-11-19",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZQ41P4DCR25",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-28",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd": null
}

// Row 2
{
  "Id": "EZ5D7B4G6CW2",
  "FinInstrmGnlAttrbts_FullNm": "Credit Option Index_Swaption EZWZPN7G1GC9 EUR 20251015",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Idx Swt EUR 20251015",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HCIAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-07-03T02:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-10-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-10-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZWZPN7G1GC9",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-05",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd": null
}

// Row 3
{
  "Id": "EZ817D3RYS64",
  "FinInstrmGnlAttrbts_FullNm": "NA/CDS Idx Swt EUR 20251119",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Idx Swt EUR 20251119",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HCIAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5299000UUYW66L5LT560",
  "TradgVnRltdAttrbts_Id": "RFQN",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-29T07:28:46.723Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-11-19T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-11-19",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZ6RYYRN5GR0",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "RFQN",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd": null
}

// Row 4
{
  "Id": "EZDJR6HX6P52",
  "FinInstrmGnlAttrbts_FullNm": "Credit Option Index_Swaption EZWZPN7G1GC9 EUR 20250917",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Idx Swt EUR 20250917",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HCIAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-11T02:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-17T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-17",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZWZPN7G1GC9",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd": null
}

// Row 5
{
  "Id": "EZFB5B96NJS0",
  "FinInstrmGnlAttrbts_FullNm": "Credit Option Index_Swaption EZQ41P4DCR25 EUR 20250917",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Idx Swt EUR 20250917",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HCIAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-11T02:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-17T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-17",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZQ41P4DCR25",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd": null
}

```

---

### 📊 FULINS_H_20250830_02of02_firds_data.csv

- **Instrument Type**: H
- **Total Rows**: 411,444
- **Total Columns**: 38

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 624 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 21 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 114,246 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 140,881 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 107,919 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 107,919 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 378,482 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 411,379 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 411,265 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 411,175 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 411,175 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd | float64 | 408,799 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 411,427 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI | object | 411,427 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 376,705 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 297,722 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 297,722 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 411,372 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Ccy | object | 411,375 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Yld | float64 | 411,443 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 332,363 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZLNZKQ1J269",
  "FinInstrmGnlAttrbts_FullNm": "Rates Option Swaption Call EZBB5JFFX8V0 ILS 20251209",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/O Call Epn Fxd Flt ILS 20251209",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HRCAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "ILS",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-12-09T03:21:45Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-09T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-12-09",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZBB5JFFX8V0",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "TLBO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "1.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2024-12-11",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 2
{
  "Id": "EZLP0V53MSL4",
  "FinInstrmGnlAttrbts_FullNm": "Rates Option Swaption Call EZMQFGB6YC07 SAR 20270715",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/O Call Epn Fxd Flt SAR 20270715",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HRCAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "SAR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-07-15T02:04:35Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-07-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2027-07-15",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZMQFGB6YC07",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "4.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-26",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "SRIOR-SUAA",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 3
{
  "Id": "EZLP27MDXV92",
  "FinInstrmGnlAttrbts_FullNm": "Rates Option Swaption Call EZY3YYJPS5C5 SAR 20270217",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/O Call Epn Fxd Flt SAR 20270217",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HRCAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "SAR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-02-17T04:12:55Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-02-17T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2027-02-17",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZY3YYJPS5C5",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "4.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2023-02-19",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "SRIORSUAA",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 4
{
  "Id": "EZLP4NYKR6Q6",
  "FinInstrmGnlAttrbts_FullNm": "Rates Option Swaption Call EZHSQTWKB855 ZAR 20260929",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/O Call Epn Fxd Flt ZAR 20260929",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HRCAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "ZAR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-09-28T23:29:14Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-09-29T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-09-29",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZHSQTWKB855",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "JIBA",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "5.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2023-09-30",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

// Row 5
{
  "Id": "EZLP4WH569D6",
  "FinInstrmGnlAttrbts_FullNm": "Rates Option Swaption Call EZNMMGZ2ZN58 SAR 20260325",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/O Call Epn Fxd Flt SAR 20260325",
  "FinInstrmGnlAttrbts_ClssfctnTp": "HRCAVP",
  "FinInstrmGnlAttrbts_NtnlCcy": "SAR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-03-25T00:31:21Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-03-25T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-03-25",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "EZNMMGZ2ZN58",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "2.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2024-03-27",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "SRIORSUAA",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null
}

```

---

### 📊 FULINS_I_20250830_01of01_firds_data.csv

- **Instrument Type**: I
- **Total Rows**: 2
- **Total Columns**: 19

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | 1 |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | 2 | EUA Phase 4, SEME SI 20291217 CS |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | 1 |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | 1 |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | 1 |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | 1 |  |
| Issr | object | 0 | 1 |  |
| TradgVnRltdAttrbts_Id | object | 0 | 2 | FTFS, XEER |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | 1 |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | 2 | 2023-06-01T08:29:07Z, 2020-12-15T06:00:00Z |
| TradgVnRltdAttrbts_TermntnDt | object | 0 | 2 | 2029-12-16T23:00:00Z, 2029-12-17T23:59:59Z |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 0 | 1 |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 0 | 1 |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 0 | 1 |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 0 | 1 |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 0 | 1 |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | 1 |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | 2 | 2023-12-29, 2023-05-23 |
| TechAttrbts_RlvntTradgVn | object | 0 | 1 |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EU000A2QMW50",
  "FinInstrmGnlAttrbts_FullNm": "EUA Phase 4",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20291217",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ITNXXX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "FTFS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-06-01T08:29:07Z",
  "TradgVnRltdAttrbts_TermntnDt": "2029-12-16T23:00:00Z",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": "ENVR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": "EMIS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": "EUAE",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "OTHR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-29",
  "TechAttrbts_RlvntTradgVn": "XEER"
}

// Row 2
{
  "Id": "EU000A2QMW50",
  "FinInstrmGnlAttrbts_FullNm": "SEME SI 20291217 CS",
  "FinInstrmGnlAttrbts_ShrtNm": "EEX/F 20291217",
  "FinInstrmGnlAttrbts_ClssfctnTp": "ITNXXX",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900J0JGLSFDWNFC20",
  "TradgVnRltdAttrbts_Id": "XEER",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-12-15T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2029-12-17T23:59:59Z",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": "ENVR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": "EMIS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": "EUAE",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": "OTHR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": "EXOF",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-05-23",
  "TechAttrbts_RlvntTradgVn": "XEER"
}

```

---

### 📊 FULINS_J_20250830_01of01_firds_data.csv

- **Instrument Type**: J
- **Total Rows**: 118,998
- **Total Columns**: 44

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 21,099 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 1,635 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 118,927 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 118,962 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 118,962 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 114,674 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 87,963 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 118,974 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 32,540 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 14,386 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 109,422 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 106,781 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 106,781 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 109,921 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 109,921 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 109,921 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 116,357 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx | object | 118,829 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct | object | 118,964 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct | object | 118,964 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct | object | 118,964 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 118,958 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 118,958 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct | object | 118,994 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct | object | 118,994 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 118,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 118,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 118,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct | object | 118,997 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZ00K9120994",
  "FinInstrmGnlAttrbts_FullNm": "Equity Forward Non_Standard Multiple ISINs EUR 20270630",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Fwd Nstd Bskt EUR 20270630",
  "FinInstrmGnlAttrbts_ClssfctnTp": "JEBXFC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-11-13T17:35:18Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-06-30T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2027-06-30",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "DE000BASF111",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-04-03",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null
}

// Row 2
{
  "Id": "EZ05XJYN89V6",
  "FinInstrmGnlAttrbts_FullNm": "Equity Forward Price_Return_Basic_Performance_Basket Multiple ISINs EUR 20270826",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Fwd Bskt Fwd Pr EUR 20270826",
  "FinInstrmGnlAttrbts_ClssfctnTp": "JEBXFC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-09-20T12:10:15Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-08-26T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2027-08-26",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "DE0005190003",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-10-14",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null
}

// Row 3
{
  "Id": "EZ0G0T1TS723",
  "FinInstrmGnlAttrbts_FullNm": "Equity Forward Price_Return_Basic_Performance_Basket Multiple ISINs EUR 20270831",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Fwd Bskt Fwd Pr EUR 20270831",
  "FinInstrmGnlAttrbts_ClssfctnTp": "JEBXFC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-10-01T10:05:28Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-08-31T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2027-08-31",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "FR0000045072",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-10-13",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null
}

// Row 4
{
  "Id": "EZ0TWBPYXZ79",
  "FinInstrmGnlAttrbts_FullNm": "Equity Forward Non_Standard Multiple ISINs EUR 20260615",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Fwd Nstd Bskt EUR 20260615",
  "FinInstrmGnlAttrbts_ClssfctnTp": "JEBXFC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-04-28T16:54:26Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-15T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-15",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "DE0007100000",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-05-28",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null
}

// Row 5
{
  "Id": "EZ1P9GTN5RX4",
  "FinInstrmGnlAttrbts_FullNm": "Equity Forward Price_Return_Basic_Performance_Basket Multiple ISINs EUR 20280427",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Fwd Bskt Fwd Pr EUR 20280427",
  "FinInstrmGnlAttrbts_ClssfctnTp": "JEBXFC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-11-16T05:58:17Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-04-27T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2028-04-27",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "FR0000120578",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-11-18",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct": null
}

```

---

### 📊 FULINS_O_20250830_01of03_firds_data.csv

- **Instrument Type**: O
- **Total Rows**: 500,000
- **Total Columns**: 48

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 2 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 53,785 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 496,455 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 497,793 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 497,793 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 497,793 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 42,910 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 235,573 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 412,292 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 447,027 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 446,893 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 419,951 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,322 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 486,368 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct | object | 490,826 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct | object | 490,826 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct | object | 490,826 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 483,263 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 483,263 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 498,606 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 498,606 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 498,606 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct | object | 494,471 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct | object | 494,471 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct | object | 494,471 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 499,360 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 499,360 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 499,360 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 493,517 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 460,635 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000C772L13",
  "FinInstrmGnlAttrbts_FullNm": "OEU3 SI 20250915 PS AM C 96.5000 0",
  "FinInstrmGnlAttrbts_ShrtNm": "Eurex/O 20250915 C AM F FEU 96.5000",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCAFPS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900UT4DG0LG5R9O07",
  "TradgVnRltdAttrbts_Id": "XEUR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-07-28T00:15:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000C4F5E66",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": "96.5",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-29",
  "TechAttrbts_RlvntTradgVn": "XEUR",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 2
{
  "Id": "DE000C772L39",
  "FinInstrmGnlAttrbts_FullNm": "OEU3 SI 20250915 PS AM C 96.6250 0",
  "FinInstrmGnlAttrbts_ShrtNm": "Eurex/O 20250915 C AM F FEU 96.6250",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCAFPS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900UT4DG0LG5R9O07",
  "TradgVnRltdAttrbts_Id": "XEUR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-09-19T00:15:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000C4F5E66",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": "96.625",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-17",
  "TechAttrbts_RlvntTradgVn": "XEUR",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 3
{
  "Id": "DE000C772L54",
  "FinInstrmGnlAttrbts_FullNm": "OEU3 SI 20250915 PS AM C 96.7500 0",
  "FinInstrmGnlAttrbts_ShrtNm": "Eurex/O 20250915 C AM F FEU 96.7500",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCAFPS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900UT4DG0LG5R9O07",
  "TradgVnRltdAttrbts_Id": "XEUR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-09-19T00:15:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000C4F5E66",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": "96.75",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-17",
  "TechAttrbts_RlvntTradgVn": "XEUR",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 4
{
  "Id": "DE000C772L70",
  "FinInstrmGnlAttrbts_FullNm": "OEU3 SI 20250915 PS AM C 96.8750 0",
  "FinInstrmGnlAttrbts_ShrtNm": "Eurex/O 20250915 C AM F FEU 96.8750",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCAFPS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900UT4DG0LG5R9O07",
  "TradgVnRltdAttrbts_Id": "XEUR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-09-19T00:15:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000C4F5E66",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": "96.875",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-17",
  "TechAttrbts_RlvntTradgVn": "XEUR",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 5
{
  "Id": "DE000C772L96",
  "FinInstrmGnlAttrbts_FullNm": "OEU3 SI 20250915 PS AM C 97.0000 0",
  "FinInstrmGnlAttrbts_ShrtNm": "Eurex/O 20250915 C AM F FEU 97.0000",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCAFPS",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900UT4DG0LG5R9O07",
  "TradgVnRltdAttrbts_Id": "XEUR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-09-19T00:15:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-15",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000C4F5E66",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": "97.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-17",
  "TechAttrbts_RlvntTradgVn": "XEUR",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

```

---

### 📊 FULINS_O_20250830_02of03_firds_data.csv

- **Instrument Type**: O
- **Total Rows**: 500,000
- **Total Columns**: 33

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 491,345 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 491,345 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 3,545 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 231,868 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 9,551 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,104 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 430,359 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct | object | 499,855 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 496,455 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 497,793 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 497,793 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 497,793 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 434,372 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 496,564 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "SE0020806412",
  "FinInstrmGnlAttrbts_FullNm": "OMXS308L1920",
  "FinInstrmGnlAttrbts_ShrtNm": "NDAQST/O 202812 C OMXS30 1920",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCEICS",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300KBQIVNEJEZVL96",
  "TradgVnRltdAttrbts_Id": "SEED",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-12-11T07:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-12-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2028-12-15",
  "DerivInstrmAttrbts_PricMltplr": "100.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "SE0000337842",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "OMX STOCKHOLM 30",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "1920.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-12",
  "TechAttrbts_RlvntTradgVn": "SEED",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null
}

// Row 2
{
  "Id": "SE0020806420",
  "FinInstrmGnlAttrbts_FullNm": "OMXS308L1960",
  "FinInstrmGnlAttrbts_ShrtNm": "NDAQST/O 202812 C OMXS30 1960",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCEICS",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300KBQIVNEJEZVL96",
  "TradgVnRltdAttrbts_Id": "SEED",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-12-11T07:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-12-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2028-12-15",
  "DerivInstrmAttrbts_PricMltplr": "100.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "SE0000337842",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "OMX STOCKHOLM 30",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "1960.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-12",
  "TechAttrbts_RlvntTradgVn": "SEED",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null
}

// Row 3
{
  "Id": "SE0020806438",
  "FinInstrmGnlAttrbts_FullNm": "OMXS308L2000",
  "FinInstrmGnlAttrbts_ShrtNm": "NDAQST/O 202812 C OMXS30 2000",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCEICS",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300KBQIVNEJEZVL96",
  "TradgVnRltdAttrbts_Id": "SEED",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-12-11T07:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-12-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2028-12-15",
  "DerivInstrmAttrbts_PricMltplr": "100.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "SE0000337842",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "OMX STOCKHOLM 30",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "2000.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-12",
  "TechAttrbts_RlvntTradgVn": "SEED",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null
}

// Row 4
{
  "Id": "SE0020806446",
  "FinInstrmGnlAttrbts_FullNm": "OMXS308L2040",
  "FinInstrmGnlAttrbts_ShrtNm": "NDAQST/O 202812 C OMXS30 2040",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCEICS",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300KBQIVNEJEZVL96",
  "TradgVnRltdAttrbts_Id": "SEED",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-12-11T07:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-12-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2028-12-15",
  "DerivInstrmAttrbts_PricMltplr": "100.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "SE0000337842",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "OMX STOCKHOLM 30",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "2040.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-12",
  "TechAttrbts_RlvntTradgVn": "SEED",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null
}

// Row 5
{
  "Id": "SE0020806453",
  "FinInstrmGnlAttrbts_FullNm": "OMXS308L2080",
  "FinInstrmGnlAttrbts_ShrtNm": "NDAQST/O 202812 C OMXS30 2080",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OCEICS",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300KBQIVNEJEZVL96",
  "TradgVnRltdAttrbts_Id": "SEED",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-12-11T07:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-12-15T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2028-12-15",
  "DerivInstrmAttrbts_PricMltplr": "100.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "SE0000337842",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "OMX STOCKHOLM 30",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "2080.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-12",
  "TechAttrbts_RlvntTradgVn": "SEED",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null
}

```

---

### 📊 FULINS_O_20250830_03of03_firds_data.csv

- **Instrument Type**: O
- **Total Rows**: 177,576
- **Total Columns**: 45

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 159,052 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 49,258 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 39,365 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 88,486 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 167,380 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 163,156 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct | object | 168,402 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct | object | 168,402 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct | object | 168,402 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 160,839 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 160,839 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 176,182 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 176,182 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 176,182 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct | object | 172,047 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct | object | 172,047 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct | object | 172,047 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 176,936 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 176,936 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 176,936 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 171,093 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 128,537 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 128,669 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 138,211 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 177,357 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct | object | 177,431 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "HU0010000235",
  "FinInstrmGnlAttrbts_FullNm": "USD/TRY260353274P",
  "FinInstrmGnlAttrbts_ShrtNm": "Budapesti Ertek/O 20260318 F",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OPEFCS",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930094UMSXWVWJMT48",
  "TradgVnRltdAttrbts_Id": "XBUD",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-03-18T17:30:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-03-31",
  "DerivInstrmAttrbts_PricMltplr": "1000.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "HU0009512372",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "53.274",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "TRY",
  "TechAttrbts_RlvntCmptntAuthrty": "HU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-07",
  "TechAttrbts_RlvntTradgVn": "XBUD",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null
}

// Row 2
{
  "Id": "HU0010000318",
  "FinInstrmGnlAttrbts_FullNm": "CF250904429P",
  "FinInstrmGnlAttrbts_ShrtNm": "Budapesti Ertek/O 20250917 F",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OPEFCS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HUF",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930094UMSXWVWJMT48",
  "TradgVnRltdAttrbts_Id": "XBUD",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-17T17:30:00Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-30",
  "DerivInstrmAttrbts_PricMltplr": "1000.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "HU0009301974",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "442.9",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "HUF",
  "TechAttrbts_RlvntCmptntAuthrty": "HU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-07",
  "TechAttrbts_RlvntTradgVn": "XBUD",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null
}

// Row 3
{
  "Id": "HU0010000334",
  "FinInstrmGnlAttrbts_FullNm": "CF251204495P",
  "FinInstrmGnlAttrbts_ShrtNm": "Budapesti Ertek/O 20251217 F",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OPEFCS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HUF",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930094UMSXWVWJMT48",
  "TradgVnRltdAttrbts_Id": "XBUD",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-17T17:30:00Z",
  "DerivInstrmAttrbts_XpryDt": "2025-12-31",
  "DerivInstrmAttrbts_PricMltplr": "1000.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "HU0009412458",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "449.5",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "HUF",
  "TechAttrbts_RlvntCmptntAuthrty": "HU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-07",
  "TechAttrbts_RlvntTradgVn": "XBUD",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null
}

// Row 4
{
  "Id": "HU0010000359",
  "FinInstrmGnlAttrbts_FullNm": "CF260304560P",
  "FinInstrmGnlAttrbts_ShrtNm": "Budapesti Ertek/O 20260318 F",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OPEFCS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HUF",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930094UMSXWVWJMT48",
  "TradgVnRltdAttrbts_Id": "XBUD",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-03-18T17:30:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-03-31",
  "DerivInstrmAttrbts_PricMltplr": "1000.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "HU0009512786",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "456.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "HUF",
  "TechAttrbts_RlvntCmptntAuthrty": "HU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-07",
  "TechAttrbts_RlvntTradgVn": "XBUD",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null
}

// Row 5
{
  "Id": "HU0010000375",
  "FinInstrmGnlAttrbts_FullNm": "JY250902552P",
  "FinInstrmGnlAttrbts_ShrtNm": "Budapesti Ertek/O 20250917 F",
  "FinInstrmGnlAttrbts_ClssfctnTp": "OPEFCS",
  "FinInstrmGnlAttrbts_NtnlCcy": "HUF",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "54930094UMSXWVWJMT48",
  "TradgVnRltdAttrbts_Id": "XBUD",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-07T08:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-17T17:30:00Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-30",
  "DerivInstrmAttrbts_PricMltplr": "1000.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "HU0009302550",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "255.2",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "HUF",
  "TechAttrbts_RlvntCmptntAuthrty": "HU",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-07",
  "TechAttrbts_RlvntTradgVn": "XBUD",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct": null
}

```

---

### 📊 FULINS_R_20250830_01of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 50

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 453,958 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 405,876 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 31,299 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 499,965 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 33,354 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,881 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 36,041 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 473,373 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 88,816 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,901 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 31,245 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 430,396 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 430,396 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 153,388 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 98,683 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 485,510 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 499,788 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 499,788 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 499,788 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct | object | 499,867 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct | object | 499,867 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct | object | 499,867 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 499,984 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 499,984 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 499,943 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 499,943 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 499,943 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct | object | 499,962 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct | object | 499,962 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct | object | 499,962 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 499,785 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 499,785 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 499,785 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 499,998 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "BE0099150162",
  "FinInstrmGnlAttrbts_FullNm": "CP 76 PETROFINA",
  "FinInstrmGnlAttrbts_ShrtNm": "TOTAL PETROCHEM/RI P",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RAXXXB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5299003N2SCVNU16O909",
  "TradgVnRltdAttrbts_Id": "VPXB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-10-28T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "DerivInstrmAttrbts_OptnTp": "OTHR",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": "PNDG",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "BE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-07",
  "TechAttrbts_RlvntTradgVn": "VPXB",
  "DerivInstrmAttrbts_PricMltplr": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_OptnExrcStyle": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null
}

// Row 2
{
  "Id": "BE0099395676",
  "FinInstrmGnlAttrbts_FullNm": "CP 79 PETROFINA",
  "FinInstrmGnlAttrbts_ShrtNm": "TOTAL PETROCHEM/RI P",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RAXXXB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5299003N2SCVNU16O909",
  "TradgVnRltdAttrbts_Id": "VPXB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-10-28T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "DerivInstrmAttrbts_OptnTp": "OTHR",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": "PNDG",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "BE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-07",
  "TechAttrbts_RlvntTradgVn": "VPXB",
  "DerivInstrmAttrbts_PricMltplr": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_OptnExrcStyle": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null
}

// Row 3
{
  "Id": "BE0099887748",
  "FinInstrmGnlAttrbts_FullNm": "CP 41 SOLVAY",
  "FinInstrmGnlAttrbts_ShrtNm": "SOLVAYSA/RI P",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RAXXXB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300MMVL80RTBP3O28",
  "TradgVnRltdAttrbts_Id": "VPXB",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2017-05-05T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NOISINFOUND9",
  "DerivInstrmAttrbts_OptnTp": "OTHR",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": "PNDG",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "BE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-05-07",
  "TechAttrbts_RlvntTradgVn": "VPXB",
  "DerivInstrmAttrbts_PricMltplr": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_OptnExrcStyle": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null
}

// Row 4
{
  "Id": "FR001400G230",
  "FinInstrmGnlAttrbts_FullNm": "ARGAN SA",
  "FinInstrmGnlAttrbts_ShrtNm": "ARGAN/Rts",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RAXXXB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "529900FXM41XSCUSGH04",
  "TradgVnRltdAttrbts_Id": "TPIR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-04-17T11:51:18.619Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "FK0114538241",
  "DerivInstrmAttrbts_OptnTp": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-09-25",
  "TechAttrbts_RlvntTradgVn": "TPIR",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_OptnExrcStyle": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null
}

// Row 5
{
  "Id": "FR001400HCY0",
  "FinInstrmGnlAttrbts_FullNm": "Covivio SA/France",
  "FinInstrmGnlAttrbts_ShrtNm": "COVIVIO/Rts",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RAXXXB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "969500P8M3W2XX376054",
  "TradgVnRltdAttrbts_Id": "TPIR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-04-28T10:51:28.631Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "FR0000064578",
  "DerivInstrmAttrbts_OptnTp": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2024-09-06",
  "TechAttrbts_RlvntTradgVn": "TPIR",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_OptnExrcStyle": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null
}

```

---

### 📊 FULINS_R_20250830_02of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 53

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 59,121 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 97,989 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 382,724 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 366,762 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 44,450 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 44,264 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 47,089 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct | object | 490,624 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct | object | 490,624 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct | object | 490,624 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 480,069 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 480,069 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 480,069 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 472,890 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 445,561 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 484,304 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 145,758 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,944 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,479 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 499,996 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct | object | 498,317 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct | object | 498,317 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct | object | 498,317 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 499,955 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 499,955 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 473,524 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 473,524 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 473,524 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct | object | 497,976 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct | object | 497,976 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct | object | 497,976 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 495,952 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 495,952 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 495,952 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct | object | 497,733 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct | object | 497,733 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct | object | 497,733 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 498,473 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct | object | 499,839 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct | object | 499,839 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000MM2PW99",
  "FinInstrmGnlAttrbts_FullNm": "Mini Short NASDAQ 100 emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./POS NASDAQ DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFITPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-08-21T10:23:39Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-22T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-23",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct": null
}

// Row 2
{
  "Id": "DE000MM2PWD1",
  "FinInstrmGnlAttrbts_FullNm": "Mini Short S&P 500 emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./POS S&P500 DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFITPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-08-21T10:23:39Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-22T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US78378X1072",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "S&P 500",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-23",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct": null
}

// Row 3
{
  "Id": "DE000MM2PWE9",
  "FinInstrmGnlAttrbts_FullNm": "Mini Short S&P 500 emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./POS S&P500 DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFITPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-08-21T10:23:39Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-22T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US78378X1072",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "S&P 500",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-23",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct": null
}

// Row 4
{
  "Id": "DE000MM2PWG4",
  "FinInstrmGnlAttrbts_FullNm": "Mini Short Dow Jones Industrial Average emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./POS DJIA DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFITPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-08-21T10:23:39Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-22T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US2605661048",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "DOWJONES",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-23",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct": null
}

// Row 5
{
  "Id": "DE000MM2PWH2",
  "FinInstrmGnlAttrbts_FullNm": "Mini Short Dow Jones Industrial Average emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./POS DJIA DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFITPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-08-21T10:23:39Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-22T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US2605661048",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "DOWJONES",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-23",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct": null
}

```

---

### 📊 FULINS_R_20250830_03of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 27

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 37,764 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 75,923 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 1,875 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 33,301 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 33,301 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 25,481 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 482,523 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 476,437 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 490,942 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,205 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 499,994 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,990 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 499,994 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000MK91EF9",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Long BYD emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./COS BYD DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-23T10:59:34Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-24T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CNE100000296",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-25",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 2
{
  "Id": "DE000MK91EG7",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Long BYD emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./COS BYD DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-23T10:59:34Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-24T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CNE100000296",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-25",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 3
{
  "Id": "DE000MK91EH5",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Long BYD emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./COS BYD DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-23T10:59:34Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-24T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CNE100000296",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-25",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 4
{
  "Id": "DE000MK91EJ1",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Long BYD emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./COS BYD DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-23T10:59:34Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-24T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CNE100000296",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-25",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 5
{
  "Id": "DE000MK91EK9",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Long BYD emittiert von Morgan Stanley & Co. Int. plc",
  "FinInstrmGnlAttrbts_ShrtNm": "MS CO.I./COS BYD DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "4PQUHN3JPFGFNF3BB653",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-23T10:59:34Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-24T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CNE100000296",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-25",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

```

---

### 📊 FULINS_R_20250830_04of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 26

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 51,320 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 90,087 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 127 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 23,200 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 23,200 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 63,585 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 425,483 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 447,306 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 464,828 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,995 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,996 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 499,995 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,939 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000PC8VUR9",
  "FinInstrmGnlAttrbts_FullNm": "BNP Paribas Em.-u.Handelsg.mbHTurboL O.End Vontobel 49,183",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/COS VONTOB DYN UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-04-23T09:51:45Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-04-24T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CH0012335540",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 2
{
  "Id": "DE000PC8VUR9",
  "FinInstrmGnlAttrbts_FullNm": "BNP TUR.WAR.OP.END. VTLN",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/COS VONTOB DYN UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-15T07:52:59Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-19T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CH0012335540",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 3
{
  "Id": "DE000PC8VUR9",
  "FinInstrmGnlAttrbts_FullNm": "VONTOBEL HOLDING AG Unlimited Long",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/COS VONTOB DYN UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-04-23T11:51:45Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-04-24T09:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T17:30:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CH0012335540",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-04-25",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 4
{
  "Id": "DE000PC8VUS7",
  "FinInstrmGnlAttrbts_FullNm": "BNP Paribas Em.-u.Handelsg.mbHTurboL O.End Vontobel 47,0479",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/COS VONTOB DYN UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-04-23T09:51:45Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-04-24T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CH0012335540",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

// Row 5
{
  "Id": "DE000PC8VUS7",
  "FinInstrmGnlAttrbts_FullNm": "BNP TUR.WAR.OP.END. VTLN",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/COS VONTOB DYN UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-15T07:52:59Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-19T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "CH0012335540",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-14",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null
}

```

---

### 📊 FULINS_R_20250830_05of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 27

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 60,802 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 435,169 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 1,177 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 49,732 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 49,732 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 61,587 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 98,612 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,930 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 456,516 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,996 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 477,999 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 499,352 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 499,997 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "FRBNPP08BDX8",
  "FinInstrmGnlAttrbts_FullNm": "AIRBU x10 LEV B",
  "FinInstrmGnlAttrbts_ShrtNm": "BNPPAR/Rts 21001230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "7245009UXRIGIRYOBR48",
  "TradgVnRltdAttrbts_Id": "XMLI",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-24T00:01:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-27T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NL0000235190",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-20",
  "TechAttrbts_RlvntTradgVn": "XMLI",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 2
{
  "Id": "FRBNPP08BDY6",
  "FinInstrmGnlAttrbts_FullNm": "ALSTO x5 LEV B",
  "FinInstrmGnlAttrbts_ShrtNm": "BNPPAR/Rts 21001230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "7245009UXRIGIRYOBR48",
  "TradgVnRltdAttrbts_Id": "XMLI",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-24T00:01:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-27T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "FR0010220475",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-20",
  "TechAttrbts_RlvntTradgVn": "XMLI",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 3
{
  "Id": "FRBNPP08BE56",
  "FinInstrmGnlAttrbts_FullNm": "APPLE x8 LEV B",
  "FinInstrmGnlAttrbts_ShrtNm": "BNPPAR/Rts 21001230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "7245009UXRIGIRYOBR48",
  "TradgVnRltdAttrbts_Id": "XMLI",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-24T00:01:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-27T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0378331005",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-20",
  "TechAttrbts_RlvntTradgVn": "XMLI",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 4
{
  "Id": "FRBNPP08BE80",
  "FinInstrmGnlAttrbts_FullNm": "AMEX x3 LEV B",
  "FinInstrmGnlAttrbts_ShrtNm": "BNPPAR/Rts 21001230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "7245009UXRIGIRYOBR48",
  "TradgVnRltdAttrbts_Id": "XMLI",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-24T00:01:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-27T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0258161092",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-20",
  "TechAttrbts_RlvntTradgVn": "XMLI",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 5
{
  "Id": "FRBNPP08BE98",
  "FinInstrmGnlAttrbts_FullNm": "AMEX x8 LEV B",
  "FinInstrmGnlAttrbts_ShrtNm": "BNPPAR/Rts 21001230",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTCE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "7245009UXRIGIRYOBR48",
  "TradgVnRltdAttrbts_Id": "XMLI",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-24T00:01:00Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-27T00:01:00Z",
  "DerivInstrmAttrbts_XpryDt": "9999-12-31",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0258161092",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-20",
  "TechAttrbts_RlvntTradgVn": "XMLI",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

```

---

### 📊 FULINS_R_20250830_06of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 42

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 51,449 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 29,385 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 288,134 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 21,931 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 21,966 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 66,996 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 116,080 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 470,913 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,977 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,775 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 429,932 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 434,437 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 434,437 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 434,437 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 499,984 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 499,984 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 499,990 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 499,990 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 499,990 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 239,277 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 498,771 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 222,988 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 223,059 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 453,077 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 499,990 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 446,055 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 446,054 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 499,999 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 236,488 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000UP5ES42",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG TurboP O.EndGoldm.S.883,364029",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/POS GSACHS DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTPB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-11-07T10:17:13Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-11-08T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US38141G1040",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 2
{
  "Id": "DE000UP5ES42",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Put Optionsschein auf The Goldman Sachs Group Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/POS GSACHS DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTPB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-11-07T11:17:08Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-11-08T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US38141G1040",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-11-09",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 3
{
  "Id": "DE000UP5EY36",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG TurboP O.End Amazon 241,674454",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/POS AMAZON DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTPB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-12-19T10:49:47Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-12-20T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0231351067",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 4
{
  "Id": "DE000UP5EY36",
  "FinInstrmGnlAttrbts_FullNm": "Open End Turbo Put Optionsschein auf Amazon.com Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/POS AMAZON DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTPB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-12-19T11:49:43Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-12-20T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0231351067",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-12-21",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

// Row 5
{
  "Id": "DE000UP5F4D6",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG TurboP O.End Moderna 50,823452",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/POS MOD.I. DYN UNL REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RFSTPB",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-11-11T10:20:35Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-11-12T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US60770K1079",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_OptnExrcStyle": "BERM",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-30",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null
}

```

---

### 📊 FULINS_R_20250830_07of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 55

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 8,472 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 2,199 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 12,738 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 89,751 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 387,284 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 387,205 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 392,648 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 5,260 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 110,937 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 499,090 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 494,164 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 160,516 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 499,999 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct | object | 482,051 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct | object | 482,051 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct | object | 482,051 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 499,961 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 499,961 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 113,114 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 499,942 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 499,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 497,707 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 497,707 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 497,707 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct | object | 499,305 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct | object | 499,305 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct | object | 499,305 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct | object | 499,491 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct | object | 499,491 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct | object | 499,491 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 497,326 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct | object | 499,337 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct | object | 499,337 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct | object | 499,337 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct | object | 499,896 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct | object | 499,896 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct | object | 499,896 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Yld | float64 | 499,999 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000HT2J7V9",
  "FinInstrmGnlAttrbts_FullNm": "HSBC Trinkaus & Burkhardt GmbHPut 18.12.26 Nasd100 24600",
  "FinInstrmGnlAttrbts_ShrtNm": "HSBC T+B/POS NASDAQ 24600 20261218",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWINPE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "JUNT405OW8OY5GN4DX16",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-02-06T11:19:58Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-07T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-12-17T22:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-12-18",
  "DerivInstrmAttrbts_PricMltplr": "0.01",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": "24600.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-13",
  "TechAttrbts_RlvntTradgVn": "MUND",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null
}

// Row 2
{
  "Id": "DE000HT2J7V9",
  "FinInstrmGnlAttrbts_FullNm": "HSBC WAR. PUT 12/26 N100",
  "FinInstrmGnlAttrbts_ShrtNm": "HSBC T+B/POS NASDAQ 24600 20261218",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWINPE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "JUNT405OW8OY5GN4DX16",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-02-06T11:20:19Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-07T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-12-17T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-12-18",
  "DerivInstrmAttrbts_PricMltplr": "0.01",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": "24600.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-13",
  "TechAttrbts_RlvntTradgVn": "MUND",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null
}

// Row 3
{
  "Id": "DE000HT2J7V9",
  "FinInstrmGnlAttrbts_FullNm": "Index-Optionsschein",
  "FinInstrmGnlAttrbts_ShrtNm": "HSBC T+B/POS NASDAQ 24600 20261218",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWINPE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "JUNT405OW8OY5GN4DX16",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-02-06T12:19:56Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-07T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-12-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-12-18",
  "DerivInstrmAttrbts_PricMltplr": "0.01",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": "24600.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-13",
  "TechAttrbts_RlvntTradgVn": "MUND",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null
}

// Row 4
{
  "Id": "DE000HT2J7W7",
  "FinInstrmGnlAttrbts_FullNm": "HSBC Trinkaus & Burkhardt GmbHPut 18.12.26 Nasd100 24800",
  "FinInstrmGnlAttrbts_ShrtNm": "HSBC T+B/POS NASDAQ 24800 20261218",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWINPE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "JUNT405OW8OY5GN4DX16",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-02-06T11:19:58Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-07T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-12-17T22:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-12-18",
  "DerivInstrmAttrbts_PricMltplr": "0.01",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": "24800.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-13",
  "TechAttrbts_RlvntTradgVn": "MUND",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null
}

// Row 5
{
  "Id": "DE000HT2J7W7",
  "FinInstrmGnlAttrbts_FullNm": "HSBC WAR. PUT 12/26 N100",
  "FinInstrmGnlAttrbts_ShrtNm": "HSBC T+B/POS NASDAQ 24800 20261218",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWINPE",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "JUNT405OW8OY5GN4DX16",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-02-06T11:20:19Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-07T06:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-12-17T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-12-18",
  "DerivInstrmAttrbts_PricMltplr": "0.01",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": "US6311011026",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "NASDAQ",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": "24800.0",
  "DerivInstrmAttrbts_OptnExrcStyle": "EURO",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-13",
  "TechAttrbts_RlvntTradgVn": "MUND",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Yld": null
}

```

---

### 📊 FULINS_R_20250830_08of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 25

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 4,275 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 17,922 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 54,513 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 102,010 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 0 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 22 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 5,450 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 2,630 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 499,978 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 499,988 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000JH66KY1",
  "FinInstrmGnlAttrbts_FullNm": "Optionsschein auf Robinhood Markets Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "JPM STR.PRO./COS ROBMAR 174",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "XZYUUT6IYN31D9K77X08",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-25T13:37:21Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-26T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-18",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US7707001027",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "174.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-27",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 2
{
  "Id": "DE000JH66KZ8",
  "FinInstrmGnlAttrbts_FullNm": "Optionsschein auf Robinhood Markets Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "JPM STR.PRO./COS ROBMAR 176",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "XZYUUT6IYN31D9K77X08",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-25T13:37:21Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-26T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-18",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US7707001027",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "176.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-27",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 3
{
  "Id": "DE000JH66L00",
  "FinInstrmGnlAttrbts_FullNm": "Optionsschein auf Robinhood Markets Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "JPM STR.PRO./COS ROBMAR 178",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "XZYUUT6IYN31D9K77X08",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-25T13:39:41Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-26T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-18",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US7707001027",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "178.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-27",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 4
{
  "Id": "DE000JH66L18",
  "FinInstrmGnlAttrbts_FullNm": "Optionsschein auf Robinhood Markets Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "JPM STR.PRO./COS ROBMAR 180",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "XZYUUT6IYN31D9K77X08",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-25T13:37:21Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-26T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-18",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US7707001027",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "180.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-27",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 5
{
  "Id": "DE000JH66L26",
  "FinInstrmGnlAttrbts_FullNm": "Optionsschein auf Robinhood Markets Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "JPM STR.PRO./COS ROBMAR 182",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "XZYUUT6IYN31D9K77X08",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-06-25T13:38:33Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-06-26T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-06-17T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-06-18",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US7707001027",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "182.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-27",
  "TechAttrbts_RlvntTradgVn": "STUB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

```

---

### 📊 FULINS_R_20250830_09of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 500,000
- **Total Columns**: 27

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 9,239 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 6,677 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 24,065 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 106,845 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 1 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 1,515 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 17,150 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 5,128 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 498,485 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 497,541 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 499,999 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 499,999 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000UM57BE8",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG Call 19.09.25 JPM.Ch. 212",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/COS JPMORG 212 20250919 REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-06-07T10:25:01Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-06-10T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-18T21:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-19",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US46625H1005",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "212.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-06-11",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 2
{
  "Id": "DE000UM57BE8",
  "FinInstrmGnlAttrbts_FullNm": "Call Optionsschein auf JPMorgan Chase & Co.",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/COS JPMORG 212 20250919 REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-06-07T12:24:15Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-06-10T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-09-18T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2025-09-19",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US46625H1005",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "212.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-06-11",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 3
{
  "Id": "DE000UM57BU4",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG Call 16.01.26 UberTech 72",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/COS UBERTE 72 20260116 REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-31T09:44:55Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-06-03T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-01-15T22:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2026-01-16",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US90353T1007",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "72.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-06-04",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 4
{
  "Id": "DE000UM57BU4",
  "FinInstrmGnlAttrbts_FullNm": "Call Optionsschein auf Uber Technologies Inc.",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/COS UBERTE 72 20260116 REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-31T11:44:09Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-06-03T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-01-15T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-01-16",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US90353T1007",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "72.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-06-04",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

// Row 5
{
  "Id": "DE000UM57C34",
  "FinInstrmGnlAttrbts_FullNm": "UBS AG Call 19.12.25 Bk.of Am 38",
  "FinInstrmGnlAttrbts_ShrtNm": "UBS AG/COS BK AME 38 20251219 REGS",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "BFM8T61CT2L1QCEMIK50",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2024-05-31T09:48:26Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-06-03T05:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-12-18T22:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2025-12-19",
  "DerivInstrmAttrbts_PricMltplr": "0.1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US0605051046",
  "DerivInstrmAttrbts_OptnTp": "CALL",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "38.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-06-04",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null
}

```

---

### 📊 FULINS_R_20250830_10of10_firds_data.csv

- **Instrument Type**: R
- **Total Rows**: 184,031
- **Total Columns**: 39

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 9,398 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 1,205 | N/A |  |
| DerivInstrmAttrbts_OptnTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt | float64 | 1,453 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn | object | 24,725 | N/A |  |
| DerivInstrmAttrbts_OptnExrcStyle | object | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 8,283 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 2,025 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 5,225 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 53,016 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Pdg | object | 182,738 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 180,603 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 183,437 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 183,436 | N/A |  |
| DerivInstrmAttrbts_StrkPric_NoPric_Ccy | object | 184,027 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 184,011 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct | object | 136,566 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct | object | 136,566 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct | object | 136,566 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 183,886 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 183,886 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_BsisPts | float64 | 183,875 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct | object | 184,029 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct | object | 184,029 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct | object | 184,029 | N/A |  |
| DerivInstrmAttrbts_StrkPric_Pric_Pctg | float64 | 184,027 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "DE000PM127Q5",
  "FinInstrmGnlAttrbts_FullNm": "BNP FAC.CERT. SHORT P911",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/POS PORSCH 100 UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-15T07:31:49Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-19T06:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000PAG9113",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "100.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-29",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null
}

// Row 2
{
  "Id": "DE000PM127Q5",
  "FinInstrmGnlAttrbts_FullNm": "DR. ING. H.C. F. PORSCHE AG Faktor 12 Short",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/POS PORSCH 100 UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-16T11:27:54Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-17T08:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "DE000PAG9113",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "100.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-29",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null
}

// Row 3
{
  "Id": "DE000PM129F4",
  "FinInstrmGnlAttrbts_FullNm": "BNP Paribas Em.-u.Handelsg.mbHFactS O.End ASMLHold 7",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/POS ASMLHO 100 UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "FRAB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-16T10:27:53Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-17T06:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NL0010273215",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "100.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-29",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": "2098-01-13T22:59:59Z",
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null
}

// Row 4
{
  "Id": "DE000PM129F4",
  "FinInstrmGnlAttrbts_FullNm": "BNP FAC.CERT. SHORT ASME",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/POS ASMLHO 100 UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "MUND",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-05-15T07:31:49Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-19T06:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NL0010273215",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "100.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-29",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null
}

// Row 5
{
  "Id": "DE000PM129F4",
  "FinInstrmGnlAttrbts_FullNm": "ASML HOLDING N.V. Faktor 12 Short",
  "FinInstrmGnlAttrbts_ShrtNm": "BNP PARIBAS EM/POS ASMLHO 100 UNL",
  "FinInstrmGnlAttrbts_ClssfctnTp": "RWSNPA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300TS3U4JKMR1B479",
  "TradgVnRltdAttrbts_Id": "STUB",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2025-01-16T11:27:53Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-17T08:00:00Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "NL0010273215",
  "DerivInstrmAttrbts_OptnTp": "PUTO",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt": "100.0",
  "DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn": "True",
  "DerivInstrmAttrbts_OptnExrcStyle": "AMER",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-29",
  "TechAttrbts_RlvntTradgVn": "FRAB",
  "TradgVnRltdAttrbts_TermntnDt": "9999-12-31T22:00:00Z",
  "DerivInstrmAttrbts_XpryDt": null,
  "DerivInstrmAttrbts_PricMltplr": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Pdg": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_StrkPric_NoPric_Ccy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_StrkPric_Pric_BsisPts": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct": null,
  "DerivInstrmAttrbts_StrkPric_Pric_Pctg": null
}

```

---

### 📊 FULINS_S_20250830_01of05_firds_data.csv

- **Instrument Type**: S
- **Total Rows**: 500,000
- **Total Columns**: 31

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 323,861 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 76,037 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | float64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 466,872 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 496,495 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 498,479 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 498,479 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN | object | 497,889 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 499,999 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 36,747 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 493,200 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 493,203 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 499,999 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI | object | 499,887 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 499,998 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 499,998 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZ0XX8PK3511",
  "FinInstrmGnlAttrbts_FullNm": "Credit Swap Non_Standard Basket Multiple ISINs EUR 20280620",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Corp Basket EUR 20280620",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SCBCCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-03-21T17:53:53Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-06-20T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2028-06-20",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "BE6282460615",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-23",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null
}

// Row 2
{
  "Id": "EZ279H54S0L1",
  "FinInstrmGnlAttrbts_FullNm": "Credit Swap Non_Standard Basket Multiple ISINs EUR 20271220",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Corp Basket EUR 20271220",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SCBCCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2023-01-24T14:53:03Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-12-20T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2027-12-20",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "BE6282460615",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2023-12-23",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null
}

// Row 3
{
  "Id": "EZ3S6195JWG9",
  "FinInstrmGnlAttrbts_FullNm": "Credit Swap Non_Standard Basket Multiple ISINs EUR 20320620",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Corp Basket EUR 20320620",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SCBCCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-12-13T19:22:11Z",
  "TradgVnRltdAttrbts_TermntnDt": "2032-06-20T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2032-06-20",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "BE6301510028",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-12-17",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null
}

// Row 4
{
  "Id": "EZ4Q4H6S6XJ9",
  "FinInstrmGnlAttrbts_FullNm": "Credit Swap Non_Standard Basket Multiple ISINs EUR 20280710",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Corp Basket EUR 20280710",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SCBCCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-04-09T12:50:31Z",
  "TradgVnRltdAttrbts_TermntnDt": "2028-07-10T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2028-07-10",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "BE6282460615",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-12-20",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null
}

// Row 5
{
  "Id": "EZ53J8RNJ9N2",
  "FinInstrmGnlAttrbts_FullNm": "Credit Swap Non_Standard Basket Multiple ISINs EUR 20290110",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/CDS Corp Basket EUR 20290110",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SCBCCA",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "549300ZK53CNGEEI6A29",
  "TradgVnRltdAttrbts_Id": "JPEU",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-01-16T17:48:53Z",
  "TradgVnRltdAttrbts_TermntnDt": "2029-01-10T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2029-01-10",
  "DerivInstrmAttrbts_PricMltplr": "1.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": "BE6282460615",
  "DerivInstrmAttrbts_DlvryTp": "OPTL",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-01-18",
  "TechAttrbts_RlvntTradgVn": "JPEU",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null
}

```

---

### 📊 FULINS_S_20250830_02of05_firds_data.csv

- **Instrument Type**: S
- **Total Rows**: 500,000
- **Total Columns**: 26

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 297,940 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 35,415 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 206,794 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 499,997 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 499,997 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 421,602 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 421,602 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 200,923 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 200,923 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 469,118 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZN2YQ8J9GV9",
  "FinInstrmGnlAttrbts_FullNm": "Equity Swap Portfolio_Swap_Single_Name SE0000101362 SEK 20260407",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SStk Tot Rtn SEK 20260407",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SESTXC",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "R0MUWSFPU8MPRO8K5P83",
  "TradgVnRltdAttrbts_Id": "BNPS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-27T17:13:11Z",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "SE0000101362",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2025-06-17",
  "TechAttrbts_RlvntTradgVn": "BNPS",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null
}

// Row 2
{
  "Id": "EZN2YQSDGY69",
  "FinInstrmGnlAttrbts_FullNm": "Equity Swap Portfolio_Swap_Single_Name ID1000061302 USD 20250212",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SStk Tot Rtn USD 20250212",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SESTXC",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "R0MUWSFPU8MPRO8K5P83",
  "TradgVnRltdAttrbts_Id": "BNPS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-03-15T13:09:39Z",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "ID1000061302",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-03-16",
  "TechAttrbts_RlvntTradgVn": "BNPS",
  "DerivInstrmAttrbts_XpryDt": "2025-02-12",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null
}

// Row 3
{
  "Id": "EZN2YRX9JKG2",
  "FinInstrmGnlAttrbts_FullNm": "Equity Swap Portfolio_Swap_Single_Name US55024U1097 USD 20221216",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SStk Tot Rtn USD 20221216",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SESTXC",
  "FinInstrmGnlAttrbts_NtnlCcy": "USD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "R0MUWSFPU8MPRO8K5P83",
  "TradgVnRltdAttrbts_Id": "BNPS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-12-03T21:24:01Z",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "US55024U1097",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "DE",
  "TechAttrbts_PblctnPrd_FrDt": "2021-12-07",
  "TechAttrbts_RlvntTradgVn": "BNPS",
  "DerivInstrmAttrbts_XpryDt": "2022-12-16",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null
}

// Row 4
{
  "Id": "EZN2YT9N4584",
  "FinInstrmGnlAttrbts_FullNm": "Equity Swap Portfolio_Swap_Single_Name BE0003555639 EUR 20260305",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SStk Tot Rtn EUR 20260305",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SESTXC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "R0MUWSFPU8MPRO8K5P83",
  "TradgVnRltdAttrbts_Id": "BNPS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-10-30T17:11:48Z",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "BE0003555639",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "BE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-11-01",
  "TechAttrbts_RlvntTradgVn": "BNPS",
  "DerivInstrmAttrbts_XpryDt": "2026-03-05",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null
}

// Row 5
{
  "Id": "EZN2YYSFK9Y4",
  "FinInstrmGnlAttrbts_FullNm": "Equity Swap Portfolio_Swap_Single_Name ES0105630315 EUR 20250328",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SStk Tot Rtn EUR 20250328",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SESTXC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "R0MUWSFPU8MPRO8K5P83",
  "TradgVnRltdAttrbts_Id": "BNPS",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-04-30T19:07:04Z",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": "ES0105630315",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "TechAttrbts_RlvntCmptntAuthrty": "ES",
  "TechAttrbts_PblctnPrd_FrDt": "2025-03-21",
  "TechAttrbts_RlvntTradgVn": "BNPS",
  "DerivInstrmAttrbts_XpryDt": null,
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null
}

```

---

### 📊 FULINS_S_20250830_03of05_firds_data.csv

- **Instrument Type**: S
- **Total Rows**: 500,000
- **Total Columns**: 37

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 453,330 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 456,795 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 463 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp | object | 322,463 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy | object | 322,463 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 46,997 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN | object | 481,372 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN | object | 499,349 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 457,031 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 177,542 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 177,542 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd | float64 | 487,355 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 470,335 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 284,143 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 284,143 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy | object | 462,492 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm | object | 473,971 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit | object | 424,725 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val | float64 | 424,725 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 313,723 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 220,511 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx | object | 450,577 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZM7QNYL9BD3",
  "FinInstrmGnlAttrbts_FullNm": "Foreign_Exchange Swap EUR GBP 202112",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps EUR GBP 20211222",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SFCXXP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "1VUV7VQFKUOQSJ21A208",
  "TradgVnRltdAttrbts_Id": "AACA",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2021-03-11T10:52:57.44Z",
  "TradgVnRltdAttrbts_ReqForAdmssnDt": "2021-03-11T10:52:57.44Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-03-11T10:52:57.44Z",
  "DerivInstrmAttrbts_XpryDt": "2021-12-22",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": "FXMJ",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "EUR",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2021-03-13",
  "TechAttrbts_RlvntTradgVn": "AACA",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null
}

// Row 2
{
  "Id": "EZM7QS1V9CZ2",
  "FinInstrmGnlAttrbts_FullNm": "Foreign_Exchange Swap EUR USD 20280428",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps EUR USD 20280428",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SFCXXP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-21T02:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2028-04-28",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": "FXMJ",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "USD",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-24",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "TradgVnRltdAttrbts_TermntnDt": "2028-04-28T23:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null
}

// Row 3
{
  "Id": "EZM7QT4VQ7H4",
  "FinInstrmGnlAttrbts_FullNm": "Foreign_Exchange Swap SAR USD 20260721",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps SAR USD 20260721",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SFCXXP",
  "FinInstrmGnlAttrbts_NtnlCcy": "SAR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-07-16T01:07:51Z",
  "DerivInstrmAttrbts_XpryDt": "2026-07-21",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": "FXCR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "USD",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-25",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "TradgVnRltdAttrbts_TermntnDt": "2026-07-21T23:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null
}

// Row 4
{
  "Id": "EZM7R21VSNX0",
  "FinInstrmGnlAttrbts_FullNm": "Foreign_Exchange Swap AUD NZD 20251014",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps AUD NZD 20251014",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SFCXXP",
  "FinInstrmGnlAttrbts_NtnlCcy": "AUD",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-07-14T02:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2025-10-14",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": "FXCR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "NZD",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-07-16",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "TradgVnRltdAttrbts_TermntnDt": "2025-10-14T23:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null
}

// Row 5
{
  "Id": "EZM7R2K6TK20",
  "FinInstrmGnlAttrbts_FullNm": "Foreign_Exchange Swap THB USD 20260201",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swaps THB USD 20260201",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SFCXXP",
  "FinInstrmGnlAttrbts_NtnlCcy": "THB",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "O2RNE8IBXP4R0TD8PU41",
  "TradgVnRltdAttrbts_Id": "XSGA",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-02-10T01:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2026-02-01",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp": "FXCR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy": "USD",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-02-12",
  "TechAttrbts_RlvntTradgVn": "XSGA",
  "TradgVnRltdAttrbts_TermntnDt": "2026-02-01T23:59:59Z",
  "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null
}

```

---

### 📊 FULINS_S_20250830_04of05_firds_data.csv

- **Instrument Type**: S
- **Total Rows**: 500,000
- **Total Columns**: 33

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 6,881 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 424 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 233,092 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 119,966 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 119,966 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 117,964 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | int64 | 0 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 382,036 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy | object | 499,661 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx | object | 499,675 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit | object | 499,653 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val | float64 | 499,653 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 386,759 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 498,087 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd | float64 | 499,830 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm | object | 499,954 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 499,993 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZBWNHMCJ2G7",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float 37 YEAR EUR-EURIBOR-Reuters 3 MNTH 20580408",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap Fxd Flt EUR 20580408",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRCCSP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2021-04-06T06:50:44Z",
  "TradgVnRltdAttrbts_TermntnDt": "2058-04-08T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2058-04-08",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "37",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2021-04-07",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 2
{
  "Id": "EZBWNKYT1ZF0",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float EUR-EURIBOR-Reuters 6 MNTH 20190725",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap Fxd Flt EUR 20190725",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRCCSP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "3IOL70HIEQ2FWND3JI79",
  "TradgVnRltdAttrbts_Id": "HBFR",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2018-01-09T00:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": null,
  "DerivInstrmAttrbts_XpryDt": "2019-07-25",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "DAYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "554",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2021-01-03",
  "TechAttrbts_RlvntTradgVn": "HBFR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "EUR-EURIBOR-Reuters",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": "EUR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": "DAYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": "554.0",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 3
{
  "Id": "EZBWNPZ9LHS7",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float 3 YEAR SEK-STIBOR 3 MNTH 20271021",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap Fxd Flt SEK 20271021",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRCCSP",
  "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "5RJTDGZG4559ESIYLD31",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2024-10-18T22:30:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-10-21T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2027-10-21",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": "STBO",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "STBO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3",
  "TechAttrbts_RlvntCmptntAuthrty": "SE",
  "TechAttrbts_PblctnPrd_FrDt": "2024-10-23",
  "TechAttrbts_RlvntTradgVn": "AURO",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 4
{
  "Id": "EZBWNRFW7Z21",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float 30 YEAR EUR-EURIBOR-Reuters 3 MNTH 20501104",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap Fxd Flt EUR 20501104",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRCCSP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "724500D4BFEWKWVC1G62",
  "TradgVnRltdAttrbts_Id": "TWEM",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2020-11-02T08:02:54Z",
  "TradgVnRltdAttrbts_TermntnDt": "2050-11-04T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2050-11-04",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "30",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2024-01-16",
  "TechAttrbts_RlvntTradgVn": "TWEM",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

// Row 5
{
  "Id": "EZBWNRM1H6N5",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float 2 YEAR EUR-EURIBOR-Reuters 3 MNTH 20270121",
  "FinInstrmGnlAttrbts_ShrtNm": "EUR SWAP VS 3M 2YR",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRCCSP",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "254900QBKK4WBSO3GE51",
  "TradgVnRltdAttrbts_Id": "AURO",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-20T12:10:28Z",
  "TradgVnRltdAttrbts_TermntnDt": "2027-01-21T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2027-01-21",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "PHYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EURI",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "2",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-01-22",
  "TechAttrbts_RlvntTradgVn": "BTFE",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null
}

```

---

### 📊 FULINS_S_20250830_05of05_firds_data.csv

- **Instrument Type**: S
- **Total Rows**: 266,374
- **Total Columns**: 42

#### Column Structure

| Column Name | Data Type | Null Count | Unique Count | Sample Values |
|-------------|-----------|------------|--------------|---------------|
| Id | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_FullNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ShrtNm | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_ClssfctnTp | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_NtnlCcy | object | 0 | N/A |  |
| FinInstrmGnlAttrbts_CmmdtyDerivInd | bool | 0 | N/A |  |
| Issr | object | 0 | N/A |  |
| TradgVnRltdAttrbts_Id | object | 0 | N/A |  |
| TradgVnRltdAttrbts_IssrReq | bool | 0 | N/A |  |
| TradgVnRltdAttrbts_AdmssnApprvlDtByIssr | object | 266,275 | N/A |  |
| TradgVnRltdAttrbts_FrstTradDt | object | 0 | N/A |  |
| TradgVnRltdAttrbts_TermntnDt | object | 2,984 | N/A |  |
| DerivInstrmAttrbts_XpryDt | object | 162 | N/A |  |
| DerivInstrmAttrbts_PricMltplr | int64 | 0 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx | object | 189,393 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit | object | 39,565 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val | float64 | 39,565 | N/A |  |
| DerivInstrmAttrbts_DlvryTp | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx | object | 169,115 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit | object | 58 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val | float64 | 58 | N/A |  |
| TechAttrbts_RlvntCmptntAuthrty | object | 0 | N/A |  |
| TechAttrbts_PblctnPrd_FrDt | object | 0 | N/A |  |
| TechAttrbts_RlvntTradgVn | object | 0 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm | object | 97,317 | N/A |  |
| DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm | object | 116,477 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm | object | 266,138 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit | object | 265,792 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val | float64 | 265,792 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx | object | 265,880 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy | object | 265,845 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd | float64 | 266,370 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct | object | 266,331 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct | object | 266,331 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct | object | 266,331 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp | object | 266,316 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp | object | 266,358 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct | object | 266,361 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct | object | 266,361 | N/A |  |
| TradgVnRltdAttrbts_ReqForAdmssnDt | object | 266,372 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct | object | 266,372 | N/A |  |
| DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct | object | 266,372 | N/A |  |

#### First 5 Rows Sample

```json
// Row 1
{
  "Id": "EZXY13YZW2B3",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float_OIS 10 YEAR EUR-EONIA-OIS-COMPOUND 1 DAYS 20291010",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap OIS EUR 20291010",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRHCSC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2138004TYNQCB7MLTG76",
  "TradgVnRltdAttrbts_Id": "RESF",
  "TradgVnRltdAttrbts_IssrReq": "True",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2019-10-03T16:18:09.737Z",
  "TradgVnRltdAttrbts_FrstTradDt": "2019-10-08T08:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2029-10-10T23:59:59Z",
  "DerivInstrmAttrbts_XpryDt": "2029-10-10",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": "EONA",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "DAYS",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "1.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": "EONA",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "YEAR",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "10.0",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2022-09-29",
  "TechAttrbts_RlvntTradgVn": "RESF",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null
}

// Row 2
{
  "Id": "EZXZ9RCN3P36",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float_OIS 10 YEAR EUR-EuroSTR-OIS Compound 1 DAYS 20350115",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap OIS EUR 20350115",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRHCSC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "969500AMLHB21RACL168",
  "TradgVnRltdAttrbts_Id": "HPCV",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-01-13T00:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2035-01-15T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2035-01-15",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "DAYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "1.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2025-01-14",
  "TechAttrbts_RlvntTradgVn": "HPCV",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "EUR-EuroSTR-OIS Compound",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null
}

// Row 3
{
  "Id": "EZXZZ7ZXCRB9",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float_OIS 7 YEAR EUR-EuroSTR-OIS Compound 1 DAYS 20310801",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap OIS EUR 20310801",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRHCSC",
  "FinInstrmGnlAttrbts_NtnlCcy": "EUR",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "969500AMLHB21RACL168",
  "TradgVnRltdAttrbts_Id": "HPCV",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2024-07-30T00:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2031-08-01T00:00:00Z",
  "DerivInstrmAttrbts_XpryDt": "2031-08-01",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": null,
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "DAYS",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "1.0",
  "TechAttrbts_RlvntCmptntAuthrty": "FR",
  "TechAttrbts_PblctnPrd_FrDt": "2024-07-31",
  "TechAttrbts_RlvntTradgVn": "HPCV",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "EUR-EuroSTR-OIS Compound",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null
}

// Row 4
{
  "Id": "EZY1XJ3FTGD5",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float_OIS 3 MNTH KRW-CD 91D 3 MNTH 20260128",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap OIS KRW 20260128",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRHCSC",
  "FinInstrmGnlAttrbts_NtnlCcy": "KRW",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2138004TYNQCB7MLTG76",
  "TradgVnRltdAttrbts_Id": "RESF",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-05-22T00:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2025-10-27T23:59:59.999Z",
  "DerivInstrmAttrbts_XpryDt": "2026-01-28",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-05-23",
  "TechAttrbts_RlvntTradgVn": "RESF",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "CD 91D",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "CD 91D",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null
}

// Row 5
{
  "Id": "EZY2H1DJGXB0",
  "FinInstrmGnlAttrbts_FullNm": "Rates Swap Fixed_Float_OIS 3 MNTH KRW-CD 91D 3 MNTH 20260509",
  "FinInstrmGnlAttrbts_ShrtNm": "NA/Swap OIS KRW 20260509",
  "FinInstrmGnlAttrbts_ClssfctnTp": "SRHCSC",
  "FinInstrmGnlAttrbts_NtnlCcy": "KRW",
  "FinInstrmGnlAttrbts_CmmdtyDerivInd": "False",
  "Issr": "2138004TYNQCB7MLTG76",
  "TradgVnRltdAttrbts_Id": "RESF",
  "TradgVnRltdAttrbts_IssrReq": "False",
  "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": null,
  "TradgVnRltdAttrbts_FrstTradDt": "2025-08-27T00:00:00Z",
  "TradgVnRltdAttrbts_TermntnDt": "2026-02-06T23:59:59.999Z",
  "DerivInstrmAttrbts_XpryDt": "2026-05-09",
  "DerivInstrmAttrbts_PricMltplr": "1",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx": null,
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val": "3.0",
  "DerivInstrmAttrbts_DlvryTp": "CASH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit": "MNTH",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val": "3.0",
  "TechAttrbts_RlvntCmptntAuthrty": "NL",
  "TechAttrbts_PblctnPrd_FrDt": "2025-08-28",
  "TechAttrbts_RlvntTradgVn": "RESF",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm": "CD 91D",
  "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm": "CD 91D",
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct": null,
  "TradgVnRltdAttrbts_ReqForAdmssnDt": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct": null,
  "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct": null
}

```

---

## Pattern Analysis

### Common Columns (Present in All Types)

- `FinInstrmGnlAttrbts_ClssfctnTp`
- `FinInstrmGnlAttrbts_CmmdtyDerivInd`
- `FinInstrmGnlAttrbts_FullNm`
- `FinInstrmGnlAttrbts_NtnlCcy`
- `FinInstrmGnlAttrbts_ShrtNm`
- `Id`
- `Issr`
- `TechAttrbts_PblctnPrd_FrDt`
- `TechAttrbts_RlvntCmptntAuthrty`
- `TechAttrbts_RlvntTradgVn`
- `TradgVnRltdAttrbts_FrstTradDt`
- `TradgVnRltdAttrbts_Id`
- `TradgVnRltdAttrbts_IssrReq`
- `TradgVnRltdAttrbts_TermntnDt`

### Type-Specific Columns

#### Type C Specific Columns

- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type D Specific Columns

- `DebtInstrmAttrbts_DebtSnrty`
- `DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd`
- `DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN`
- `DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx`
- `DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm`
- `DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit`
- `DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val`
- `DebtInstrmAttrbts_IntrstRate_Fxd`
- `DebtInstrmAttrbts_MtrtyDt`
- `DebtInstrmAttrbts_NmnlValPerUnit`
- `DebtInstrmAttrbts_TtlIssdNmnlAmt`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type E Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type F Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type H Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_OptnExrcStyle`
- `DerivInstrmAttrbts_OptnTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_StrkPric_NoPric_Ccy`
- `DerivInstrmAttrbts_StrkPric_NoPric_Pdg`
- `DerivInstrmAttrbts_StrkPric_Pric_BsisPts`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn`
- `DerivInstrmAttrbts_StrkPric_Pric_Pctg`
- `DerivInstrmAttrbts_StrkPric_Pric_Yld`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type I Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`

#### Type J Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type O Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_OptnExrcStyle`
- `DerivInstrmAttrbts_OptnTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_StrkPric_Pric_BsisPts`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn`
- `DerivInstrmAttrbts_StrkPric_Pric_Pctg`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type R Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_OptnExrcStyle`
- `DerivInstrmAttrbts_OptnTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_StrkPric_NoPric_Ccy`
- `DerivInstrmAttrbts_StrkPric_NoPric_Pdg`
- `DerivInstrmAttrbts_StrkPric_Pric_BsisPts`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt`
- `DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn`
- `DerivInstrmAttrbts_StrkPric_Pric_Pctg`
- `DerivInstrmAttrbts_StrkPric_Pric_Yld`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

#### Type S Specific Columns

- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val`
- `DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy`
- `DerivInstrmAttrbts_DlvryTp`
- `DerivInstrmAttrbts_PricMltplr`
- `DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val`
- `DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI`
- `DerivInstrmAttrbts_XpryDt`
- `TradgVnRltdAttrbts_AdmssnApprvlDtByIssr`
- `TradgVnRltdAttrbts_ReqForAdmssnDt`

### Complete Column Listing by Type

#### Type C - All 17 Columns

```
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type D - All 45 Columns

```
DebtInstrmAttrbts_DebtSnrty
DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd
DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN
DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx
DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm
DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit
DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val
DebtInstrmAttrbts_IntrstRate_Fxd
DebtInstrmAttrbts_MtrtyDt
DebtInstrmAttrbts_NmnlValPerUnit
DebtInstrmAttrbts_TtlIssdNmnlAmt
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type E - All 28 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type F - All 70 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Ptt_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_RnwblNrgy_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_Pulp_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Ppr_RcvrdPpr_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type H - All 44 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fxd
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_OptnExrcStyle
DerivInstrmAttrbts_OptnTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_StrkPric_NoPric_Ccy
DerivInstrmAttrbts_StrkPric_NoPric_Pdg
DerivInstrmAttrbts_StrkPric_Pric_BsisPts
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn
DerivInstrmAttrbts_StrkPric_Pric_Pctg
DerivInstrmAttrbts_StrkPric_Pric_Yld
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type I - All 19 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_TermntnDt
```

#### Type J - All 44 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_Dlvrbl_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type O - All 49 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_OptnExrcStyle
DerivInstrmAttrbts_OptnTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_StrkPric_Pric_BsisPts
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn
DerivInstrmAttrbts_StrkPric_Pric_Pctg
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type R - All 63 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_LiveStock_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Soft_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_OptnExrcStyle
DerivInstrmAttrbts_OptnTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_StrkPric_NoPric_Ccy
DerivInstrmAttrbts_StrkPric_NoPric_Pdg
DerivInstrmAttrbts_StrkPric_Pric_BsisPts
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt
DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn
DerivInstrmAttrbts_StrkPric_Pric_Pctg
DerivInstrmAttrbts_StrkPric_Pric_Yld
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

#### Type S - All 48 Columns

```
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Coal_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Indx
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Unit
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_Term_Val
DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy
DerivInstrmAttrbts_DlvryTp
DerivInstrmAttrbts_PricMltplr
DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI
DerivInstrmAttrbts_XpryDt
FinInstrmGnlAttrbts_ClssfctnTp
FinInstrmGnlAttrbts_CmmdtyDerivInd
FinInstrmGnlAttrbts_FullNm
FinInstrmGnlAttrbts_NtnlCcy
FinInstrmGnlAttrbts_ShrtNm
Id
Issr
TechAttrbts_PblctnPrd_FrDt
TechAttrbts_RlvntCmptntAuthrty
TechAttrbts_RlvntTradgVn
TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
TradgVnRltdAttrbts_FrstTradDt
TradgVnRltdAttrbts_Id
TradgVnRltdAttrbts_IssrReq
TradgVnRltdAttrbts_ReqForAdmssnDt
TradgVnRltdAttrbts_TermntnDt
```

## Model Design Recommendations

### Current Instrument Model Analysis

The current `Instrument` model uses a unified approach with:

- **Core identification fields**: `id`, `isin`, `instrument_type`
- **Essential common fields**: `full_name`, `short_name`, `currency`, `cfi_code`, `lei_id`
- **JSON document storage**: `firds_data`, `processed_attributes`
- **Type-specific formatting**: Methods for equity, debt, future attributes

### Recommended Changes Based on Analysis

Based on the FIRDS reference data analysis above, consider:

1. **Expand instrument_type values** to handle all FIRDS instrument types (C, D, E, F, H, I, J, S, R, O)
2. **Review common columns** - these should be promoted to dedicated database columns for better performance
3. **Update type-specific formatters** - add methods for each instrument type found in FIRDS
4. **Consider data type mappings** - ensure proper handling of dates, numbers, text fields, etc.
5. **Update service layer** - modify FIRDS parsing logic to handle all instrument types
6. **Map FIRDS types to business logic** - determine how each FIRDS type maps to internal instrument categories

### Next Steps

1. Review this analysis report
2. Identify which columns should become dedicated database fields vs JSON storage
3. Plan the mapping from FIRDS instrument types to internal instrument_type values
4. Update the instrument model, service layer, and routes accordingly
5. Test data ingestion for all FIRDS instrument types

