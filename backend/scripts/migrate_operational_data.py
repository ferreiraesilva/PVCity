import sys
from pathlib import Path
from datetime import date, datetime

# Permite importar os módulos da app
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv()

from openpyxl import load_workbook
from sqlalchemy.orm import Session

from app.db.session import engine
from app.db.base import Base # Garante que todos os modelos estão carregados para create_all
from app.models.enterprise import Enterprise
from app.models.unit_standard_flow import UnitStandardFlow
from app.models.real_estate_agency import RealEstateAgency

WORKBOOK_SOURCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "projects-docs" / "references" / "source-of-truth"
)
FLOW_SHEET = "Tabela Venda - Parcela"
IMOBS_SHEET = "Imobs"

def _to_float(value, default=0.0):
    if value is None: return default
    try: return float(value)
    except: return default

def _to_int(value, default=0):
    if value is None: return default
    try: return int(float(value))
    except: return default

def extract_sheet_rows(wb, sheet_name):
    if sheet_name not in wb.sheetnames:
        return []
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows: return []
    headers = [str(h) if h is not None else "" for h in rows[0]]
    return [dict(zip(headers, row)) for row in rows[1:] if any(v is not None for v in row)]

def migrate():
    # Cria as tabelas caso não existam (homologação rápida)
    print("Sincronizando schema do banco...")
    Base.metadata.create_all(bind=engine)

    workbook_path = next(WORKBOOK_SOURCE_DIR.glob("*.xlsx"))
    print(f"Lendo Excel: {workbook_path.name}")
    wb = load_workbook(workbook_path, data_only=True, read_only=True)

    flow_rows = extract_sheet_rows(wb, FLOW_SHEET)
    imobs_rows = extract_sheet_rows(wb, IMOBS_SHEET)
    wb.close()

    print(f"  Linhas de fluxo lidas: {len(flow_rows)}")
    print(f"  Imobiliárias lidas: {len(imobs_rows)}")

    with Session(engine) as session:
        # --- Limpeza Prévia (Opcional, mas útil para re-rodar) ---
        # session.query(UnitStandardFlow).delete()
        # session.query(RealEstateAgency).delete()
        
        # --- Imobiliárias ---
        existing_imobs = {i.name for i in session.query(RealEstateAgency.name).all()}
        new_imobs = []
        for row in imobs_rows:
            name = row.get("Imobiliaria") or row.get("Nome") or row.get("Imobiliária") # Tenta nomes comuns
            if not name: continue
            name = str(name).strip()
            if name not in existing_imobs:
                new_imobs.append(RealEstateAgency(name=name, is_active=True))
                existing_imobs.add(name)

        if new_imobs:
            session.bulk_save_objects(new_imobs)
            print(f"  ✅ Imobiliárias inseridas: {len(new_imobs)}")

        # --- Fluxos Padrão ---
        enterprise_map = {e.name: e.id for e in session.query(Enterprise).all()}
        
        new_flows = []
        skipped_flows = 0
        
        # O Excel agrupa por 'Nome da Origem' (Empreendimento)
        # Vamos usar um contador para gerar o row_slot sequencial por empreendimento
        slots_counter = {}

        for row in flow_rows:
            ent_name = str(row.get("Nome da Origem") or "")
            ent_id = enterprise_map.get(ent_name)
            if not ent_id:
                skipped_flows += 1
                continue

            if ent_id not in slots_counter:
                slots_counter[ent_id] = 39 # Começa no slot 39 (padrão da UI)

            new_flows.append(UnitStandardFlow(
                enterprise_id=ent_id,
                periodicity=str(row.get("Parcela") or row.get("Frequencia") or ""),
                installment_count=_to_int(row.get("N° Parcelas"), 1),
                start_month=_to_int(row.get("Meses"), 0),
                installment_value=0.0, # Valor absoluto é 0 na tabela, pois é baseado em %
                percent=_to_float(row.get("Pcs")),
                row_slot=slots_counter[ent_id]
            ))
            slots_counter[ent_id] += 1

        if new_flows:
            # Remove fluxos antigos antes de inserir novos para evitar duplicidade na recarga
            all_affected_ents = list(slots_counter.keys())
            session.query(UnitStandardFlow).filter(UnitStandardFlow.enterprise_id.in_(all_affected_ents)).delete(synchronize_session=False)
            
            session.bulk_save_objects(new_flows)
            print(f"  ✅ Linhas de fluxo inseridas: {len(new_flows)}")
        
        session.commit()
        print(f"\n🚀 Migração operacional concluída!")

if __name__ == "__main__":
    migrate()
