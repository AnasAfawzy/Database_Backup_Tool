import paramiko
import zipfile
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def backup_database():
    progress_bar["value"] = 0
    message_box.delete(1.0, tk.END)

    hostname = entry_hostname.get().strip()
    ssh_port = entry_ssh_port.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    database_name = entry_database.get().strip()
    db_username = entry_db_username.get().strip()
    db_password = entry_db_password.get().strip()
    backup_dir = entry_backup_dir.get().strip()

    if not (
        hostname
        and ssh_port
        and username
        and password
        and database_name
        and db_username
        and db_password
        and backup_dir
    ):
        message_box.insert(tk.END, "Please fill in all fields before proceeding.\n")
        return

    message_box.insert(tk.END, "Connecting to the server...\n")
    root.update_idletasks()

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_filename = f"database_backup_{timestamp}.sql"
    zip_filename = f"database_backup_{timestamp}.zip"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=hostname,
            port=int(ssh_port),
            username=username,
            password=password,
            timeout=30,
        )
        message_box.insert(tk.END, "Connected to the server.\n")
        progress_bar["value"] += 20
        root.update_idletasks()

        dump_command = f"mysqldump -u {db_username} -p'{db_password}' {database_name} > /tmp/{sql_filename}"
        stdin, stdout, stderr = ssh.exec_command(dump_command)

        error = stderr.read().decode()
        if error:
            message_box.insert(tk.END, f"Error during mysqldump: {error}\n")
            ssh.close()
            return
        else:
            message_box.insert(
                tk.END, "Database dump created successfully on the server.\n"
            )
            progress_bar["value"] += 30
            root.update_idletasks()

        sftp = ssh.open_sftp()
        remote_path = f"/tmp/{sql_filename}"
        local_path = os.path.join(backup_dir, sql_filename)

        try:
            sftp.stat(remote_path)
            message_box.insert(tk.END, "Backup file exists, downloading...\n")
            sftp.get(remote_path, local_path)
        except FileNotFoundError:
            message_box.insert(tk.END, "Backup file not found on the server.\n")
            sftp.close()
            ssh.close()
            return

        sftp.close()

        zip_path = os.path.join(backup_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(local_path, arcname=sql_filename)

        os.remove(local_path)

        progress_bar["value"] = 100
        message_box.insert(
            tk.END,
            f"Database backup downloaded and zipped successfully at: {zip_path}\n",
        )

    except paramiko.ssh_exception.NoValidConnectionsError as e:
        message_box.insert(tk.END, f"Failed to connect to the server: {str(e)}\n")
    except TimeoutError:
        message_box.insert(tk.END, "Connection attempt timed out.\n")
    except Exception as e:
        message_box.insert(tk.END, f"An error occurred: {str(e)}\n")
    finally:
        ssh.close()

    progress_bar["value"] = 0
    message_box.delete(1.0, tk.END)

    message_box.insert(tk.END, "Connecting to the server...\n")
    root.update_idletasks()

    hostname = entry_hostname.get()
    ssh_port = int(entry_ssh_port.get())
    username = entry_username.get()
    password = entry_password.get()
    database_name = entry_database.get()
    db_username = entry_db_username.get()
    db_password = entry_db_password.get()
    backup_dir = entry_backup_dir.get()

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_filename = f"database_backup_{timestamp}.sql"
    zip_filename = f"database_backup_{timestamp}.zip"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=hostname,
            port=ssh_port,
            username=username,
            password=password,
            timeout=30,
        )
        message_box.insert(tk.END, "Connected to the server.\n")
        progress_bar["value"] += 20
        root.update_idletasks()

        dump_command = f"mysqldump -u {db_username} -p'{db_password}' {database_name} > /tmp/{sql_filename}"
        stdin, stdout, stderr = ssh.exec_command(dump_command)

        error = stderr.read().decode()
        if error:
            message_box.insert(tk.END, f"Error during mysqldump: {error}\n")
            ssh.close()
            return
        else:
            message_box.insert(
                tk.END, "Database dump created successfully on the server.\n"
            )
            progress_bar["value"] += 30
            root.update_idletasks()

        sftp = ssh.open_sftp()
        remote_path = f"/tmp/{sql_filename}"
        local_path = os.path.join(backup_dir, sql_filename)

        try:
            sftp.stat(remote_path)
            message_box.insert(tk.END, "Backup file exists, downloading...\n")
            sftp.get(remote_path, local_path)
        except FileNotFoundError:
            message_box.insert(tk.END, "Backup file not found on the server.\n")
            sftp.close()
            ssh.close()
            return

        sftp.close()

        zip_path = os.path.join(backup_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(local_path, arcname=sql_filename)

        os.remove(local_path)

        progress_bar["value"] = 100
        message_box.insert(
            tk.END,
            f"Database backup downloaded and zipped successfully at: {zip_path}\n",
        )

    except paramiko.ssh_exception.NoValidConnectionsError as e:
        message_box.insert(tk.END, f"Failed to connect to the server: {str(e)}\n")
    except TimeoutError:
        message_box.insert(tk.END, "Connection attempt timed out.\n")
    except Exception as e:
        message_box.insert(tk.END, f"An error occurred: {str(e)}\n")
    finally:
        ssh.close()


def choose_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        entry_backup_dir.delete(0, tk.END)
        entry_backup_dir.insert(0, dir_path)


root = tk.Tk()
root.title("Database Backup Tool")

tk.Label(root, text="Hostname").grid(row=0, column=0)
entry_hostname = tk.Entry(root)
entry_hostname.grid(row=0, column=1)

tk.Label(root, text="SSH Port").grid(row=1, column=0)
entry_ssh_port = tk.Entry(root)
entry_ssh_port.grid(row=1, column=1)
entry_ssh_port.insert(0, "0")

tk.Label(root, text="SSH Username").grid(row=2, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=2, column=1)

tk.Label(root, text="SSH Password").grid(row=3, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=3, column=1)

tk.Label(root, text="Database Name").grid(row=4, column=0)
entry_database = tk.Entry(root)
entry_database.grid(row=4, column=1)

tk.Label(root, text="DB Username").grid(row=5, column=0)
entry_db_username = tk.Entry(root)
entry_db_username.grid(row=5, column=1)

tk.Label(root, text="DB Password").grid(row=6, column=0)
entry_db_password = tk.Entry(root, show="*")
entry_db_password.grid(row=6, column=1)

tk.Label(root, text="Backup Directory").grid(row=7, column=0)
entry_backup_dir = tk.Entry(root)
entry_backup_dir.grid(row=7, column=1)
tk.Button(root, text="Browse", command=choose_directory).grid(row=7, column=2)

progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=200, mode="determinate"
)
progress_bar.grid(row=8, column=1)

message_box = tk.Text(root, height=10, width=50)
message_box.grid(row=9, column=0, columnspan=3)

tk.Button(root, text="Backup Now", command=backup_database).grid(row=10, column=1)

root.mainloop()
