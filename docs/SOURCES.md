# Public PDF Sources for the Clinic RAG Assistant

The project is designed to use PDF documents downloaded from public healthcare-related websites. Run the downloader from the project root:

```bash
python scripts/download_public_pdfs.py
```

The downloader saves the files into this `docs/` folder using the exact filenames expected by the RAG pipeline.

| Local Filename | Source URL | Purpose |
|---|---|---|
| `appointment_policy.pdf` | https://hospitals.aku.edu/pakistan/health-solutions/Documents/Frequently%20Asked%20Questions%2C%20Teleclinics.pdf | Appointment booking / tele-clinic booking process |
| `arrival_time_policy.pdf` | https://hospitals.aku.edu/pakistan/patients-families/Documents/Appointment%20for%20CT%20Scan.pdf | Arrival-before-appointment guidance |
| `doctor_schedule.pdf` | https://iph.punjab.gov.pk/system/files/Standard%20Operating%20Procedures%20%20Family%20clinic.pdf | Clinic scheduling, operating practices, walk-in availability |
| `lab_test_instructions.pdf` | https://idc.net.pk/wp-content/themes/idc/assets/pdf/health-packages-broucher-idc.pdf | Fasting and lab-test preparation guidance |
| `medicine_refill_policy.pdf` | https://sabinecountyhospital.com/wp-content/uploads/2023/05/Prescription-Refill-Policy.pdf | Medicine refill policy example |
| `emergency_policy.pdf` | https://www.pmuhealth.gop.pk/wp-content/uploads/2020/09/emergency-manual-guidelines.pdf | Emergency guidance and urgent-care flow |
| `consultation_fees.pdf` | https://hcc.kp.gov.pk/wp-content/uploads/2024/11/MSDS-for-GP-and-Specialist-Clinics.pdf | Consultation fees/tariff display and clinic standards |
| `report_collection_policy.pdf` | https://hcc.kp.gov.pk/wp-content/uploads/2023/12/MSDS-for-Collection-Centers-of-Clinical-Laboratories.pdf | Report collection / lab collection center standards |

> Note: These PDFs belong to their respective source organizations. They are not authored by this project. The script downloads them from the original public URLs for educational RAG testing.
