import csv
import os
from datetime import datetime

# Define data folder path
DATA_FOLDER = "data_of_instagram"
REPORTS_FOLDER = "reports"

# Create reports folder if it doesn't exist
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)
    print(f"Created reports folder: {REPORTS_FOLDER}")

OUTPUT_FILE = os.path.join(REPORTS_FOLDER, f"instagram_report_{datetime.now().strftime('%Y-%m-%d')}.txt")

def load_usernames_from_csv(csv_file):
    """Load usernames from a CSV file into a set."""
    usernames = set()
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return usernames
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'username' in row:
                usernames.add(row['username'])
    
    return usernames

def write_report():
    # File paths
    following_csv = os.path.join(DATA_FOLDER, 'following.csv')
    followers_csv = os.path.join(DATA_FOLDER, 'followers_1.csv')
    
    # Load usernames from both files
    following = load_usernames_from_csv(following_csv)
    followers = load_usernames_from_csv(followers_csv)
    
    if not following:
        print("No following data found.")
        return
    
    if not followers:
        print("No followers data found.")
        return
    
    # Find users you're following who don't follow you back
    not_following_back = following - followers
    
    # Find users who follow you but you don't follow them
    you_dont_follow = followers - following
    
    # Find mutual connections
    mutual = following.intersection(followers)
    
    # Write comprehensive report to text file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("================================\n")
        file.write("   INSTAGRAM FOLLOWING REPORT   \n")
        file.write("================================\n\n")
        file.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        file.write("=== SUMMARY ===\n")
        file.write(f"Total accounts you're following: {len(following)}\n")
        file.write(f"Total accounts following you: {len(followers)}\n")
        file.write(f"Mutual connections: {len(mutual)}\n")
        file.write(f"Not following you back: {len(not_following_back)}\n")
        file.write(f"You don't follow them: {len(you_dont_follow)}\n\n")
        
        # Write accounts that don't follow you back
        file.write("=== ACCOUNTS THAT DON'T FOLLOW YOU BACK ===\n")
        if not_following_back:
            for i, username in enumerate(sorted(not_following_back), 1):
                file.write(f"{i}. {username}\n")
        else:
            file.write("Everyone you follow also follows you back!\n")
        file.write("\n")
        
        # Write accounts you don't follow back
        file.write("=== ACCOUNTS YOU DON'T FOLLOW BACK ===\n")
        if you_dont_follow:
            for i, username in enumerate(sorted(you_dont_follow), 1):
                file.write(f"{i}. {username}\n")
        else:
            file.write("You follow everyone who follows you!\n")
        file.write("\n")
        
        # Write mutual connections
        file.write("=== MUTUAL CONNECTIONS ===\n")
        if mutual:
            for i, username in enumerate(sorted(mutual), 1):
                file.write(f"{i}. {username}\n")
        else:
            file.write("No mutual connections found.\n")
    
    print(f"Instagram report generated and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    write_report() 