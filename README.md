# Golden Gate Batch cloning for London BioFoundry

Scripts to take a whole OpenCloning workspace, pull out every L0 template plasmid in it, and
re-clone the part of each one into the storage vector in a single batch.

## Project 1 - Batch-cloning L0 vectors

Every L0 template carries its part between the same pair of BbsI sites, so the same two primers
work on all of them. For each template the batch does two steps:

1. PCR the part out with `oRMLB007_L0_part_recovery_BbsI_F-RM` / `oRMLB008_L0_part_recovery_BbsI_R-RM`,
   which add BbsI sites to both ends of the product.
2. BbsI Golden Gate of that product into `pGCBA-Storage_v2_annotated`, keeping the circular assembly.

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

```bash
python clone.py
```

For every GenBank file in `project1/input/sequences/` this writes two files into `project1/output/`,
named after the template with `pGGA-` swapped for `pGCBA_v2-`:

* `<name>.gb` - the finished plasmid
* `<name>.json` - the OpenCloning cloning strategy, so the PCR and the assembly can be inspected
  or replayed in the web app

It also prints one line per plasmid with the PCR and plasmid sizes, which is the quickest way to
spot a template that amplified something unexpected.

### Step 4 - Upload them to the db

* Go to the sequences tab
* Click on `Upload sequences with history`
* Select all json files in `output`. Doing all at the same time might be a bit slow and it may freeze, so you can do some first, then others. But try all at once the first time.
* REMEMBER - if you want to tag them all as you upload them, you can do it on top of the window where it says "tags to apply".
* OpenCloning will create a single entry per unique plasmid and primer, so even though each json file contains a copy of the primers and the same backbone, only one entry will be created for the backbone and each primer.
