import pandas as pd

def load_clean_export(file_path, output_path):
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    # Drop rows where 'content' is null
    df = df.dropna(subset=['content'])
    
    # Ensure 'time' is string before converting
    df['time'] = df['time'].astype(str)

    # Convert 'time' column to datetime (invalid times become NaT)
    df['time'] = pd.to_datetime(df['time'], errors='coerce')

    # Remove timezone info (if needed)
    if pd.api.types.is_datetime64tz_dtype(df['time']):
        df['time'] = df['time'].dt.tz_localize(None)

    # Sort: first valid times (newest first), then NaT at the bottom
    df = df.sort_values(by='time', ascending=False, na_position='last')

    # Export cleaned and sorted DataFrame to a new Excel file
    df.to_excel(output_path, index=False)

    print(f"✅ Cleaned and sorted data saved to {output_path}")

# Example usage:
load_clean_export('data.xlsx', 'cleaned_data.xlsx')
