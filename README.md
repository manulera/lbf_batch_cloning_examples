# Golden Gate Batch cloning for London BioFoundry

## Installing the dependencies

## Project 1 - Batch-cloning L0 vectors

### Step 0 - set up python env

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 1 - downloading an entire workspace

* Click on your user name on the top-right, go to Manage Workspace
* On that new window, click on "Export workspace". That will generate a single json file with all the sequences, strains etc. in it. Rename that file as workspace.json and put it in the folder `project1/input/`.

### Step 2 - extract all sequences labelled with the tag L0_version_1-Template

This is done with this script:

```bash
python get_sequences.py
```

It writes one GenBank file per tagged sequence into `project1/input/sequences/`.

### Step 3 - Do the same cloning for all the plasmids downloaded

### Step 4 - Upload them to the db

