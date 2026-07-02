"""Download public healthcare PDF documents for the RAG assistant.

Run from project root:
    python scripts/download_public_pdfs.py

The PDFs are downloaded from original public source URLs and saved into docs/.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"

PUBLIC_PDF_SOURCES = [
    {
        "filename": "appointment_policy.pdf",
        "url": "https://hospitals.aku.edu/pakistan/health-solutions/Documents/Frequently%20Asked%20Questions%2C%20Teleclinics.pdf",
        "purpose": "Appointment booking / tele-clinic booking process",
    },
    {
        "filename": "arrival_time_policy.pdf",
        "url": "https://hospitals.aku.edu/pakistan/patients-families/Documents/Appointment%20for%20CT%20Scan.pdf",
        "purpose": "Arrival-before-appointment guidance",
    },
    {
        "filename": "doctor_schedule.pdf",
        "url": "https://iph.punjab.gov.pk/system/files/Standard%20Operating%20Procedures%20%20Family%20clinic.pdf",
        "purpose": "Clinic scheduling, operating practices, walk-in availability",
    },
    {
        "filename": "lab_test_instructions.pdf",
        "url": "https://idc.net.pk/wp-content/themes/idc/assets/pdf/health-packages-broucher-idc.pdf",
        "purpose": "Fasting and lab-test preparation guidance",
    },
    {
        "filename": "medicine_refill_policy.pdf",
        "url": "https://sabinecountyhospital.com/wp-content/uploads/2023/05/Prescription-Refill-Policy.pdf",
        "purpose": "Medicine refill policy example",
    },
    {
        "filename": "emergency_policy.pdf",
        "url": "https://www.pmuhealth.gop.pk/wp-content/uploads/2020/09/emergency-manual-guidelines.pdf",
        "purpose": "Emergency guidance and urgent-care flow",
    },
    {
        "filename": "consultation_fees.pdf",
        "url": "https://hcc.kp.gov.pk/wp-content/uploads/2024/11/MSDS-for-GP-and-Specialist-Clinics.pdf",
        "purpose": "Consultation fees/tariff display and clinic standards",
    },
    {
        "filename": "report_collection_policy.pdf",
        "url": "https://hcc.kp.gov.pk/wp-content/uploads/2023/12/MSDS-for-Collection-Centers-of-Clinical-Laboratories.pdf",
        "purpose": "Report collection / lab collection center standards",
    },
]


def _safe_url(url: str) -> str:
    """Percent-encode path spaces while preserving existing escapes."""
    split = urlsplit(url)
    path = quote(split.path, safe="/%")
    return urlunsplit((split.scheme, split.netloc, path, split.query, split.fragment))


def _download_one(url: str, destination: Path) -> bool:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )
    }
    response = requests.get(_safe_url(url), headers=headers, timeout=60)
    response.raise_for_status()

    content = response.content
    if not content.startswith(b"%PDF"):
        # Some servers return a valid PDF with extra bytes before %PDF, so do a softer check.
        if b"%PDF" not in content[:1024]:
            print(f"Warning: {destination.name} may not be a PDF. Saving response anyway.")

    destination.write_bytes(content)
    return True


def download_public_pdfs() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Saving PDFs into: {DOCS_DIR}")
    failed: list[dict[str, str]] = []

    for item in PUBLIC_PDF_SOURCES:
        destination = DOCS_DIR / item["filename"]
        print(f"Downloading {item['filename']} ...")
        try:
            _download_one(item["url"], destination)
            print(f"  saved: {destination}")
        except Exception as exc:
            failed.append(item)
            print(f"  failed: {exc}")

    if failed:
        print("\nSome PDFs could not be downloaded automatically.")
        print("Open these URLs manually in your browser, download them, and rename as shown:")
        for item in failed:
            print(f"- {item['filename']}: {item['url']}")
    else:
        print("\nAll public PDFs downloaded successfully.")


if __name__ == "__main__":
    download_public_pdfs()
