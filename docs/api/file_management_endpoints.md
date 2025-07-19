# File Management API - Complete Guide

This document is the **comprehensive reference** for all file management operations in the MarketDataAPI. It covers downloading, parsing, organizing, and managing ESMA FIRDS and FITRS data files.

> ✅ **Production Ready**: All endpoints have been tested with real data including multi-part downloads of 1.24M+ records.

## Base URL
All endpoints assume the Flask app is running on `http://localhost:5000`

## Available Endpoints

### 1. Download by Criteria (Main Endpoint)
**Endpoint:** `POST /api/v1/files/download-by-criteria`

Downloads and parses ESMA files based on specific criteria.

**Request Body:**
```json
{
    "file_type": "firds",           // Required: "firds" or "fitrs"
    "dataset": "FULINS_E",          // Optional: Dataset type
    "date": "2024-01-15",           // Optional: Specific date (YYYY-MM-DD)
    "date_range": ["2024-01-01", "2024-01-31"],  // Optional: Date range (uses latest)
    "force_update": false           // Optional: Re-download existing files
}
```

**Parameters:**
- `file_type` (required): "firds" or "fitrs"
- `dataset` (optional): 
  - For FIRDS: "FULINS_E" (equity), "FULINS_D" (debt), "FULINS_F" (futures), "FULINS_C", "DELVINS"
  - For FITRS: "FITRS", "DVCAP", "DVCRES"
- `date` (optional): Specific date in YYYY-MM-DD format
- `date_range` (optional): Array of [start_date, end_date] - when provided, uses the latest file in range
- `force_update` (optional): Boolean, whether to re-download existing files (default: false)

**Response:**
```json
{
    "success": true,
    "message": "Processed 1 firds files",
    "files_processed": 1,
    "criteria": {
        "file_type": "firds",
        "dataset": "FULINS_E",
        "date": null,
        "date_range": null,
        "force_update": false
    },
    "date_range_used": {
        "from": "2024-01-01",
        "to": "2024-12-31",
        "latest_only": false
    },
    "files_downloaded": ["FULINS_20240115_E_1of1_firds_data.csv"],
    "files_skipped": [],
    "files_failed": []
}
```

### 2. List Files with Filters
**Endpoint:** `GET /api/v1/files`

Lists all files with optional filtering.

**Query Parameters:**
- `file_type`: "firds" or "fitrs"
- `dataset_type`: Dataset type to filter by
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
- `limit`: Maximum number of files to return

**Example:** `GET /api/v1/files?file_type=firds&dataset_type=FULINS_E&limit=10`

### 3. List Available ESMA Files
**Endpoint:** `GET /api/v1/esma-files`

Lists files available from the ESMA registry.

**Query Parameters:**
- `file_type`: "firds" or "fitrs"
- `limit`: Maximum number of files to return (default: 50)

### 4. Batch Download and Parse
**Endpoint:** `POST /api/v1/files/download`

Downloads and parses multiple files from URLs.

**Request Body:**
```json
{
    "urls": ["http://example.com/file1.zip", "http://example.com/file2.zip"],
    "force_update": false
}
```

### 5. File Statistics
**Endpoint:** `GET /api/v1/files/stats/detailed`

Get detailed file statistics with filters.

**Query Parameters:**
- `file_type`: "firds" or "fitrs"
- `dataset_type`: Dataset type to filter by
- `date_from`: Start date for filtering
- `date_to`: End date for filtering

### 6. Simple File Statistics
**Endpoint:** `GET /api/v1/files/stats`

Get basic file statistics by type.

### 7. File Cleanup
**Endpoint:** `POST /api/v1/files/cleanup`

Remove old files based on retention policy.

**Request Body:**
```json
{
    "dry_run": true,
    "retention_days": 30
}
```

### 8. Delete Files
**Endpoint:** `DELETE /api/v1/files/delete`

Delete specific files.

**Request Body:**
```json
{
    "file_names": ["file1.csv", "file2.csv"]
}
```

### 9. Organize Files
**Endpoint:** `POST /api/v1/files/organize`

Organize files into proper folder structure.

### 10. File Summary
**Endpoint:** `GET /api/v1/files/summary`

Get a summary of all files and storage usage.

## Usage Examples

### Download Latest FIRDS Equity File
```bash
curl -X POST http://localhost:5000/api/v1/files/download-by-criteria \
  -H "Content-Type: application/json" \
  -d '{
    "file_type": "firds",
    "dataset": "FULINS_E"
  }'
```

### Download FIRDS File for Specific Date
```bash
curl -X POST http://localhost:5000/api/v1/files/download-by-criteria \
  -H "Content-Type: application/json" \
  -d '{
    "file_type": "firds",
    "dataset": "FULINS_E",
    "date": "2024-01-15"
  }'
```

### Download Latest File in Date Range
```bash
curl -X POST http://localhost:5000/api/v1/files/download-by-criteria \
  -H "Content-Type: application/json" \
  -d '{
    "file_type": "firds",
    "dataset": "FULINS_E",
    "date_range": ["2024-01-01", "2024-01-31"]
  }'
```

### Force Re-download Existing File
```bash
curl -X POST http://localhost:5000/api/v1/files/download-by-criteria \
  -H "Content-Type: application/json" \
  -d '{
    "file_type": "firds",
    "dataset": "FULINS_D",
    "force_update": true
  }'
```

### List FIRDS Files with Filters
```bash
curl "http://localhost:5000/api/v1/files?file_type=firds&dataset_type=FULINS_E&limit=5"
```

## Dataset Types

### FIRDS (Financial Instrument Reference Data System)
- `FULINS_E`: Equity instruments
- `FULINS_D`: Debt instruments  
- `FULINS_F`: Futures/derivatives
- `FULINS_C`: Other instruments
- `DELVINS`: Delisted instruments

### FITRS (Financial Instrument Transparency System)
- `FITRS`: General FITRS data
- `DVCAP`: Data validation capacity
- `DVCRES`: Data validation results

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `404`: Resource not found
- `500`: Internal server error

Error responses include detailed error messages:
```json
{
    "error": "file_type is required (firds or fitrs)"
}
```

## File Storage Structure

Downloaded files are stored in:
- FIRDS files: `downloads/firds/`
- FITRS files: `downloads/fitrs/`

Files are named with meaningful names like:
- `FULINS_20240115_E_1of1_firds_data.csv`
- `FULINS_20240115_D_1of1_firds_data.csv`

## Notes

1. The `download-by-criteria` endpoint is the primary way to download files by date, type, and dataset
2. If both `date` and `date_range` are provided, `date_range` takes precedence
3. When `date_range` is used, only the latest file in that range is downloaded
4. Files are automatically parsed after download and stored in CSV format
5. Original ZIP files are not retained after parsing to save space
6. The system automatically handles file organization and cleanup
