# 本地历史手写 OCR 可行性（候选，不是校准或裁决）

2026-11-18。仅使用一张原始横带 `literature/tiles/01_DHS/page_0523/pdf_0523_band_y0_top.png` 做视觉及离线识别；未读取既有转写、盲读、重读或裁决作为提示，未请求付费供应商，未修改 raw、封存或释义。原图 SHA-256：`16ec0e0581599d7830ae0fb090973d521416e69e40ca7722d2ba8d28469cf644`。

## 当前可复用环境

- `D:/系统/法律文书处理` 的专用解释器 `%LOCALAPPDATA%/LegalDocMarkdown/.venv/Scripts/python.exe` 已有 PaddleOCR 3.7.0、Paddle GPU 3.3.0；本机 NVIDIA RTX 3050 Laptop，显存 4,096 MiB。`PP-OCRv6_medium_det` 与 `PP-OCRv6_medium_rec` 权重已在 `%USERPROFILE%/.paddlex/official_models/`。该环境没有 Kraken、PyTorch 或 Transformers。
- 系统 Python 3.12 中有 Transformers，但未发现 PyTorch、Kraken 或现成古手写识别模型；不能仅凭 Transformers 存在即判断该模型可运行。
- Windows 显示已注册 Ubuntu WSL 2，原状态为 Stopped；顺序执行 `wsl -d Ubuntu -- uname -a` 返回“灾难性故障 / Wsl/Service/E_UNEXPECTED”，因此无法确认 Ubuntu 内依赖或使用 Linux Kraken。未修改、安装或修复系统环境。
- 用户代理 `127.0.0.1:20808` 端口可达；通过代理请求 GitHub API 20 秒超时，Zenodo 官方归档的 HEAD 请求返回 200、`Content-Length: 29879539`。这只证明该文件在本次请求可达，未下载模型。

## 已运行的一图试验

在本地 GPU 0、离线模式加载现有 PP-OCRv6 medium 检测和识别模型，关闭整页方向、图像去畸变与行方向分类；从初始化到识别约 **7.3 秒**，输出 28 个检测框。结构化识别原文、分数与原图像素坐标保存在 `codex_local_htr_p0523_candidate.json`，状态为 `OCR_CANDIDATE_ONLY_NOT_TRUTH`。输出只是一张横带，不可推算全书准确率或任务费用。

目视对照原图可以看到显著限制：原图 M 栏两处手写行上方有斜笔和横笔，识别框 `[1199,904,1472,1029]` 输出 `chun chong`，未保留这些上方记号；另一包含连写的框 `[1208,799,1435,909]` 输出 `chin `、模型分数 0.803，仍漏失笔画或词段。个别检测框输出 `2`，与相邻汉字或残迹的对应关系须逐框核对。这些比对只记录看得见的差异，不判定该页正确转写，也不把模型分数当裁决置信度。它可提供定位、疑点和候选，**不可自动填回、不可替代 M0 或 H 栏校准**。

第一次直接从 Python 加载模型时提示 `Could not locate cublasLt64_13.dll` 并退出；改为先调用项目现有的 `legal_doc_md.gpu.register_bundled_cuda_dlls()` 后原环境 GPU 推理成功。没有改变系统 PATH 的持久配置，也没有修改 OCR 工程。

## 开源专用模型线索

[HTR-UVA/eScriptorium 官方仓库](https://github.com/HTR-UVA/eScriptorium)列出 `MSS_HSMS_v1.mlmodel`，用途为卡斯蒂利亚语手写体，仓库声明项目与模型采用 CC BY 4.0，要求注明来源；它按 HSMS 半古文字规范处理缩写与上置字母，**不能默认等同于本项目的逐笔字面口径**。[Zenodo 归档 v1.0.1](https://zenodo.org/records/20506257)包含两种模型的 ZIP，页面显示 29.9 MB、本次 HEAD 为 29,879,539 字节。仅知整个归档大小，尚未确认 MSS 单个文件大小。未下载或执行模型，也未在仓库提交权重；本机 WSL 未能启动、Windows 环境缺少 Kraken/PyTorch，因此现阶段不能声称该模型可用或对本书有效。

## 重跑一图的命令

只在已存在上述专用环境及模型时运行，输出写系统临时目录；按用户要求不得先读已有转写来调整输出。初次执行加载模型可能另有启动耗时。

```powershell
$env:PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK = 'True'
$env:HF_HUB_OFFLINE = '1'
@'
from pathlib import Path
from legal_doc_md.gpu import register_bundled_cuda_dlls
register_bundled_cuda_dlls()
from paddleocr import PaddleOCR
import tempfile
models = Path.home()/'.paddlex'/'official_models'
ocr = PaddleOCR(
    text_detection_model_name='PP-OCRv6_medium_det',
    text_detection_model_dir=str(models/'PP-OCRv6_medium_det'),
    text_recognition_model_name='PP-OCRv6_medium_rec',
    text_recognition_model_dir=str(models/'PP-OCRv6_medium_rec'),
    use_doc_orientation_classify=False, use_doc_unwarping=False,
    use_textline_orientation=False, device='gpu:0')
for result in ocr.predict('literature/tiles/01_DHS/page_0523/pdf_0523_band_y0_top.png'):
    result.save_to_json(str(Path(tempfile.gettempdir())/'codex_htr_p0523_v6'))
'@ | & "$env:LOCALAPPDATA/LegalDocMarkdown/.venv/Scripts/python.exe" -X utf8 -
```
