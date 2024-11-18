# s2s-cs
Create a CodeSystem json file from a tab separated csv file 
If given a writable fhir tx endpoint, the codesystem can be written to the server (POST)

Feel free to modify it for your own purposes.

### to install 
   * `virtualenv .venv`
   * `source env/bin/activate`
   * `pip install -r requirements.txt`

### to run 
    * `cd your-install-folder`
    * `source .venv/bin/activate`
    * `python main.py`