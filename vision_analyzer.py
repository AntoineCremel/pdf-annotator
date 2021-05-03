import json
import re
from google.cloud import storage

def read_uri(gcs_input_uri):
    match = re.match(r'gs://([^/]+)/(.+)', gcs_input_uri)
    bucket_name = match.group(1)
    file_name = match.group(2)

    return bucket_name, file_name

def save_to_gcs_json(result, bucket, output_name):
    print("Saving results to {}".format(output_name))
    to_save = json.dumps(result, indent=4)
    blob = bucket.blob(output_name)
    blob.upload_from_string(to_save)

def json_extract(bucket_name, input_dir="raw_ocr/"):
    """
    Open the json files contained at the directory inside your google bucket
    Read the content and try to generate a new json with
    all the useful data

    In our current version, we ignore all data about the position
    and shape of each element of text. Instead, we just take the raw
    text string at the end of the JSON and try to make sense of that.
    """
    # Get the json string from the gcs
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    print("Looking into bucket {}".format(bucket_name))
    # Find the list 
    blobs = storage_client.list_blobs(bucket, prefix=input_dir)

    for blob in blobs:
        # Skip "directories"
        if blob.name[-1] == '/':
            continue
        json_string = blob.download_as_bytes()
        print("Successfully loaded string data from {}".format(blob.name))
        # Turn it into a dict
        response = json.loads(json_string)

        # Extract the full text
        pages = response['responses']
        result = dict()
        print("{} pages to look through".format(len(pages)))

        for page in pages:
            text = page['fullTextAnnotation']['text']
            page_extract(text, result)

        print(result)
        # Create the name of the file
        # step back in the directories
        new_name = blob.name[len(input_dir):]
        new_name = new_name.split(".pdf")[0]
        new_name += "_extracted.json"
        save_to_gcs_json(result, bucket, new_name)

def page_extract(page_text, result):
    lines = page_text.split("\n")
    for i in range(len(lines)):
        # Check if we have any semi colon
        if ':' in lines[i]:
            semi_colon_split = lines[i].split(":")
            if len(semi_colon_split) == 2:
                if semi_colon_split[1].strip() != '':
                    # If we found text before and after the semi colon, just create a dict entry
                    result[semi_colon_split[0].strip()] = semi_colon_split[1].strip()
                    print("Found an association on the line {}".format(lines[i]))
                else:
                    # Otherwise read the next line
                    result[semi_colon_split[0].strip()] = lines[i+1].strip()
                    print("Found an association on the lines {} and {}".format(lines[i], lines[i+1]))
        
        # Look for the file's validity date
        if "Valable du" in lines[i]:
            pass
            #parser.parse(lines[i][])

if __name__ == "__main__":
    json_extract("gs://vision-project-311920.appspot.com/AttestationDroits_du_13-08-2018 (1) (2)output-1-to-1.json")