from typing import List, cast
from commons import MemberInfo, parse_df_to_member_info, scoreg_excel_to_df
import pandas as pd
from enum import Enum
from dataclasses import dataclass
import argparse
import warnings
warnings.filterwarnings("ignore", message="Workbook contains no default style")

class Stufe(str, Enum):
    BIEBER = 'BI'
    WICHTEL = 'WI'
    WOELFLINGE = 'WOE'
    GUIDES = 'GU'
    SPAEHER = 'SP'
    CAVELIERS = 'CA'
    EXPLORERS = 'EX'
    RANGER = 'RA'
    ROVER = 'RO'

@dataclass
class ParsedArgs():
    stufen: List[Stufe]
    parents: bool
    input_file_path: str
    output_file_path: str

def parse_args() -> ParsedArgs:
    parser = argparse.ArgumentParser(
        prog='Scoreg2Contacts',
        description='Program to create a vcard file containing the contact information of either the members or the parents of members.'
    )
    parser.add_argument('-i', '--input-file', required=True)
    parser.add_argument('-o', '--output-file', required=True)
    parser.add_argument('-s', '--stufen', default="")
    parser.add_argument('-p', '--parents', action="store_true")
    args = parser.parse_args()
    stufen = []
    for s in str(args.stufen).split(","):
        if (s == ''):
            continue
        stufen.append(Stufe[s])
    return ParsedArgs(stufen=stufen, input_file_path=args.input_file, output_file_path=args.output_file, parents=args.parents)

def filter_by_stufen(df: pd.DataFrame, selected_stufen: List[Stufe]) -> pd.DataFrame:
    if (len(selected_stufen) == 0):
        return df
    return cast(pd.DataFrame, df[df['Stufe'].isin(selected_stufen)])

def create_single_vcard(fullname: str, phone: str | None, phone2: str | None, email: str | None) -> str:
    vcard = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{fullname}"
    ]

    if phone and phone.lower() != "nan":
        vcard.append(f"TEL;TYPE=CELL:{phone}")

    if phone2 and phone2.lower() != "nan":
        vcard.append(f"TEL;TYPE=HOME:{phone2}")

    if email and email.lower() != "nan":
        vcard.append(f"EMAIL;TYPE=INTERNET:{email}")

    vcard.append("END:VCARD")
    return "\n".join(vcard)


def create_parents_vcard(members: List[MemberInfo]) -> str:
    vcards = []

    for m in members:
        if m.contact_1_kind.lower() != "nan" and m.contact_1_name.lower() != "nan" and m.contact_1_phone.lower() != "nan":
            vcards.append(create_single_vcard(
                f"{m.contact_1_name} ({m.firstname} {m.lastname[0]})",
                m.contact_1_phone,
                None,
                m.contact_1_email
            ))
        if m.contact_2_kind.lower() != "nan" and m.contact_2_name.lower() != "nan" and m.contact_2_phone.lower() != "nan":
            vcards.append(create_single_vcard(
                f"{m.contact_2_name} ({m.firstname} {m.lastname[0]})",
                m.contact_2_phone,
                None,
                m.contact_2_email
            ))

    print(f"Created {len(vcards)} parent vcard entries out of {len(members)} members...")
    return "\n".join(vcards)

def create_member_vcard(members: List[MemberInfo]) -> str:
    vcards = []

    for m in members:
        if m.handy.lower() == "nan" and m.festnetz.lower() == "nan":
            print(f"No phone information given for {m.firstname} {m.lastname}, skipping...")
            continue
        vcards.append(create_single_vcard(
            f"{m.firstname} {m.lastname}",
            m.handy,
            m.festnetz,
            m.email_1
        ))


    print(f"Created {len(vcards)} member vcard entries out of {len(members)} members...")
    return "\n".join(vcards)


if __name__ == "__main__":
    # Example usage
    a = parse_args()
    df = scoreg_excel_to_df(a.input_file_path)
    fd = filter_by_stufen(df, a.stufen)
    members = parse_df_to_member_info(fd)
    output_payload = create_parents_vcard(members) if a.parents else create_member_vcard(members)

    with open(a.output_file_path, "w", encoding="utf-8") as f:
        f.write(output_payload)

