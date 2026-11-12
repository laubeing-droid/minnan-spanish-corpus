from check_50 import found
import json

for i, x in enumerate(found):
    print(f"{i+1:02d}. {x['id']} (p{x['page']}:{x['pos']}) | H: {x['source_H']} | M: {x['source_M']} | L: {x['source_L']} | ZH: {x['queue_zh']} | EN: {x['queue_en']}")
