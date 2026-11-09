"""
verify_setup.py — Verifica que el entorno de desarrollo está correctamente configurado.

Ejecutar con: python verify_setup.py
Debe mostrar ✅ en cada componente.
"""

import sys
import importlib
import subprocess
import os


def check(name: str, condition: bool, fix: str = ""):
    if condition:
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ {name}")
        if fix:
            print(f"     → {fix}")
    return condition


def main():
    print("\n🔍 Verificando entorno de RiskMind AI...\n")
    all_ok = True

    # --- Python version ---
    print("📌 Python:")
    py_version = sys.version_info
    all_ok &= check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 10),
        "Se necesita Python 3.10+. Descargar de https://python.org",
    )

    # --- Virtual environment ---
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    all_ok &= check(
        "Entorno virtual activo",
        in_venv,
        "Activar con: source venv/bin/activate (macOS) o venv\\Scripts\\activate (Windows)",
    )

    # --- Core packages ---
    print("\n📦 Dependencias core:")
    packages = {
        "langchain": "pip install langchain==0.3.7",
        "langchain_community": "pip install langchain-community==0.3.7",
        "langchain_chroma": "pip install langchain-chroma==0.2.2",
        "chromadb": "pip install chromadb==0.5.23",
        "sentence_transformers": "pip install sentence-transformers==3.3.1",
        "pypdf": "pip install pypdf==5.1.0",
        "fastapi": "pip install fastapi==0.115.6",
        "uvicorn": "pip install uvicorn[standard]==0.34.0",
        "ragas": "pip install ragas==0.2.8",
        "dotenv": "pip install python-dotenv==1.0.1",
    }

    for pkg, fix in packages.items():
        try:
            mod = importlib.import_module(pkg)
            version = getattr(mod, "__version__", "ok")
            all_ok &= check(f"{pkg} ({version})", True)
        except ImportError:
            all_ok &= check(pkg, False, fix)

    # --- Embeddings model test ---
    print("\n🧠 Modelo de embeddings:")
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode(["test"])
        all_ok &= check(
            f"all-MiniLM-L6-v2 cargado ({embedding.shape[1]} dimensiones)",
            embedding.shape[1] == 384,
        )
    except Exception as e:
        all_ok &= check(
            "all-MiniLM-L6-v2",
            False,
            f"Error: {e}",
        )

    # --- ChromaDB test ---
    print("\n🗄️  ChromaDB:")
    try:
        import chromadb

        client = chromadb.Client()
        collection = client.get_or_create_collection("test_setup")
        collection.add(
            documents=["test document"],
            ids=["test_1"],
            metadatas=[{"tenant_id": "test"}],
        )
        results = collection.query(query_texts=["test"], n_results=1)
        client.delete_collection("test_setup")
        all_ok &= check("ChromaDB funcional (crear, insertar, buscar, borrar)", True)
    except Exception as e:
        all_ok &= check("ChromaDB", False, f"Error: {e}")

    # --- Ollama ---
    print("\n🤖 Ollama (LLM local):")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            has_llama = "llama3.1:8b" in result.stdout.lower() or "llama3.1" in result.stdout.lower()
            all_ok &= check("Ollama instalado", True)
            all_ok &= check(
                "Modelo llama3.1:8b descargado",
                has_llama,
                "Ejecutar: ollama pull llama3.1:8b",
            )
        else:
            all_ok &= check(
                "Ollama",
                False,
                "Instalar desde https://ollama.com/download",
            )
    except FileNotFoundError:
        all_ok &= check(
            "Ollama instalado",
            False,
            "Instalar desde https://ollama.com/download",
        )
    except subprocess.TimeoutExpired:
        all_ok &= check("Ollama", False, "Timeout al verificar Ollama")

    # --- .env file ---
    print("\n⚙️  Configuración:")
    env_exists = os.path.exists(".env")
    all_ok &= check(
        "Archivo .env presente",
        env_exists,
        "Copiar: cp .env.example .env (macOS) o copy .env.example .env (Windows)",
    )

    # --- Git ---
    print("\n🔀 Git:")
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        all_ok &= check(f"Git instalado ({result.stdout.strip()})", result.returncode == 0)
    except FileNotFoundError:
        all_ok &= check("Git", False, "Instalar desde https://git-scm.com")

    # --- Summary ---
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 ¡Todo listo! El entorno está correctamente configurado.")
        print("   Siguiente paso: implementar la ingesta (loader.py + chunker.py)")
    else:
        print("⚠️  Hay componentes por configurar. Revisa los ❌ arriba.")
    print()

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
