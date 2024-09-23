# Database Backup Tool

This is a simple Python-based GUI application that allows you to back up a MySQL database from a remote server via SSH. The backup is downloaded and compressed into a ZIP file. The tool uses the following libraries:

- `paramiko` for SSH and SFTP communication.
- `zipfile` for compressing the backup file.
- `tkinter` for the graphical user interface (GUI).

## Features

- Connect to a remote server via SSH.
- Run `mysqldump` to back up the database.
- Download the backup file to a local directory.
- Compress the SQL backup into a ZIP file.
- Progress bar to track the backup process.

## Requirements

Ensure you have the following installed:

- Python 3.x
- Paramiko: `pip install paramiko`
- Tkinter: Should be available by default in most Python installations.

## How to Use

1. Clone this repository.

   ```bash
   git clone https://github.com/AnasAfawzy/Database_Backup_Tool.git
   cd backup-tool
   ```

2. Install dependencies:

   ```bash
   pip install paramiko
   ```

3. Run the `Backup.py` script:

   ```bash
   python Backup.py
   ```

4. Enter the required information in the GUI:
   - Hostname of the remote server.
   - SSH port, username, and password for the server.
   - Database name, database username, and password.
   - The local directory where the backup should be saved.

## Author

- **Anas Ashraf Fawy**  
  Email: [anas.a.fawzy@gmail.com](mailto:anas.a.fawzy@gmail.com)
