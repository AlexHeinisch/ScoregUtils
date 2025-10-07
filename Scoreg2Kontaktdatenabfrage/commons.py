from dataclasses import dataclass
import pandas as pd
from typing import List


def scoreg_excel_to_df(file_path: str) -> pd.DataFrame:
    df = pd.read_excel('./input_files/Scoreg_WRN.xlsx')
    return df

@dataclass
class MemberInfo():
    firstname: str
    lastname: str
    birthday: str
    email_1: str
    email_2: str
    handy: str
    festnetz: str
    plz: str
    city: str
    street: str
    state: str
    country: str
    contact_1_kind: str
    contact_1_name: str
    contact_1_email: str
    contact_1_phone: str
    contact_2_kind: str
    contact_2_name: str
    contact_2_email: str
    contact_2_phone: str

def _clean_birthday(value):
    """Format birthday values as YYYY-MM-DD without time."""
    if pd.isna(value) or value is None:
        return ""
    try:
        return pd.to_datetime(value).strftime("%Y-%m-%d")
    except Exception:
        return str(value)

def parse_df_to_member_info(df: pd.DataFrame) -> List[MemberInfo]:
    pages = []
    df = df.fillna('')
    df.sort_values(by='Nachname', ascending=True, inplace=True)
    for _, row in df.iterrows():
        pages.append(MemberInfo(
            firstname=row['Vorname'],
            lastname=row['Nachname'],
            birthday=_clean_birthday(row['Geburtsdatum']),
            email_1=row['E-Mail'],
            email_2=row['E-Mail2'],
            handy=row['Handy'],
            festnetz=row['Telefon'],
            plz=row['PLZ'],
            city=row['Stadt'],
            street=row['Strasse'],
            state=row['Bundesland'],
            country=row['Land'],
            contact_1_kind=row.get('Kontakt 1 Art'),
            contact_1_name=row['Kontakt 1'],
            contact_1_email=row.get('Kontakt 1 E-Mail'),
            contact_1_phone=row['Kontakt 1 Telefon'],
            contact_2_kind=row['Kontakt 2 Art'],
            contact_2_name=row['Kontakt 2'],
            contact_2_email=row['Kontakt 2 E-Mail'],
            contact_2_phone=row['Kontakt 2 Telefon']
        ))
    return pages


