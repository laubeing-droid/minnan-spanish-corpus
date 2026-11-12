# Uso / 使用方法 (Español)

> [中文](USAGE.md) | [English](USAGE.en.md) | [Español](USAGE.es.md)
> Requisitos: Python ≥ 3.10, **sin dependencias de terceros** (solo biblioteca estándar).
> Ejecutar todos los comandos desde la raíz del repositorio.

---

## 1. Dónde están los datos

| Qué busca | Dónde |
| --- | --- |
| Zona congelada M1 del diccionario págs. 835–1140 (seis capas: desambiguación/fonología/Tâi-lô; véase nota en [DATA_SCHEMA.md](DATA_SCHEMA.md)) | `literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json` |
| Lecturas ciegas selladas página a página (págs. 0030–0834 y complemento en 0845–1140) | `literature/workspace_m2_dhs834/blind_read_pXXXX.json` |
| Manifiesto maestro de sellos SHA-256 | `literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json` |
| Cola de trabajo de cotejo filológico manual (ordenada por severidad) | `literature/workspace_m2_dhs834/COLLATION_QUEUE.json` |
| Registro de páginas no lexicográficas (portadas modernas, etc.) | `literature/workspace_m2_dhs834/non_lexicographic_pages.json` |
| Borradores base de las 22 fuentes | `literature/baseline_all22_extracted/body/` |

## 2. Verificar la integridad

```bash
python architect_gatekeeper.py
```

`[PASS] M1 ...` y `[PASS] M2 Gate: N blind-read pages verified` indican que se cumplen las condiciones de coherencia comprobadas por el verificador. No certifican las lecturas del manuscrito, los valores fonéticos históricos ni la calidad filológica de todo el corpus. El alcance y los límites de estas comprobaciones se explican en §3 de [METHODOLOGY.md](METHODOLOGY.md).

`architect_gatekeeper.py` está **declarado inmodificable** y también comprueba posibles fabricaciones. No se debe modificar para conseguir que los datos sean aceptados.

## 3. Progreso

```bash
python literature/tools/zcode_m2_pipeline.py status
```

## 4. Reconstruir teselas desde el PDF original

Las teselas escaneadas no se distribuyen (derechos), pero pueden **reconstruirse de forma
determinista** desde una copia legítima del PDF:

```bash
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849
# genera literature/tiles/01_DHS/page_XXXX/: 3 bandas horizontales + 4 columnas + página 300dpi
```

## 5. Protocolo de transcripción en tres pasos (páginas nuevas o reparadas)

1. `slice --start X --end Y`;
2. **Transcripción puramente visual**: escribir
   `literature/workspace_m2_dhs834/raw_blind/raw_part_pXXXX.json`, con la forma
   `{"pages":[{ ...solo esta página... }]}` y campos de página `pdf_page / historical_folio /
   page_header / page_footer_printed / page_footer_handwritten / entries`; cada entrada es
   `{position, source_L, source_H, source_M, source_R, tone_marks_M, tone_marks_R}`;
3. Sellar y pasar la puerta:

```bash
python literature/tools/zcode_m2_pipeline.py commit --input literature/workspace_m2_dhs834/raw_blind/<combinado>.json
python architect_gatekeeper.py
```

**Reglas de oro**: `source_M` solo admite grafía dominica del siglo XVII (c-/qu-/ch-/g-/s-/z-/ttz-);
prohibido k-/kh-/ts-/tsh-/chh- moderno. `tone_marks` solo admite
`T00 (無標號) / T01 (升斜) / T02 (降斜) / T03 (尖頂帽) / T04 (凹角) / T05 (平橫) /
T06/T07 (交叉入聲號) / T99 (污損難辨)`. Columna vacía `[空]`, ilegible `[残]`, dudoso `[疑:A/B]`.
**Prohibido escribir a mano `blind_read_pXXXX.json`** — los archivos sellados solo se generan
mediante el flujo de commit.

## 6. Uso de la cola de cotejo

`COLLATION_QUEUE.json` es una lista de páginas ordenada por severidad:

```json
{"page": 621, "can": 2, "yi": 3, "t99": 1, "estimated": true,
 "severity": "high", "notes": "..."}
```

* `can`/`yi`/`t99` = recuentos de `[残]`/`[疑:]`/T99 de la página; `estimated` = folio estimado o
  notas marcadas para revisión humana.
* Orden recomendado: `high` → `medium`; las entradas con `page ≥ 835` son páginas nuevas de
  relleno — léanse junto a sus vecinas.

## 7. Prohibiciones

* Modificar `architect_gatekeeper.py` (un verificador automodificado queda anulado);
* Escribir o editar directamente `blind_read_pXXXX.json` (solo se produce vía commit);
* Mezclar contabilidades entre líneas de obra (cada línea lleva su propia cuenta; jamás se suman);
* Escribir romanización moderna o fonética especulativa en `source_M`.

## 8. Preguntas frecuentes

* **¿Por qué no hay PDF/imágenes?** Derechos: el facsímil moderno pertenece a la editorial y a las
  bibliotecas. Las coordenadas del corpus son números de página del PDF; con una copia legítima
  puede reconstruir todas las teselas (§4).
* **¿Errores de codificación?** Todo el JSON es UTF-8 (`ensure_ascii=False`); leer con
  `encoding="utf-8"`.
* **¿Avisos CRLF?** Inofensivos (`core.autocrlf`); los sellos se calculan sobre los bytes
  confirmados de cada archivo `blind_read`.
