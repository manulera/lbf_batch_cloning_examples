"""PCR the L0 part out of each template, then Golden Gate it into the storage vector."""

import glob
import os

from Bio.Restriction import BbsI
from pydna.assembly2 import golden_gate_assembly, pcr_assembly
from pydna.opencloning_models import CloningStrategy
from pydna.parsers import parse
from pydna.primer import Primer

FWD = Primer("ttggtggaagactaTATGgctaggagtcgtctggtg", name="oRMLB007_L0_part_recovery_BbsI_F-RM")
RVS = Primer("cgataggaagaccaAAGActtcgcaaccacccgatag", name="oRMLB008_L0_part_recovery_BbsI_R-RM")



def read(path):
    """Parse a GenBank file, keeping only the file name (no folders) in the sequence source."""
    record = parse(path)[0]
    record.source.file_name = os.path.basename(path)
    return record


vector = read("sequences/pGCBA-Storage_v2_annotated.gb")
vector.name = "pGCBA-Storage_v2_annotated"

os.makedirs("project1/output", exist_ok=True)

for path in sorted(glob.glob("project1/input/sequences/*.gb")):
    template = read(path)
    template.name = os.path.basename(path).removesuffix(".gb")
    name = template.name.replace("pGGA-", "pGCBA_v2-")

    (pcr_product,) = pcr_assembly(template, FWD, RVS, limit=13)
    pcr_product.name = f"{name}_PCR"

    (product,) = golden_gate_assembly([pcr_product, vector], [BbsI], circular_only=True)
    product.name = name

    with open(f"project1/output/{name}.gb", "w") as f:
        f.write(product.format("genbank"))
    with open(f"project1/output/{name}.json", "w") as f:
        f.write(CloningStrategy.from_dseqrecords([product]).model_dump_json(indent=2))

    print(f"{name}: PCR {len(pcr_product)} bp -> plasmid {len(product)} bp")
