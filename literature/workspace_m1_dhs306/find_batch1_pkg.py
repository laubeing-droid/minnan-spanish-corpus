import json
import glob

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

print("Batch 1 package_path:", reg['batches'][1]['package_path'])
print("Files matching *0840* in dhs306:")
for f in glob.glob("literature/assets/dhs306/*0840*"):
    print(" ", f)
