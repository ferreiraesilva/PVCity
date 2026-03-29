from __future__ import annotations

import unicodedata
from typing import Any


_PERIODICITY_ALIASES = {
    "sinal": "Sinal",
    "entrada": "Entrada",
    "mensais": "Mensais",
    "semestrais": "Semestrais",
    "unica": "Única",
    "permuta": "Permuta",
    "anuais": "Anuais",
    "veiculo": "Veículo",
    "financ. bancario": "Financ. Bancário",
    "financ. direto": "Financ. Direto",
}

_ADJUSTMENT_ALIASES = {
    "fixas irreajustaveis": "Fixas Irreajustaveis",
    "incc": "INCC",
    "igpm + 12% a.a": "IGPM + 12% a.a",
    "ipca + 0,99% a.m": "IPCA + 0,99% a.m",
    "ipca + 13,65% a.a": "IPCA + 13,65% a.a",
}

_MODIFICATION_ALIASES = {
    "nao": "Não",
    "decorado (r$/m2)": "Decorado (R$/m²)",
    "facility (r$/m2)": "Facility (R$/m²)",
}


def _ascii_key(value: Any) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_only.strip().lower().split())


def normalize_periodicity_label(value: Any) -> str | None:
    key = _ascii_key(value)
    if not key:
        return None
    return _PERIODICITY_ALIASES.get(key, str(value).strip())


def normalize_adjustment_label(value: Any) -> str | None:
    key = _ascii_key(value)
    if not key:
        return None
    return _ADJUSTMENT_ALIASES.get(key, str(value).strip())


def normalize_modification_kind(value: Any) -> str | None:
    key = _ascii_key(value)
    if not key:
        return None
    return _MODIFICATION_ALIASES.get(key, str(value).strip())


def normalize_yes_no_label(value: Any) -> str | None:
    key = _ascii_key(value)
    if not key:
        return None
    if key == "sim":
        return "Sim"
    if key in {"nao", "não"}:
        return "Não"
    return str(value).strip()


def is_financing_periodicity(value: Any) -> bool:
    normalized = normalize_periodicity_label(value)
    return normalized in {"Financ. Bancário", "Financ. Direto"}
