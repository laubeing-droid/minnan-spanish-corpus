# 已实际使用的项目脚本

这5个脚本曾在原DHS项目运行，产物随本包记录。Python语法在本次打包再检查；没有声称跨平台或脱离项目运行通过。

- extract_native_visual_tiles_v1.py START END：现有PyMuPDF和Pillow；读取同项目source内PDF，单内嵌图限制，输出native_images原扫描及无插值分块。旧目标存在会排他失败；不要为重跑覆盖。新机器缺依赖时先按其权限处理，包不安装依赖。
- render_visual_pages_v1.py START END：原项目低清预览，仅作定位，不替代原像素。脚本原样保存；先查看实际输出位置和存在性。
- audit_body_coverage_v1.py：硬编码本次原项目绝对路径。只在该目录仍存在时直接运行；移机需新建配置化副本并重测，不能假装便携。输出新时间戳覆盖报告。
- audit_declared_artifacts_v1.py：以脚本上两级作项目根；需要230原批manifest及全部原文件，按path/sha等字段递归校验。包只有摘要，禁止在包目录运行并把空集当全书通过。
- index_recorded_pages_v1.py：同样依赖原项目manifest与早期页码侧车；读取已观察页码，不以固定偏移填补。

运行位置：把这里视作源代码存档。实际已验证位置是原项目/scripts；小包不复制7GB原图。要移机运行，先完整带入原项目依赖并逐条检查路径；任何改动另版再验。所有脚本只做材料化/映射/完整性工作，不自动识读。

证据：audit/coverage_snapshot_20261016T172548Z_v1.json、audit/all_declared_artifacts_audit_20261016T172640Z_v1.json、index/page_index_20261016T172548Z_v1.json及工作日志。原像素脚本的逐页manifest仍在原项目native_images。

未纳入：freeze_reader旧模板有140页元数据残留；freeze各版本是批特定实现；首版合并脚本只产生中间v1，最终v2另有人工检查过滤；图匹配流程候选分数不足独立定位。这些不作为本包已验证通用工具。
