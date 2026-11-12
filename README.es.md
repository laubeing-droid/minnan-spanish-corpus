# minnan-spanish-corpus · Corpus de documentos históricos bilingües minnan–español

> El texto chino ([README.md](README.md)) es la versión canónica. Este repositorio constituye un corpus en proceso de construcción y cotejo: el sellado de ingeniería y la superación de la puerta automática (`[PASS]`) garantizan la integridad estructural, pero no equivalen a la validación filológica definitiva de todas las páginas. Las 22 fuentes corresponden a archivos PDF registrados (3.139 posiciones físicas de página en 9 líneas documentales), no a 22 obras independientes.

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

Este repositorio reúne borradores históricos, datos organizados por capas y registros sellados de lectura ciega de 22 PDF sobre el contacto temprano entre el hokkien y el español. Permite localizar materiales, comparar lecturas y continuar el cotejo. Los resultados proceden de etapas distintas y todavía no cuentan con una revisión filológica independiente de todo el conjunto.

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

La transcripción se distingue de la interpretación. El protocolo M2 (v3.1, `WITHOUT_PRIOR_DRAFT`) exige leer las imágenes sin consultar borradores anteriores. Los conocimientos fonológicos modernos no deben utilizarse para reescribir las grafías históricas. Se conservan también borradores elaborados con ayuda de referencias, sin presentarlos retrospectivamente como lecturas ciegas independientes.

En DHS, las cuatro columnas registran lemas españoles (`L`), caracteres chinos (`H`), grafías hokkien (`M`) y lecturas en mandarín (`R`). Las reconstrucciones fonológicas y las correspondencias modernas en Tâi-lô del MOE se guardan por separado. Una conversión determinista permite repetir el procedimiento, pero no demuestra por sí sola que la lectura o el valor fonético sean correctos. Este formato no se aplica automáticamente a todas las fuentes. El [esquema de datos](docs/DATA_SCHEMA.md) explica las seis capas (`layer_0` a `layer_5`).

Los hashes SHA-256 registran las páginas selladas (`LOCKED_BEFORE_COLLATION`). El archivo inmodificable `architect_gatekeeper.py` comprueba las condiciones de ortografía, códigos tonales (`T00–T07 / T99`) e integridad que implementa, incluidos los controles contra el uso de plantillas. Superarlos no sustituye el cotejo filológico. La [metodología](docs/METHODOLOGY.md) detalla el procedimiento y sus límites.

## 3. Importancia

Estos documentos permiten comparar caracteres y grafías tempranas del hokkien de base zhangzhou, así como estudiar la comunidad sangley de Manila, la traducción sino-hispánica y la impresión de textos católicos chinos. El *Beng Sim Po Cam* de Juan Cobo, por ejemplo, es la primera traducción conocida de un clásico chino a una lengua europea. Los diccionarios y documentos civiles registran otros contextos de uso lingüístico que deben estudiarse atendiendo a la historia y a los testimonios de cada obra.

El proyecto también explora cómo los métodos computacionales y generativos pueden ayudar a investigar la historia y filología del minnan. El trabajo incluye delimitar fuentes y preguntas, identificar fenómenos, comparar materiales, contrastar explicaciones y someter los resultados al juicio del investigador. La transcripción y el cotejo son la base, no el final de ese proceso. El documento de [importancia del proyecto](docs/SIGNIFICANCE.md) distingue los resultados existentes del método completo todavía en desarrollo; el [contexto histórico](docs/HISTORICAL_BACKGROUND.md) presenta el marco de las fuentes.

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

## 5. Cómo empezar

Para leer o citar materiales, consulte la [guía de uso](docs/USAGE.es.md) o la [guía para Agent](docs/AGENT_GUIDE.md); no hace falta ejecutar programas. Los comandos siguientes se dirigen a quienes mantienen el proyecto. El corte genera archivos locales y requiere acceso legítimo al PDF original y autorización para esa tarea.

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
