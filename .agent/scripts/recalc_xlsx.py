from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def find_soffice() -> str:
    candidates = [
        shutil.which("soffice"),
        shutil.which("soffice.com"),
        shutil.which("soffice.exe"),
        r"C:\Program Files\LibreOffice\program\soffice.com",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)

    raise FileNotFoundError(
        "LibreOffice não encontrado. Instale o LibreOffice ou adicione o caminho do soffice ao PATH."
    )


def recalc_xlsx(input_file: Path, out_dir: Path) -> Path:
    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_file}")

    out_dir.mkdir(parents=True, exist_ok=True)

    soffice = find_soffice()

    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nodefault",
        "--nolockcheck",
        "--nofirststartwizard",
        "--convert-to",
        "xlsx",
        "--outdir",
        str(out_dir),
        str(input_file),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Falha ao recalcular/converter a planilha.\n"
            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )

    output_file = out_dir / input_file.name
    if not output_file.exists():
        raise RuntimeError(
            "O LibreOffice executou, mas o arquivo de saída não foi encontrado.\n"
            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )

    return output_file


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python .agent/scripts/recalc_xlsx.py <arquivo.xlsx> [diretorio_saida]")
        return 1

    input_file = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_file.parent

    try:
        output = recalc_xlsx(input_file, out_dir)
        print(f"OK: arquivo recalculado/salvo em: {output}")
        return 0
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
