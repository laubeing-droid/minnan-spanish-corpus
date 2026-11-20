#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐页导出 ADK 队列项与封存锚（只读），供读图裁决用。

用法: python literature/tools/dump_adk_items.py 283 284 285
输出: 每页一段——队列项（position/field/kind/v1/rr）+ 封存条目六字段锚。
不写任何正式数据。
"""
import json
import sys
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")


def main(pages):
    for pg in pages:
        pk = f"{pg:04d}"
        q = json.loads((M2 / f"collision_mr/adk/adk_p{pk}.json").read_text(encoding="utf-8"))
        seal = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        by_pos = {e["position"]: e for e in seal["entries"]}
        print(f"===== p{pk} | 队列 {len(q['items'])} 项 | 封存 {len(seal['entries'])} 条 =====")
        # 封存锚表（只列被任务涉及的 position，附行上下文）
        touched = sorted({it["position"] for it in q["items"] if isinstance(it.get("position"), int)})
        print("-- 锚（position: H | M | R | toneM | toneR）")
        for pos in touched:
            e = by_pos.get(pos)
            if not e:
                print(f"  pos {pos}: 封存缺此 position！")
                continue
            prev_h = by_pos.get(pos - 1, {}).get("source_H", "")
            print(f"  p{pos}: H={e.get('source_H','')!r} | M={e.get('source_M','')!r} | R={e.get('source_R','')!r}"
                  f" | tM={e.get('tone_marks_M', [])} | tR={e.get('tone_marks_R', [])} | 上行H={prev_h!r}")
        print("-- 任务（queueIndex: pos field kind | v1 | rr）")
        for idx, it in enumerate(q["items"], 1):
            print(f"  q{idx}: p{it.get('position')} {it.get('field')} {it.get('kind','')[:32]}"
                  f" | v1={it.get('v1','')!r} | rr={it.get('rr','')!r}")


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
