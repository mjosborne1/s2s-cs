import pandas as pd
from collections import defaultdict
from pathlib import Path 
import os
import json
from fhirclient import client
from fhirclient.models import codesystem, fhirdate

    
## Create a smart client to the terminology server
def create_client(endpoint):
    settings = {
        'app_id': 's2s-cs',
        'api_base': endpoint
    }
    print(f'created smart client to {endpoint}')
    smart = client.FHIRClient(settings=settings)
    return smart

## Build a FHIR code system based on the Code\tDisplay rows in the TSV file
def build_code_system(infile,template,outdir,endpoint):    
    # Sample tab-separated data    
    with open(template) as f:
       meta = json.load(f)

    # Read the data into a pandas DataFrame    
    df = pd.read_csv(infile, sep='\t', dtype={'Code':str,'Display':str})

    # Remove duplicates
    uniq_df = df.drop_duplicates(subset=['Code'], keep='first')  

    # Create a smart fhir client if publication is happening now.
    smart = None
    if endpoint != None:
        smart = create_client(endpoint=endpoint)

    cs = codesystem.CodeSystem()
    cs.id = meta.get("id")
    cs.name = meta.get('name')
    cs.url = meta.get('url')
    cs.version = meta.get('version')
    cs.title = meta.get('title')
    cs.description = meta.get('description')
    cs.publisher = meta.get('publisher')
    cs.date = fhirdate.FHIRDate(meta.get('date'))
    cs.status = meta.get('status')
    cs.content = meta.get('content')
    cs.concept = []
    for index, row in uniq_df.iterrows():
        concept = codesystem.CodeSystemConcept()
        concept.code = row['Code']
        concept.display = row['Display']
        cs.concept.append(concept)

    # Set Outfile name
    path = Path(infile)
    outfile = os.path.join(outdir,f'{path.stem}_done.json')

    # save it to a new JSON file
    with open(outfile, "w") as f:
        json.dump(cs.as_json(), f, indent=2)
        print(f"Written CodeSystem to {outfile}")

    if smart != None:
        if cs.id:
            response = cs.update(smart.server)
        else:
            response = cs.create(smart.server)
        if response:
            return 201
        else:
            return 500
    else:
        print("INFO: Codesystem not uploaded to fhir server")
        return 200