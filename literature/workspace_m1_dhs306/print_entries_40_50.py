from check_50 import found

for i, x in enumerate(found[39:], 40):
    print(f"{i}. {x['id']}: H='{x['source_H']}' | M='{x['source_M']}' | L='{x['source_L']}' | R='{x['source_R']}'")
