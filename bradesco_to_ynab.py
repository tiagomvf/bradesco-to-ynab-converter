import csv
import os
from datetime import datetime

def convert_bradesco_to_ynab(input_path, output_path):
    # YNAB required columns
    ynab_header = ["Date", "Payee", "Category", "Memo", "Amount"]
    
    with open(input_path, 'r', encoding='latin-1') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile)
        writer.writerow(ynab_header)
        
        for row in reader:
            # Skip empty rows and header rows
            if len(row) < 4 or not row[0].strip() or '/' not in row[0]:
                continue
                
            # Extract relevant fields
            date_str, memo, _, amount_br = row[0].strip(), row[1].strip(), row[2], row[3].strip()
            
            # Skip summary rows
            if any(x in memo for x in ["Total", "Resumo", "Taxas", "Pagamento Mínimo", "SALDO ANTERIOR"]):
                continue
                
            try:
                # Convert date from DD/MM to MM/DD/YYYY with smart year detection
                day, month = map(int, date_str.split('/'))
                current_date = datetime.now()
                
                # Try current year first, then previous year if date is in future
                tentative_year = current_date.year
                if datetime(tentative_year, month, day) > current_date:
                    tentative_year -= 1
                
                date_obj = datetime(tentative_year, month, day)
                ynab_date = date_obj.strftime("%m/%d/%Y")
                
                # Convert amount from BR format (1.234,56) to YNAB format (1234.56)
                clean_amount = amount_br.replace('.', '').replace(',', '.')
                amount = float(clean_amount)
                
                # Determine outflow/inflow (Bradesco credits are negative)
                # Invert amount sign for YNAB compatibility
                ynab_amount = f"{-amount:.2f}"
                
                writer.writerow([
                    ynab_date,
                    "",  # Payee left blank
                    "",  # Category left empty for user to fill
                    memo,  # Original payee info goes to memo
                    ynab_amount
                ])
                
            except ValueError as e:
                print(f"Skipping invalid row: {row} - Error: {e}")

if __name__ == "__main__":
    input_dir = "input-files"
    
    # Process all CSV files in input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            # Ensure output directory exists
            output_dir = "output-files"
            os.makedirs(output_dir, exist_ok=True)
            
            input_csv = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_csv = os.path.join(output_dir, f"{base_name}_ynab_ready.csv")
            
            print(f"Processing: {filename}")
            convert_bradesco_to_ynab(input_csv, output_csv)
            print(f"Created YNAB file: {output_csv}\n")
