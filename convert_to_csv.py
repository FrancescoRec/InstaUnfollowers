import os
from bs4 import BeautifulSoup
import csv

# Define data folder path
DATA_FOLDER = "data_of_instagram"

# Create data folder if it doesn't exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created data folder: {DATA_FOLDER}")

def parse_instagram_html(html_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get the header title to identify the type of data
    header_title = ""
    header = soup.select_one('h1')
    if header:
        header_title = header.text.strip()
    
    # Find all profile entries
    profile_entries = soup.select('div.pam._3-95._2ph-._a6-g.uiBoxWhite.noborder')
    
    data = []
    
    for entry in profile_entries:
        # Get username (from the link)
        username_link = entry.select_one('a')
        if not username_link:
            continue
            
        username = username_link.text.strip()
        profile_url = username_link.get('href', '')
        
        # Get date information
        date_div = entry.select_one('div._a6-p > div > div:nth-of-type(2)')
        date_info = date_div.text.strip() if date_div else ""
        
        data.append({
            'username': username,
            'profile_url': profile_url,
            'date_info': date_info
        })
    
    return header_title, data

def save_as_csv(data, output_file):
    if not data:
        print(f"No data to write to {output_file}")
        return
    
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'profile_url', 'date_info'])
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV data saved to {output_file}")

def main():
    # Check if HTML files exist in root directory first
    root_html_files = [
        'following.html',
        'followers_1.html'
    ]
    
    for html_file in root_html_files:
        if os.path.exists(html_file):
            # If file exists in root directory, copy it to data folder
            target_file = os.path.join(DATA_FOLDER, html_file)
            try:
                with open(html_file, 'r', encoding='utf-8') as src_file:
                    content = src_file.read()
                
                with open(target_file, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(content)
                
                print(f"Copied {html_file} to {target_file}")
            except Exception as e:
                print(f"Error copying {html_file}: {e}")
    
    # List of HTML files to process
    html_files = [
        'following.html',
        'followers_1.html'
    ]
    
    for html_file in html_files:
        # Create full paths
        input_file = os.path.join(DATA_FOLDER, html_file)
        
        if not os.path.exists(input_file):
            print(f"Warning: File '{input_file}' not found. Skipping.")
            continue
        
        # Get base name for output file
        base_name = os.path.splitext(html_file)[0]
        output_file = os.path.join(DATA_FOLDER, f"{base_name}.csv")
        
        # Parse data
        header_title, data = parse_instagram_html(input_file)
        
        # Print summary
        print(f"File: {input_file}")
        print(f"Type: {header_title}")
        print(f"Found {len(data)} profiles")
        
        # Save as CSV
        save_as_csv(data, output_file)
        print("-" * 50)

if __name__ == "__main__":
    main() 