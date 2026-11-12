# minnan-spanish-corpus · Corpus de documentos históricos bilingües minnan–español

> update pending — The Chinese README is canonical. This is a work-in-progress corpus; full linguistic acceptance and complete blind-read coverage are not established by this documentation review. The 22 sources count PDFs, not 22 independent books.

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

> **22 documentos históricos bilingües minnan–español** dejados por la misión dominica y la
> comunidad sangley (china) de Manila del siglo XVII: transcripciones completas de lectura
> ciega, derivaciones fonológicas históricas y datos de corpus listos para cotejo, producidos
> con un flujo de ingeniería reproducible.

**Documentación**: [Metodología](docs/METHODOLOGY.md) · [Importancia](docs/SIGNIFICANCE.md) · [Historia del proyecto](docs/PROJECT_HISTORY.md) · [Uso](docs/USAGE.es.md) · [Registro de cambios](CHANGELOG.md)

---

## 1. Objeto de estudio

Hacia 1590–1700, los dominicos de Manila registraron en grafía castellana el dialecto de
Zhangzhou del minnan (hokkien) para evangelizar a los sangleyes, dejando diccionarios,
gramáticas, catecismos, traducciones y documentos laicos. Este proyecto conserva en forma de
corpus industrial los **22 originales supervivientes — 3.139 páginas físicas en 9 líneas de obra**:

| Línea | Obra | Signatura | Págs. |
| --- | --- | --- | ---: |
| 1 | *Dictionario Hispánico Sinicum* (diccionario español–chino) | Archivo UST, Manila | 1.140 |
| 2 | *Arte de la Lengua Chio Chiu* (gramática del zhangzhou) | UB Ms. 1027 | 122 |
| 3 | *Manuscritos chinos de Filipinas*, vols. 1–14 | HAB 91.2 Extrav 01–14 | 461 |
| 4 | *Beng Sim Po Cam* (Espejo del claro corazón), chino–español | BNE MSS/6040 | 315 |
| 5 | *Apología de la Verdadera Religión* (xilografía) | BNE R/33396 | 164 |
| 6 | Diccionario chino–español, copia de París | BnF Chinois 9276 | 178 |
| 7 | Diccionario chino–español, copia de Roma | Biblioteca Angelica Ms. 60 | 169 |
| 8 | *Xinkan Liaoshi Zhengjiao Bianlan* (catecismo) | ONB Sin 282-A | 580 |
| 9 | Fragmentos de catecismo y *Arte Sangley* de Zhangzhou | AUST Tomo 211 | 10 |

## 2. Método (resumen)

* **Protocolo de lectura ciega (v3.1)**: la transcripción sigue únicamente la imagen de la página;
  el conocimiento fonológico jamás "corrige" la escritura, de modo que el corpus es evidencia
  independiente del siglo XVII.
* **Aislamiento en seis capas**: las cuatro columnas del manuscrito (lema español L, caracteres
  chinos H, grafía hokkien del manuscrito M, glosa mandarín R) se copian literalmente; el IPA del
  zhangzhou del siglo XVII y el Tâi-lô moderno (MOE) se derivan con motores deterministas en capas separadas.
* **Sellado por hash a ciegas + puerta inmutable**: cada página se sella con SHA-256 al confirmarse;
  `architect_gatekeeper.py` (declarado inmodificable) verifica de forma independiente la pureza
  ortográfica, la validez de los códigos tonales y la integridad de los sellos, con reglas
  antiplantilla y antifalsificación. Detalles: **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**.

## 3. Importancia (resumen)

El corpus sincrónico carácter–sonido más antiguo y extenso del hokkien de Zhangzhou del siglo XVII;
material primario estructurado para la historia de la comunidad sangley de Manila, de la traducción
sino-occidental (incluida la primera traducción occidental conocida de un libro chino, el *Beng Sim
Po Cam*) y de la imprenta católica en chino; además, un paradigma de datos reproducibles para la
filología de manuscritos en peligro. Véase **[docs/SIGNIFICANCE.md](docs/SIGNIFICANCE.md)**.

## 4. Mapa del repositorio

| Ruta | Contenido |
| --- | --- |
| `literature/workspace_m1_dhs306/` | Corpus sellado de las págs. 835–1140 del diccionario (maestro de 5.762 entradas + 14 paquetes) |
| `literature/workspace_m2_dhs834/` | Páginas selladas de las págs. 0030–0834, manifiesto SHA-256, registro de páginas no lexicográficas, cola de cotejo |
| `literature/baseline_all22_extracted/` | Borradores base de las 22 fuentes (732 archivos markdown) |
| `literature/historical_dhs/` · `ledgers/` | Cuerpo completo del borrador del diccionario; registros de glifos pendientes |
| `literature/tools/` | Motores deterministas: corte de teselas, saneamiento y fonología del XVII, expansión de abreviaturas, sellado |
| `architect_gatekeeper.py` | Puerta de aceptación inmutable |
| `.zcode/workflow-drafts/` | Protocolos de construcción de la lectura ciega (guiones de flujo) |
| `literature/source22_actual_mapping.json` etc. | Inventario de fuentes, verificaciones de integridad, manifiestos de traslado, metadatos |

> Los PDF originales y las teselas escaneadas **no** están en este repositorio (derechos);
> las coordenadas del corpus se refieren a números de página del PDF.

## 5. Inicio rápido

```bash
python architect_gatekeeper.py                              # verificar integridad de todos los datos sellados
python literature/tools/zcode_m2_pipeline.py status         # progreso de la línea del diccionario
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # reconstruir teselas desde el PDF
```

Esquemas, protocolo de transcripción en tres pasos y cola de cotejo:
**[docs/USAGE.md](docs/USAGE.md)** ([English](docs/USAGE.en.md) / [中文](docs/USAGE.es.md) — versión china y este texto).

## 6. Estado

Trabajo en curso: el sellado por lectura ciega cubre toda la línea del diccionario; el proyecto está
en la etapa de **cotejo manual**. Progreso detallado e incidencias: **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)**;
historial de versiones: **[CHANGELOG.md](CHANGELOG.md)**.

## 7. Derechos y licencia

* Corpus, código y documentos: **[CC BY-NC-SA 4.0](LICENSE)** — atribución, **no comercial**, compartir igual.
* Las ediciones facsímiles/fotográficas modernas siguen perteneciendo a sus bibliotecas y editoriales
  (facsímil del diccionario © National Tsing Hua University Press) y no se redistribuyen aquí;
  los manuscritos del siglo XVII están en dominio público.

## 8. Cómo citar

```bibtex
@misc{minnan_spanish_corpus_2026,
  title  = {minnan-spanish-corpus: corpus de lectura ciega y herramientas para 22 documentos históricos bilingües minnan--español},
  author = {Minnan Historical Documents Working Group},
  year   = {2026},
  url    = {https://github.com/laubeing-droid/minnan-spanish-corpus},
  note   = {CC BY-NC-SA 4.0; escaneos originales excluidos por derechos}
}
```
