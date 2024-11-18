import argparse
import os
import helpers

def ensure_directories_exist(path):
    try:
        os.makedirs(path, exist_ok=True)  # Creates all intermediate-level directories if needed
        print(f"Directories created or already exist: {path}")
    except Exception as e:
        print(f"Error creating directories: {e}")

## Setup folders
homedir=os.environ['HOME']
rootdir=os.path.join(homedir,"data","salocal")
outdir=os.path.join(rootdir,"out")
indir=os.path.join(rootdir,"in")
infile=os.path.join(indir,"LocalSpecimens.txt")
endpoint = 'http://localhost:8080/fhir'
ensure_directories_exist(indir)
ensure_directories_exist(outdir)
template_file=os.path.join('.','templates','codesystem.json')
## Process args
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--outdir", help="output dir for processed file", default=outdir)
parser.add_argument("-t", "--template", help="output dir for processed file", default=template_file)
parser.add_argument("-i", "--infile", help="TSV Codesystem file with local codesystem", default=infile)
# Change this to the server endpoint when ready to publish
parser.add_argument("-p", "--publish", help="FHIR Endpoint to publish CodeSystem or None",default=endpoint)
args = parser.parse_args()
## Post processed file will keep the same name but be in the outdir folder.
status = helpers.build_code_system(args.infile,args.template,args.outdir,args.publish)
print(f"Completed with status: {status}")
