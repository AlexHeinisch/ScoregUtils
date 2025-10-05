import pandas as pd

def create_vcards_from_xlsx(input_file: str, output_file: str):
    # Read Excel file
    df = pd.read_excel(input_file)

    vcards = []

    for _, row in df.iterrows():
        child_firstname = str(row.get("Vorname", "")).strip()
        child_lastname = str(row.get("Nachname", "")).strip()

        for i in [1, 2]:
            contact_type = str(row.get(f"Kontakt {i} Art", "")).strip()
            contact_name = str(row.get(f"Kontakt {i}", "")).strip()
            contact_phone = str(row.get(f"Kontakt {i} Telefon", "")).strip()
            contact_email = str(row.get(f"Kontakt {i} Email", "")).strip()

            if contact_type.lower() == "nan" or contact_name.lower() == "nan" or contact_phone.lower() == "nan":
                continue

            # Clean up type (remove (*) if present)
            primary = "(*)" in contact_type
            contact_type = contact_type.replace("(*)", "").strip()

            flag = " *" if primary else ""

            # Create full name (e.g., "Anna Müller (Mutter von Lisa Müller)")
            full_name = f"{contact_name}{flag} ({contact_type} von {child_firstname} {child_lastname})"

            vcard = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"FN:{full_name}",
                f"TEL;TYPE=CELL:{contact_phone}",
            ]

            if contact_email and contact_email.lower() != "nan":
                vcard.append(f"EMAIL;TYPE=INTERNET:{contact_email}")

            vcard.append("END:VCARD")
            vcards.append("\n".join(vcard))

    # Write to .vcf file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(vcards))


if __name__ == "__main__":
    # Example usage
    create_vcards_from_xlsx("input_files/test.xlsx", "contacts.vcf")

