import vision_analyzer
import ocr
import sys
import getopt

bucket_name = "vision-project-311920.appspot.com"
blobs_to_read = ["AttestationDroits_du_13-08-2018 (1) (2).pdf", "AttestationDroits__4.pdf"]

# Run google's extraction process
ocr.pdf_ocr(bucket_name=bucket_name, blob_names=blobs_to_read)
# Extract data from the files
vision_analyzer.json_extract(bucket_name=bucket_name)