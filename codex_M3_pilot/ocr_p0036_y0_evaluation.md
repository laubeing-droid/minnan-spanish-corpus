# p0036 横带本机 OCR 小样

输入为 `literature/tiles/01_DHS/page_0036/pdf_0036_band_y0_top.png`；使用 `D:\系统\法律文书处理` 的本地 GPU OCR，模型为已缓存的 PP-OCRv5 mobile 检测与识别模型，输出到系统临时目录。没有修改原图或源 PDF。

结果可粗略提示部分西语词形，但有错认、漏词和漏调号。例如其中一行 OCR 给出 `Abertuva clatabla pang`，原图西语段看起来包含 `Abertura de la tabla`，末尾音写有图上调号；两者均须回原图复核，不能将 OCR 输出直接写入字面层。此单张试验不足以推断全书效果，也不能作为人工真值或独立校准通过证明。
