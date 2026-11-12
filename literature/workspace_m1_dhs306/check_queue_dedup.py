import json
from collections import Counter

with open("literature/workspace_m1_dhs306/l_layer_gaps_queue.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data["queue_entries"]
print("Total raw entries in queue:", len(entries))

id_counts = Counter(e["id"] for e in entries)
duplicates = {k: v for k, v in id_counts.items() if v > 1}
print(f"Unique IDs: {len(id_counts)}")
print(f"IDs with multiple entries: {len(duplicates)}")
print("Sample duplicates:", list(duplicates.items())[:10])

# Check gap_type counts in all entries
gap_type_counts = Counter(e.get("gap_type") for e in entries)
print("Gap type counts (raw):", gap_type_counts)

# Let's inspect unique IDs and their gap types
unique_id_types = {}
for e in entries:
    eid = e["id"]
    gt = e.get("gap_type")
    if eid not in unique_id_types:
        unique_id_types[eid] = set()
    unique_id_types[eid].add(gt)

unique_type_dist = Counter(tuple(sorted(list(v))) for v in unique_id_types.values())
print("Unique ID type distribution:", unique_type_dist)
