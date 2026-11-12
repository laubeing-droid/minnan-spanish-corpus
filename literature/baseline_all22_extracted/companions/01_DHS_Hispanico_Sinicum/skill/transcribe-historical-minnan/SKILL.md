---
name: transcribe-historical-minnan
description: Visually transcribe and collate historical Minnan manuscripts with Latin notation, Chinese text, or bilingual columns while preserving original forms and auditable page locations. Use for source-based transcription and collation, not modern pronunciation normalization.
---

# 历史闽南材料原形转写与校订

适用于原图转写、字段外校与跨本互参。当前方法经有限定点复验；不代表22份全文已核定。先读[验证范围](references/validation-scope.md)，需要处理具体符号时读[判断边界](references/decision-boundaries.md)。

## 先确定所做的是哪一层

- 独立首读：读者先看原图，冻结稿及hash后才接触答案。记录是否已见同条论文、旧稿或教学图；共享目录不等于强隔离。
- 已见答案/旧稿后的复核：直接标明，不回写为盲测。不同读者、图像分辨率或教学条件变化不能单独证明教学收益。
- 外校只对确切匹配的页、行、字段作判断；同词异实例或同义不同音节长度先保留差异。

## 原图与文字

用PDF物理页作稳定键，书内页码逐页观察；封面/空白/重复摄叶单列。原始扫描和现有渲染尺寸分别记录。全页预览缩小时取无插值局部，保留邻行和基线；放大低清不称增加源细节。

逐栏保留古音字母、调笔、汉字异体、西/葡原拼写、缩写和物理续行。先分字干、附加笔、删改、圈线、透背；疑字以页/栏/行或像素位置定位，必要时描述部件，不用现代音韵或熟悉文句填空。

g/c/q等先看小肚、基线下回环和同页同手参照；仅“有下伸”不足定字。缩写上横、上挑、上标先录原形；展开另列。Grammar的n/nn/c与基本符号组合不能压成DHS七调。账目和连续汉文没有该注音层时，不造调号分析。

## 保存和交付

冻结首稿保留；新校订另层逐条链接旧读、候选、图据及参考。正文只留原文、页定位和必要疑读；研究解释、实验条件、方法和脚本另存。覆盖数、hash一致、已看图、已核字段、全文核定分别报告。不要用文件完整性冒充识读准确率。

授权范围内新增文件；已有稿不覆盖。原件、审稿材料和发布有各自授权，技能本身不赋予上传、删除、安装或共享权限。现项目Pages发布暂停，交付更新须由协调者确认。

## 项目代码

本包code/tested_project_scripts仅为已跑过的项目脚本存档，依赖完整原目录；先读code/RUNNING.md。它们不执行OCR，不自动转写，也未验证为可直接迁移的命令行产品。
