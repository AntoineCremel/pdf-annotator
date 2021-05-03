#! /usr/bin/python3

import re
import json
from google.cloud import storage
from google.cloud import vision

def pdf_ocr(bucket_name, blob_names, data_dir="raw_ocr/"):
    mime_type = 'application/pdf'
    # How many pages should be grouped into each json output file.
    batch_size = 2
    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(
            type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    async_requests = []

    print("Reading file(s): ")
    for blob_name in blob_names:
        source_uri = "gs://" + bucket_name + '/' + blob_name
        print("Reading {}...".format(source_uri))
        gcs_source = vision.GcsSource(uri=source_uri)
        input_config = vision.InputConfig(
            gcs_source=gcs_source, mime_type=mime_type)

        destination_uri = "gs://" + bucket_name + '/' + data_dir + blob_name
        print("Saving raw ocr data to {}...".format(destination_uri))
        gcs_destination = vision.GcsDestination(uri=destination_uri)
        output_config = vision.OutputConfig(
            gcs_destination=gcs_destination, batch_size=batch_size)

        async_request = vision.AsyncAnnotateFileRequest(
            features=[feature], input_config=input_config,
            output_config=output_config)

        async_requests.append(async_request)

    operation = client.async_batch_annotate_files(
        requests=async_requests)

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)
    print('Done')

if __name__ == "__main__":
    pdf_ocr(bucket_name="vision-project-311920.appspot.com", blob_names=["AttestationDroits_du_13-08-2018 (1) (2).pdf"])