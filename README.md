# RiskMind AI

Plataforma de cumplimiento legal GRC impulsada por IA mediante arquitectura RAG.

**Proyecto de Título** — Ingeniería Civil en Computación e Informática, Universidad Mayor.

**Autores:** Sebastián Palma · Ignacio Flores

---

## Requisitos previos

| Herramienta | Versión mínima | Para qué |
|---|---|---|
| Python | 3.12 (no 3.13 ni 3.14) | Backend, pipeline RAG |
| Git | 2.30+ | Control de versiones |
| Node.js | 18+ | Frontend React (Semana 2) |
| Ollama | latest | LLM local gratuito para desarrollo |

---

## Setup inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/riskmind-ai.git
cd riskmind-ai
```

### 2. Crear entorno virtual de Python

**macOS (Sebastián — MacBook Air M3):**

```bash
python3.12 -m venv venv
source venv/bin/activate
```

> Verificar que estás en el venv: el prompt debe mostrar `(venv)` al inicio.

**Windows (Ignacio):**

```powershell
py -3.12 -m venv venv
venv\Scripts\activate
```

> Si da error de permisos en PowerShell, ejecutar primero:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. Instalar dependencias

**macOS / Linux:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.lock
python -m pip install "numpy>=2.0" --no-deps
```

**Windows:**
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-windows.lock
python -m pip install "numpy>=2.0" --no-deps
```

> **Windows requiere Microsoft C++ Build Tools** antes de instalar.
> Descargar de https://visualstudio.microsoft.com/visual-cpp-build-tools/,
> marcar "Desarrollo de escritorio con C++", instalar y reiniciar el PC.

> El paso de `numpy>=2.0 --no-deps` es necesario porque LangChain declara
> `numpy<2.0` pero pyarrow (dependencia de RAGAS) requiere `numpy>=2.0`.
> En la práctica LangChain funciona correctamente con numpy 2.x.
### 4. Configurar variables de entorno

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Editar `.env` con los valores reales (las claves de API se agregan en Semana 3 para evaluación).

### 5. Instalar Ollama (LLM local gratuito)

**macOS:**
```bash
# Descargar desde https://ollama.com/download
# O con Homebrew:
brew install ollama
```

**Windows:**
```
Descargar el instalador desde https://ollama.com/download
Ejecutar e instalar.
```

**Ambos — descargar el modelo:**
```bash
ollama pull llama3.1:8b
```

> Esto descarga ~4.7 GB. Hacerlo con buena conexión.
> Para verificar: `ollama run llama3.1:8b "Hola, ¿funcionas?"` — debe responder.

### 6. Verificar la instalación

```bash
python verify_setup.py
```

Debe mostrar ✅ en cada componente. Si algo falla, el script indica cómo resolverlo.

---

## Estructura del proyecto

```
riskmind-ai/
├── backend/
│ ├── ingestion/ # Carga y chunking de PDFs
│ │ ├── init.py
│ │ ├── loader.py # Carga el PDF (Sebastián)
│ │ └── chunker.py # Divide en fragmentos (Sebastián)
│ ├── retrieval/ # Búsqueda semántica
│ │ ├── init.py
│ │ └── retriever.py # Busca chunks relevantes (Sebastián)
│ ├── generation/ # Cadena de generación
│ │ ├── init.py
│ │ ├── chain.py # Cadena LangChain (Ignacio)
│ │ └── prompts.py # Templates de prompts (Ignacio)
│ ├── scoring/ # Cálculo de scores
│ │ ├── init.py
│ │ ├── compliance.py # Score de cumplimiento (Ignacio)
│ │ └── risk.py # Score de riesgo (Ignacio)
│ ├── api/ # Endpoints FastAPI
│ │ ├── init.py
│ │ └── main.py # Rutas de la API (Compartido)
│ ├── evaluation/ # Scripts de evaluación
│ │ ├── init.py
│ │ ├── gold_standard.json
│ │ ├── run_ragas.py # Métricas RAGAS (Ignacio)
│ │ └── run_benchmark.py # Benchmark LLM (Ignacio)
│ └── data/ # Corpus normativo (PDFs, no versionados)
├── frontend/ # React con TypeScript (Semana 2)
├── docs/
│ └── DECISIONES.md # Registro de decisiones técnicas
├── .env.example # Template de variables de entorno
├── .gitignore
├── requirements.txt # Dependencias con versiones base
├── requirements.lock # Versiones exactas verificadas (usar este para instalar)
├── verify_setup.py # Script de verificación de instalación
└── README.md
```

---
---

## Corpus normativo y evidencia

La carpeta `backend/data/` no se versiona (los PDFs están en `.gitignore`).
Antes de ejecutar el pipeline, colocar ahí los siguientes archivos:

| Archivo | Fuente | Propósito |
|---------|--------|-----------|
| `ley_21663.pdf` | [BCN - Ley 21.663](https://www.bcn.cl/leychile/navegar?i=1202434) | Normativa principal para la base vectorial |
| `evidencia_1_techcorp_spa.pdf` | Generado (sintético) | Empresa simulada — buen cumplimiento |
| `evidencia_2_medipyme_ltda.pdf` | Generado (sintético) | Empresa simulada — cumplimiento parcial |
| `evidencia_3_logistica_regional_spa.pdf` | Generado (sintético) | Empresa simulada — bajo cumplimiento |

Los documentos de evidencia son sintéticos, diseñados con escenarios controlados
para permitir verificación determinista de los resultados del pipeline RAG.

## Flujo de trabajo con Git

```bash
# Nunca hacer push directo a main. Siempre crear una rama:
git checkout -b feat/nombre-descriptivo

# Trabajar, hacer commits descriptivos:
git add .
git commit -m "feat: implementar chunking con RecursiveCharacterTextSplitter"

# Subir la rama:
git push origin feat/nombre-descriptivo

# Crear Pull Request en GitHub. El otro revisa y aprueba.
```

### Convención de nombres de ramas

- `feat/ingesta` — nueva funcionalidad
- `fix/tabla-11-promedio` — corrección de bug
- `docs/cap7-diseno` — documentación
- `eval/benchmark-llm` — evaluación y métricas

---

## Cómo reproducir resultados

```bash
# 1. Clonar y configurar (pasos 1-5 de arriba)

# 2. Ejecutar ingesta del corpus normativo
python -m backend.ingestion.loader

# 3. Levantar la API
uvicorn backend.api.main:app --reload

# 4. Ejecutar evaluación RAGAS
python -m backend.evaluation.run_ragas

# 5. Ejecutar benchmark LLM
python -m backend.evaluation.run_benchmark
```

---

## Decisiones técnicas

Ver [docs/DECISIONES.md](docs/DECISIONES.md) para el registro completo de decisiones
con alternativas descartadas y justificación.
