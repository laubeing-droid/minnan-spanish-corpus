# minnan-spanish-corpus · Corpus de documentos históricos bilingües minnan–español

> El texto chino ([README.md](README.md)) es la versión canónica. Este repositorio constituye un corpus en proceso de construcción y cotejo: el sellado de ingeniería y la superación de la puerta automática (`[PASS]`) garantizan la integridad estructural, pero no equivalen a la validación filológica definitiva de todas las páginas. Las 22 fuentes corresponden a archivos PDF registrados (3.139 posiciones físicas de página en 9 líneas documentales), no a 22 obras independientes.

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

> **22 fuentes documentales históricas bilingües minnan–español** legadas por la misión dominica
> (Provincia del Santísimo Rosario) y la comunidad sangley (china de origen minnan) en la Manila de
> los siglos XVI y XVII: transcripciones diplomáticas de lectura ciega, derivaciones fonológicas
> históricas y datos estructurados listos para el cotejo filológico, producidos mediante un flujo de
> ingeniería reproducible y auditable.

**Documentación**: [Contexto histórico](docs/HISTORICAL_BACKGROUND.md) · [Metodología](docs/METHODOLOGY.md) · [Importancia](docs/SIGNIFICANCE.md) · [Esquema de datos](docs/DATA_SCHEMA.md) · [Historia del proyecto](docs/PROJECT_HISTORY.md) · [Lecciones de ingeniería](docs/LESSONS.md) · [Uso](docs/USAGE.es.md) · [Registro de cambios](CHANGELOG.md)

---

## 1. Objeto de estudio

Entre ca. 1590 y 1700, los misioneros dominicos en Manila —en estrecha colaboración con intérpretes
y escribas sangleyes— registraron en ortografía castellana del Siglo de Oro la lengua vernácula
minnan (hokkien) de base zhangzhou (*lengua Chio Chiu*), dejando diccionarios, gramáticas,
catecismos, tratados apologéticos, traducciones y documentos civiles. Este proyecto estructura los
**22 archivos PDF originales registrados — 3.139 páginas físicas agrupadas en 9 líneas de obra**:

| Línea | Obra | Signatura / Archivo | Págs. PDF |
| --- | --- | --- | ---: |
| 1 | *Dictionario Hispanico Sinicum* (diccionario español–chino/hokkien) | Archivo UST, Manila (Libros 215, 2 PDFs) | 1.140 |
| 2 | *Arte de la Lengua Chio Chiu* (gramática del dialecto de Zhangzhou, ca. 1620) | CRAI Univ. de Barcelona, Ms. 1027 | 122 |
| 3 | *Manuscritos chinos de Filipinas*, vols. 1–14 | HAB Wolfenbüttel, 91.2 Extrav. 01–14 | 461 |
| 4 | *Beng Sim Po Cam* (*Espejo rico del claro corazón*, trad. fray Juan Cobo, O.P.) | Biblioteca Nacional de España, MSS/6040 | 315 |
| 5 | *Apología de la verdadera religión* (*Shilu* 《無極天主正教真傳實錄》, xilografía, 1593) | Biblioteca Nacional de España, R/33396 | 164 |
| 6 | Diccionario chino–español, copia de París | Bibliothèque nationale de France, Chinois 9276 | 178 |
| 7 | Diccionario chino–español, copia de Roma | Biblioteca Angelica, Mss. Fondo Antico 60 | 169 |
| 8 | *Xinkan Liaoshi Zhengjiao Bianlan* (catecismo bilingüe) | Österreichische Nationalbibliothek, Sin 282-A | 580 |
| 9 | Fragmentos de catecismo y *Arte Sangley* de Zhangzhou | Archivo UST, Manila, Tomo 211 | 10 |

## 2. Método (resumen)

* **Protocolo de lectura ciega (v3.1, `WITHOUT_PRIOR_DRAFT`)**: la transcripción visual en la línea M2 sigue exclusivamente la imagen de la página sin consultar borradores previos; queda prohibido «corregir» la grafía manuscrita mediante conjeturas fonológicas o contaminarla con romanizaciones modernas (POJ / Tâi-lô).
* **Aislamiento en seis capas (`layer_0` a `layer_5`)**: las cuatro columnas diplomáticas del manuscrito (lema español `L`, caracteres chinos `H`, grafía hokkien misionera `M` y glosa en mandarín `R`) se transcriben literalmente; la reconstrucción fonológica (IPA del dialecto de Zhangzhou del siglo XVII) y el estándar moderno Tâi-lô (MOE) se calculan mediante motores deterministas en capas separadas.
* **Sellado de integridad SHA-256 + puerta de aceptación inmutable**: cada página de lectura ciega se sella con SHA-256 al confirmarse (`LOCKED_BEFORE_COLLATION`); `architect_gatekeeper.py` (declarado inmodificable) verifica de forma independiente la pureza ortográfica hispano-dominica, la validez de los ocho códigos tonales geométricos (`T00–T07 / T99`) y la ausencia de plantillas fabricadas. Véase **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)** (§7 en español).

## 3. Importancia (resumen)

Aporta un material fundamental de **correspondencia entre grafía sinográfica y transcripción fonética** para el hokkien de base zhangzhou del siglo XVII, así como fuentes primarias estructuradas para la historia social de la comunidad sangley del Parián de Manila, la historia de la traducción sino-hispánica (incluida la primera traducción conocida de un libro clásico chino a una lengua europea, el *Beng Sim Po Cam* de fray Juan Cobo) y la historia de los incunables filipinos impresos por Juan de Vera (Keng Yong). Más importante aún, tomando este fondo documental como banco de pruebas, el proyecto explora una **metodología integral de ingeniería de investigación para la «Historia y filología computacional y generativa del minnan»**: desde la convergencia de fuentes y materiales, la definición de problemas y restricciones probatorias, hasta la identificación de fenómenos históricos, el análisis comparativo, el contraste de hipótesis y el juicio crítico del historiador. **El corpus y el cotejo constituyen los cimientos, no la meta final; los resultados técnicos ya acumulados se distinguen rigurosamente del flujo completo de investigación en fase de exploración, sin equiparar jamás el sellado de ingeniería con una validación académica consumada.** Véanse **[docs/SIGNIFICANCE.md](docs/SIGNIFICANCE.md)** y **[docs/HISTORICAL_BACKGROUND.md](docs/HISTORICAL_BACKGROUND.md)**.

## 4. Mapa del repositorio

| Ruta | Contenido |
| --- | --- |
| `literature/workspace_m1_dhs306/` | Zona congelada de las págs. 835–1140 del diccionario (maestro de 5.762 entradas + 14 lotes de desambiguación; véase nota de alcance en [DATA_SCHEMA.md](docs/DATA_SCHEMA.md)) |
| `literature/workspace_m2_dhs834/` | Páginas selladas de lectura ciega (págs. 0030–0834 + lectura complementaria de 140 págs. en 0845–1140), manifiesto SHA-256, registro de páginas no lexicográficas y cola de cotejo |
| `literature/baseline_all22_extracted/` | Borradores base de las 22 fuentes (732 archivos Markdown de etapas previas) |
| `literature/evidence_ledger/` | Cuatro libros de registro separados (glifos no resueltos, fonología sin prueba, glosas inciertas y operaciones pendientes; véase [LEDGERS.md](docs/LEDGERS.md)) |
| `literature/tools/` | Motores deterministas: corte de teselas (`column_slicer.py`), saneamiento ortográfico y fonología del s. XVII (`hokkien_17c_converter.py`), expansión de abreviaturas (`spanish_17c_expander.py`) y flujo M2 (`zcode_m2_pipeline.py`) |
| `architect_gatekeeper.py` | Puerta de aceptación inmutable (verificador antifalsificación y antiplantilla) |
| `.zcode/workflow-drafts/` | Guiones de flujo de trabajo para la lectura ciega y auditoría |
| `literature/source22_actual_mapping.json` | Inventario de las 22 fuentes PDF, hashes SHA-256 de origen y metadatos de traslado |

> Los archivos PDF originales y las teselas de imagen escaneadas **no** se incluyen en este repositorio por derechos de edición; todas las coordenadas del corpus se refieren a los números de página del PDF original.

## 5. Inicio rápido

```bash
python architect_gatekeeper.py                              # verificar la integridad de todos los datos sellados
python literature/tools/zcode_m2_pipeline.py status         # consultar el progreso de la línea del diccionario
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # reconstruir teselas desde el PDF local
```

Esquemas de datos, protocolo de transcripción en tres pasos y uso de la cola de cotejo:
**[docs/USAGE.es.md](docs/USAGE.es.md)** ([中文](docs/USAGE.md) / [English](docs/USAGE.en.md)).

## 6. Estado actual

Completado el relleno de lagunas (2026-11-12): el sellado de lectura ciega cubre ya toda la línea del diccionario — págs. 0030–0834 (797 páginas lexicográficas / 15.417 entradas) más las 140 páginas de complemento de las págs. 0845–1140 (2.733 entradas), en total **937 páginas selladas / 18.150 entradas**; puerta final PASS; 8 páginas preliminares modernas excluidas por registro. El proyecto entra ahora en la etapa de **cotejo filológico manual** (cola: 884 páginas — 671 altas / 213 medias — véase `COLLATION_QUEUE.json`; otras 1.810 observaciones de defectos mecánicos se transfirieron a la línea de cotejo). Historial detallado e informe sobre la resolución del enigma de las 140 páginas: **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)** y **[docs/LESSONS.md](docs/LESSONS.md)**.

## 7. Derechos y licencia

* Transcripciones originales, código y documentación de este repositorio: **[CC BY-NC-SA 4.0](LICENSE)** — atribución, **uso no comercial**, compartir igual.
* Las ediciones facsímiles y fotográficas modernas pertenecen a sus respectivas bibliotecas custodias y editoriales (facsímil de la colección © National Tsing Hua University Press) y no se redistribuyen aquí; el texto de los manuscritos históricos del siglo XVII se encuentra en el dominio público.

## 8. Cómo citar

```bibtex
@misc{minnan_spanish_corpus_2026,
  title  = {minnan-spanish-corpus: corpus de lectura ciega y herramientas para 22 fuentes documentales históricas bilingües minnan--español},
  author = {Minnan Historical Documents Working Group},
  year   = {2026},
  url    = {https://github.com/laubeing-droid/minnan-spanish-corpus},
  note   = {CC BY-NC-SA 4.0; escaneos originales excluidos por derechos editoriales}
}
```
