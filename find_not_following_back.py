import csv
import os

# Define data folder path
DATA_FOLDER = "data_of_instagram"

# Create data folder if it doesn't exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created data folder: {DATA_FOLDER}")

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

def analyze_followers():
    # File paths
    following_csv = os.path.join(DATA_FOLDER, 'following.csv')
    followers_csv = os.path.join(DATA_FOLDER, 'followers_1.csv')
    output_csv = os.path.join(DATA_FOLDER, 'not_following_back.csv')
    
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
    
    # Create CSV with the results
    with open(output_csv, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'relationship'])
        
        for username in sorted(not_following_back):
            writer.writerow([username, 'not following you back'])
        
        for username in sorted(you_dont_follow):
            writer.writerow([username, 'you don\'t follow them'])
    
    # Print summary
    print(f"Total accounts you're following: {len(following)}")
    print(f"Total accounts following you: {len(followers)}")
    print(f"Mutual connections: {len(following.intersection(followers))}")
    print(f"Not following you back: {len(not_following_back)}")
    print(f"You don't follow them: {len(you_dont_follow)}")
    print(f"\nResults saved to {output_csv}")
    
    # Print the list of users not following you back
    if not_following_back:
        print("\nAccounts that don't follow you back:")
        for i, username in enumerate(sorted(not_following_back), 1):
            print(f"{i}. {username}")

if __name__ == "__main__":
    analyze_followers() 