
# Instagram Followers/Following Analyzer

This tool helps you find out who you follow but who doesn't follow you back on Instagram.  
It uses the **Download Your Information** feature of Instagram and processes the data to generate results.

## 🔧 How It Works

1. **Request Your Data from Instagram**
    - Open the **Instagram app**.
    - Go to **Settings > Your Activity > Download your information**.
    - Select your profile.
    - Under "Some information," scroll down and select:
        - ✅ *Followers and Following*
    - Change the **date range** to *All time*.
    - Choose **HTML** format.
    - Submit the request.

2. **Wait for Instagram’s Email**
    - Instagram will send you a **ZIP file** with your data.
    - This may take anywhere from a few minutes to several hours.

3. **Extract the Data**
    - Download the ZIP file from your email.
    - Extract it into a folder called `data_of_instagram`.

4. **Install Python Requirements**
    - Make sure **Python 3.x** is installed.
    - Install the required Python packages:
      ```bash
      pip install beautifulsoup4
      ```

5. **Run the Script**
    - Place `main.py` in the same directory as the `data_of_instagram` folder.
    - Open a terminal and run:
      ```bash
      python main.py
      ```
    - The script will analyze your followers and following lists.

6. **See the Results**
    - The script will display or save a list of users you follow who **don’t follow you back**.

## 📂 Folder Structure

```plaintext
project/
├── data_of_instagram/
│   ├── followers_and_following/
│   │   ├── followers.html
│   │   ├── following.html
│   └── (other files)
├── main.py
├── README.md
````

## 📝 Requirements

* Python 3.x
* `beautifulsoup4` (install with `pip install beautifulsoup4`)

## ⚠ Notes

* This tool works with data exported directly from Instagram for safety and privacy.
* Be sure to handle your data carefully and delete it when you're done.

## 🔒 Privacy

Your Instagram data stays local on your machine. No data is sent to any servers or third-party services.