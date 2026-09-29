import re
from pathlib import Path
import fitz  # PyMuPDF


FIELD_LABELS = {
    "policyNumber": ["Policy Number"],
    "policyholderName": ["Policyholder Name", "Policy Holder Name"],
    "effectiveDates": ["Effective Dates", "Policy Effective Dates"],
    "incidentDate": ["Incident Date", "Date of Incident"],
    "incidentTime": ["Incident Time", "Time of Incident"],
    "location": ["Location", "Incident Location", "Loss Location"],
    "description": ["Description", "Incident Description", "Loss Description"],
    "claimant": ["Claimant"],
    "thirdParties": ["Third Parties", "Third Party"],
    "contactDetails": ["Contact Details", "Contact"],
    "assetType": ["Asset Type"],
    "assetId": ["Asset ID", "Vehicle ID", "Registration Number"],
    "estimatedDamage": ["Estimated Damage", "Estimated Damage Amount"],
    "claimType": ["Claim Type"],
    "attachments": ["Attachments", "Attachment"],
    "initialEstimate": ["Initial Estimate", "Initial Damage Estimate"],
}


def read_document(file_name: str, file_bytes: bytes) -> str:
    """Read TXT or PDF content."""
    suffix = Path(file_name).suffix.lower()
    if suffix == ".txt":
        return file_bytes.decode("utf-8", errors="ignore")
    if suffix == ".pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    raise ValueError("Only PDF and TXT files are supported.")


def _clean_value(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _extract_labeled(text: str, labels: list[str]) -> str | None:
    """Extract a value from 'Label: value' style lines."""

    for label in labels:
        # Use spaces/tabs instead of \s so the pattern
        # never crosses into the next line.
        pattern = rf"(?im)^[ \t]*{re.escape(label)}[ \t]*:[ \t]*(.*?)[ \t]*$"

        match = re.search(pattern, text)

        if match:
            value = _clean_value(match.group(1))

            # "None" is a valid answer for Third Parties.
            if label in ["Third Parties", "Third Party"] and value.lower() == "none":
                return "None"

            # Empty/placeholder values are considered missing.
            if value and value.lower() not in {
                "none",
                "n/a",
                "na",
                "-",
                "not provided"
            }:
                return value

            return None

    return None

def _extract_money(value: str | None):
    if not value:
        return None
    match = re.search(r"(\d[\d,]*(?:\.\d+)?)", value.replace("₹", ""))
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def extract_fields(text: str) -> dict:
    fields = {}
    for key, labels in FIELD_LABELS.items():
        fields[key] = _extract_labeled(text, labels)

    fields["estimatedDamage"] = _extract_money(fields["estimatedDamage"])
    fields["initialEstimate"] = _extract_money(fields["initialEstimate"])

    return fields
