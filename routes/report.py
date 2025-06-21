import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    tags=["feedback"],
    responses={404: {"description": "Not found"}},
)

# Set up the path for error logs
ERROR_LOG_PATH = Path(__file__).parent.parent / "data" / "error_reports.json"

# Create the error log file if it doesn't exist
def initialize_error_log():
    if not ERROR_LOG_PATH.exists():
        with open(ERROR_LOG_PATH, "w") as f:
            json.dump([], f)

# Ensure the error log exists
initialize_error_log()

class ErrorReport(BaseModel):
    original_text: str
    incorrect_translation: str
    expected_translation: str = None
    notes: str = None

class ReportResponse(BaseModel):
    success: bool
    message: str
    report_id: str = None

@router.post("/report-error", response_model=ReportResponse)
async def report_error(report: ErrorReport):
    """
    Submit a report for an incorrect translation
    """
    try:
        # Load existing reports
        with open(ERROR_LOG_PATH, "r") as f:
            reports = json.load(f)
        
        # Create a new report with timestamp and ID
        timestamp = datetime.now().isoformat()
        report_id = f"ERR-{len(reports) + 1:04d}"
        
        new_report = {
            "id": report_id,
            "timestamp": timestamp,
            "original_text": report.original_text,
            "incorrect_translation": report.incorrect_translation,
            "expected_translation": report.expected_translation,
            "notes": report.notes,
            "status": "pending"
        }
        
        # Add to reports and save
        reports.append(new_report)
        
        with open(ERROR_LOG_PATH, "w") as f:
            json.dump(reports, f, indent=2)
        
        return {
            "success": True,
            "message": "Error report submitted successfully",
            "report_id": report_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save error report: {str(e)}"
        ) 