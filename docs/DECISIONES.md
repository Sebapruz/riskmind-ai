# Registro de Decisiones Técnicas — RiskMind AI

Cada decisión técnica queda documentada aquí con fecha, alternativas descartadas y justificación.
Es material directo para Cap V (Desarrollo Técnico) y la defensa oral.

---

## 2026-11-09: Modelo de embeddings

- **Decisión:** `all-MiniLM-L6-v2` (sentence-transformers)
- **Alternativas descartadas:**
  - `text-embedding-3-small` (OpenAI): costo por token, dependencia de API externa
  - `e5-large-v2`: 1.3 GB, demasiado pesado para laptops de desarrollo
- **Razón:** gratuito, corre local, 384 dimensiones es suficiente para el corpus normativo del piloto
- **Responsable:** Sebastián

## 2026-11-09: Base de datos vectorial

- **Decisión:** ChromaDB con persistencia local
- **Alternativas descartadas:**
  - Pinecone: costo en producción
  - FAISS: sin persistencia nativa
- **Razón:** gratis, local, persistencia integrada, filtros por metadatos para multi-tenancy
- **Responsable:** Sebastián

## 2026-11-09: LLM para desarrollo

- **Decisión:** Ollama con Llama 3.1 8B (local)
- **Alternativas descartadas:**
  - APIs de pago directamente: costo innecesario durante desarrollo
- **Razón:** $0 de costo, iteración sin límite, suficiente para validar pipeline
- **Responsable:** Sebastián / Ignacio

## 2026-11-09: Normativa piloto

- **Decisión:** Ley 21.663 (Marco de Ciberseguridad)
- **Razón:** legislación chilena (diferencial), obligaciones concretas, disponible en bcn.cl
- **Responsable:** Sebastián / Ignacio

---

<!-- Agregar nuevas decisiones arriba de esta línea -->
