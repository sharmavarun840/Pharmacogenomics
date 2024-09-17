import os
import pandas as pd

# Function to map genotypes to star alleles and metabolizer status
def map_star_alleles(row):
    # Initialize star allele and metabolizer status
    star_alleles = []
    metabolizer_status = ""

    # rs3918290 (DPYD*2A)
    if row['rs3918290'] == 'GG':
        star_alleles.append("*1")
    elif row['rs3918290'] == 'GA' or row['rs3918290'] == 'AG':
        star_alleles.append("*1/*2A")
        metabolizer_status = "Intermediate Metabolizer"
    elif row['rs3918290'] == 'AA':
        star_alleles.append("*2A/*2A")
        metabolizer_status = "Poor Metabolizer"
    else:
        star_alleles.append("--")

    # rs55886062.1 (DPYD*13)
    if row['rs55886062.1'] == 'TT':
        star_alleles.append("*1")
    elif row['rs55886062.1'] == 'TG' or row['rs55886062.1'] == 'GT':
        star_alleles.append("*1/*13")
        metabolizer_status = "Intermediate Metabolizer"
    elif row['rs55886062.1'] == 'GG':
        star_alleles.append("*13/*13")
        metabolizer_status = "Poor Metabolizer"
    else:
        star_alleles.append("--")

    # rs67376798 (DPYD*9A)
    if row['rs67376798'] == 'TT':
        star_alleles.append("*1")
    elif row['rs67376798'] == 'TC' or row['rs67376798'] == 'CT':
        star_alleles.append("*1/*9A")
        metabolizer_status = "Intermediate Metabolizer"
    elif row['rs67376798'] == 'CC':
        star_alleles.append("*9A/*9A")
        metabolizer_status = "Poor Metabolizer"
    else:
        star_alleles.append("--")

    # rs1801160 (DPYD*5)
    if row['rs1801160'] == 'GG':
        star_alleles.append("*1")
    elif row['rs1801160'] == 'AG' or row['rs1801160'] == 'GA':
        star_alleles.append("*1/*5")
        metabolizer_status = "Intermediate Metabolizer"
    elif row['rs1801160'] == 'AA':
        star_alleles.append("*5/*5")
        metabolizer_status = "Poor Metabolizer"
    else:
        star_alleles.append("--")

    # Determine overall metabolizer status if not set
    if not metabolizer_status:
        metabolizer_status = "Normal Metabolizer"

    # Return the star allele combination and metabolizer status
    return {'Star Alleles': ' '.join(star_alleles), 'Metabolizer Status': metabolizer_status}

# Function to find and process the Excel file in the current directory
def process_dpy_genotypes_in_directory():
    # Get the current working directory
    current_directory = os.getcwd()

    # Look for an Excel file in the current directory
    for file in os.listdir(current_directory):
        if file.endswith(".xlsx"):
            input_file = os.path.join(current_directory, file)
            output_file = os.path.join(current_directory, f"output_{file}")
            print(f"Processing file: {file}")

            # Load the Excel file
            df = pd.read_excel(input_file)

            # Apply the star allele mapping function
            df[['Star Alleles', 'Metabolizer Status']] = df.apply(map_star_alleles, axis=1, result_type='expand')

            # Save the results to an Excel file
            df.to_excel(output_file, index=False)
            print(f"Results saved to {output_file}")
            return

    print("No Excel file found in the current directory.")

# Example usage
if __name__ == "__main__":
    process_dpy_genotypes_in_directory()
