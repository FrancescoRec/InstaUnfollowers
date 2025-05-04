# Who Unfollowed Me? 😈

Sick of mystery unfollowers ruining your day?  
This tool helps you hunt down who’s not returning the love.  
Just grab your Instagram data, follow the steps, and find out who ditched you!

---

## 🚀 What This Tool Can Do

- Reveal which *traitors* (a.k.a. accounts you follow) don’t follow you back.
- Spot people **you** forgot to follow back (oops).
- Create easy-to-read reports.
- Track how your follower drama changes over time.

---

## 📥 Before You Start — Get Your Data

Instagram doesn’t let apps grab your followers list anymore (thanks, privacy policies 😒).  
But don’t worry, it gives **you** your data — you just have to ask nicely.

**Steps to get your data:**

1. Open the **Instagram app**.
2. Go to **Settings > Your Activity > Download your information**.
3. Select:
   - ✅ *Followers and Following*
4. Set the **date range** to *All time* (we want the full story).
5. Choose **HTML** format.
6. Submit the request.
7. Check your email for the download link. (Might take a few minutes or hours — be patient!)

---

## 🗂 Set Things Up

1. Download the ZIP Instagram sends you.
2. Extract it into a folder called: `data_of_instagram`.
3. Make sure these files are inside:
   - `followers.html` (or `followers_1.html`)
   - `following.html`

*(If the script doesn’t see the `data_of_instagram` folder, it’ll try to find the files in the same directory as the script. It’s smart like that.)*

---

## 🐍 Requirements

- **Python 3.6 or higher** (because we’re not living in 2010).
- Install this magic ingredient:
  ```bash
  pip install beautifulsoup4
---
## 🔥 How to Run It

1. Open your terminal or command prompt.
2. Navigate to the folder where your files and scripts are.
3. Run:

   ```bash
   python main.py
   ```
4. Sit back and relax while the script:

   * Converts the Instagram data into CSV files.
   * Analyzes who’s ghosting you.
   * Builds a beautiful report in the `reports` folder.

---

## 📊 What’s in the Report?

Your report will tell you:

* How many people you follow.
* How many follow you back.
* Who doesn’t follow you back (*the heartbreakers 💔*).
* Who you don’t follow back (*the overlooked heroes 🫣*).
* Your mutual followers (*the real ones*).

---

## 📝 Files in This Project

* `convert_to_csv.py` — Turns Instagram HTML files into CSV.
* `find_not_following_back.py` — Finds out who’s ignoring your follow.
* `generate_instagram_report.py` — Creates the final report.
* `main.py` — Runs everything so you don’t have to.

---

## 🛡 Privacy

Your Instagram secrets never leave your computer.
No servers. No clouds. No nosy apps. Just you and the truth.

