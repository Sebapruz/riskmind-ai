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

```bash
pip install --upgrade pip
pip install -r requirements.lock
```

> **Nota para Mac M3:** Si `chromadb` o `sentence-transformers` da error de compilación,
> instalar primero las herramientas de build:
> ```bash
> xcode-select --install  # si no lo tienes ya
> ```

> **Nota para Windows:** Si `sentence-transformers` da error con torch, instalar torch primero:
> ```powershell
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> pip install -r requirements.txt
> ```

> `requirements.lock` tiene las versiones exactas verificadas. Usar este archivo
> en vez de `requirements.txt` para evitar conflictos de resolución de dependencias.
> Después de instalar, ejecutar además:
> pip install "numpy>=2.0" --no-deps
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
│   ├── ingestion/        # Carga y chunking de PDFs
│   │   ├── loader.py     # Carga el PDF
│   │   └── chunker.py    # Divide en fragmentos
│   ├── retrieval/        # Búsqueda semántica
│   │   └── retriever.py  # Busca chunks relevantes
│   ├── generation/       # Cadena de generación
│   │   ├── chain.py      # Cadena LangChain
│   │   └── prompts.py    # Templates de prompts
│   ├── scoring/          # Cálculo de scores
│   │   ├── compliance.py # Score de cumplimiento
│   │   └── risk.py       # Score de riesgo
│   ├── api/              # Endpoints FastAPI
│   │   └── main.py       # Rutas de la API
│   ├── evaluation/       # Scripts de evaluación
│   │   ├── gold_standard.json
│   │   ├── run_ragas.py
│   │   └── run_benchmark.py
│   └── data/             # Corpus normativo (PDFs, no versionados)
├── frontend/             # React con TypeScript (Semana 2)
├── docs/
│   └── DECISIONES.md     # Registro de decisiones técnicas
├── .env.example          # Template de variables de entorno
├── .gitignore
├── requirements.txt
├── verify_setup.py       # Script de verificación de instalación
└── README.md
```

---

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
