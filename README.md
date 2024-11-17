# BabyKickBot
BabyKickBot is a Telegram bot designed to log and summarize baby kicks efficiently. It uses Google Sheets as a backend for storing kick logs and provides reminders when a certain number of kicks are logged within a specified timeframe. This bot ensures secure access and continuous availability using AWS hosting.

---

## Features

- **Log Baby Kicks**:
  - Command `/kick`: Logs the timestamp of a baby kick.
  - Ensures that kicks cannot be logged within 5 minutes of the previous kick.

- **Daily Summary**:
  - Command `/summary`: Provides a summary of kicks logged on the current day.

- **Kick Notification**:
  - Automatically notifies the user if more than 10 kicks are logged within a 12-hour timeframe.

- **Secure Access**:
  - Restricted to specific Telegram user IDs using a whitelist.

---

## Security Features

1. **Telegram User Restriction**:
   - Only whitelisted Telegram user IDs can access the bot.

2. **Google Sheets Access**:
   - Uses a service account with limited permissions to interact with the Google Sheet.
   - Service account credentials are securely stored in a JSON file.

3. **Environment Variables**:
   - Sensitive information (e.g., bot token) is stored in a `.env` file and not hardcoded.

4. **Error Logging**:
   - All errors are logged using Python's `logging` module for debugging.

5. **Rate Limiting**:
   - Prevents kicks from being logged within 5 minutes of the previous entry.

---

## Prerequisites

1. **Telegram Bot**:
   - Create a bot using [BotFather](https://t.me/botfather) and obtain your bot token.

2. **Google Sheets**:
   - Create a Google Sheet with the necessary headers (e.g., `User/ChatGroup ID` and `Timestamp`).
   - Enable Google Sheets and Google Drive APIs.

3. **AWS Free Tier Account**:
   - Set up an AWS EC2 instance for hosting.

---

## Pre-requisite Setup Instructions

### **Google Sheets API Setup**

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project (e.g., `BabyKickBot`).

2. **Enable APIs**:
   - Enable the **Google Sheets API** and **Google Drive API** for the project.

3. **Create a Service Account**:
   - Navigate to **APIs & Services > Credentials**.
   - Create a service account and download the JSON credentials file (e.g., `config.json`).

4. **Share the Sheet with the Service Account**:
   - Open your Google Sheet.
   - Share it with the service account's email (found in the JSON file under `client_email`).
  
---

### **AWS Deployment**

#### **1. Launch an AWS EC2 Instance**

1. Log in to the [AWS Console](https://aws.amazon.com/).
2. Launch an **Amazon Linux 2023 Free Tier** instance with the following configuration:
   - **Instance Type**: `t2.micro`.
   - **Security Group**: Allow SSH (port 22) and HTTPS (port 443).

3. Connect to the instance using SSH:
   ```
   bash
   ssh -i /path/to/key.pem ec2-user@<INSTANCE_PUBLIC_IP>
   ```

### **2. Set Up the Environment on EC2**

**Update Packages** to ensure that your EC2 instance is up-to-date with the latest packages.
```
sudo yum update -y
sudo yum install git python3 -y
```

### **3. Clone the Repository: Clone your bot repository from GitHub to the instance:**
```
git clone https://github.com/imthomas93/BabyKickBot.git
cd BabyKickBot
```

### **4. Install Dependencies and upload Service Account File:**
1. Run pip install using - `pip install --upgrade -r requirements.txt`
2. Use SCP file transfer the config file over to EC2 using `scp -i /path/to/key.pem /path/to/config.json ec2-user@<INSTANCE_PUBLIC_IP>:/home/ec2-user/config.json`

#### **5. Set Up Environment Variables**

To securely store sensitive data like your Telegram bot token and the path to the Google Service Account file, you can use a **`.env`** file in your bot's directory.

---

## Usage
1. Log a Kick: Use the /kick command in Telegram to log a baby kick.
2. Get a Summary: Use the /summary command to retrieve the list of kicks logged today.
3. Automatic Notification: If more than 10 kicks are logged within a 12-hour period, you'll receive a summary automatically.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](License) file for details.
   
