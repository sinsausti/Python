#!/usr/bin/env python3
"""
===========================================================
 MySQL Replication Setup Script
 Description:
     Automates the process of setting up a MySQL replication
     from a master server to a slave server using:
       - LVM snapshots for consistent backups
       - Rsync for data transfer
       - Automatic configuration of replication on the slave
===========================================================
"""

import os
import sys
import MySQLdb
from time import sleep

# MySQL Master
MASTER_HOST = "10.10.10.10"
MASTER_USER = "root"
MASTER_PASS = "************"
MASTER_DB   = "mysql"
LOCAL_PATH  = "/var/lib/mysql/*"

# MySQL Slave
SLAVE_HOST  = "10.10.10.11"
SLAVE_USER  = "root"
SLAVE_PASS  = "************"
SLAVE_DB    = "mysql"
REMOTE_PATH = "/var/lib/mysql/"

# Replication user
REPL_USER = "replica"
REPL_PASS = "************"

# LVM Configuration
VG_NAME = "pve"
LV_NAME = "data"
SNAPSHOT_NAME = "dbbackup"
SNAPSHOT_SIZE = "3G"

# Rsync Options
RSYNC_OPTS = (
    "-arv --progress --delete --stats "
    "--exclude=user.* --exclude=mysql "
    "-e 'ssh -c blowfish'"
)

# Temporary mount point for snapshot
SNAPSHOT_MOUNT = "/mnt/dbbackup"

# Sleep time after stopping slave MySQL
SLAVE_STOP_DELAY = 10

# ===========================================================
# === FUNCTIONS =============================================
# ===========================================================

def run_cmd(command):
    """Run a system command and check for errors."""
    print(f"→ Executing: {command}")
    if os.system(command) != 0:
        print(f"ERROR executing: {command}")
        cleanup_and_exit(1)

def cleanup_and_exit(code):
    """Unmount snapshot and remove it before exiting."""
    print("Cleaning up snapshot (if mounted)...")
    os.system(f"umount {SNAPSHOT_MOUNT} >/dev/null 2>&1")
    os.system(f"lvremove -f /dev/{VG_NAME}/{SNAPSHOT_NAME} >/dev/null 2>&1")
    sys.exit(code)

def get_master_status():
    """Connects to master and retrieves binary log info."""
    print("Connecting to MySQL master...")
    conn = MySQLdb.connect(
        host=MASTER_HOST, user=MASTER_USER, passwd=MASTER_PASS, db=MASTER_DB
    )
    cursor = conn.cursor()
    print("Flushing and locking tables on master...")
    cursor.execute("FLUSH TABLES")
    cursor.execute("FLUSH LOGS")
    cursor.execute("FLUSH TABLES WITH READ LOCK")
    cursor.execute("SHOW MASTER STATUS")
    row = cursor.fetchone()
    log_file, log_pos = row[0], row[1]
    print(f"Master status: file={log_file}, position={log_pos}")
    return conn, cursor, log_file, log_pos

def release_master_lock(cursor, conn):
    """Unlocks master tables."""
    print("Unlocking master tables...")
    cursor.execute("UNLOCK TABLES")
    cursor.close()
    conn.close()

def create_lvm_snapshot():
    """Creates an LVM snapshot."""
    print("Creating LVM snapshot...")
    run_cmd(f"lvcreate -L{SNAPSHOT_SIZE} -s -n {SNAPSHOT_NAME} /dev/{VG_NAME}/{LV_NAME}")

def mount_snapshot():
    """Mounts the LVM snapshot."""
    print(f"Mounting snapshot at {SNAPSHOT_MOUNT}...")
    os.makedirs(SNAPSHOT_MOUNT, exist_ok=True)
    run_cmd(f"mount -o ro /dev/{VG_NAME}/{SNAPSHOT_NAME} {SNAPSHOT_MOUNT}")

def stop_mysql_slave():
    """Stops MySQL on slave before data transfer."""
    print("Stopping MySQL on slave...")
    run_cmd(f"ssh {SLAVE_HOST} 'systemctl stop mysql'")
    sleep(SLAVE_STOP_DELAY)

def rsync_data():
    """Transfers data from snapshot to slave via rsync."""
    print("Syncing data to slave...")
    run_cmd(
        f"rsync {RSYNC_OPTS} {SNAPSHOT_MOUNT}/private/* {SLAVE_USER}@{SLAVE_HOST}:{REMOTE_PATH}"
    )

def prepare_slave_mysql():
    """Prepares MySQL data directory and restarts slave."""
    print("Preparing MySQL slave...")
    run_cmd(f"ssh {SLAVE_HOST} chown -R mysql:mysql {REMOTE_PATH}")
    run_cmd(f"ssh {SLAVE_HOST} rm -f {REMOTE_PATH}master.info")
    run_cmd(f"ssh {SLAVE_HOST} 'systemctl start mysql'")

def configure_replication(log_file, log_pos):
    """Configures replication on the slave."""
    print("Configuring replication on slave...")
    conn = MySQLdb.connect(
        host=SLAVE_HOST, user=SLAVE_USER, passwd=SLAVE_PASS, db=SLAVE_DB
    )
    cursor = conn.cursor()
    sql = (
        "CHANGE MASTER TO "
        f"MASTER_HOST='{MASTER_HOST}', "
        f"MASTER_USER='{REPL_USER}', "
        f"MASTER_PASSWORD='{REPL_PASS}', "
        "MASTER_PORT=3306, "
        f"MASTER_LOG_FILE='{log_file}', "
        f"MASTER_LOG_POS={log_pos};"
    )
    cursor.execute(sql)
    cursor.execute("START SLAVE")
    cursor.close()
    conn.close()
    print("Replication successfully configured!")

# ===========================================================
# === MAIN SCRIPT ===========================================
# ===========================================================

try:
    # 1. Get master binlog info and lock tables
    conn, cursor, log_file, log_pos = get_master_status()

    # 2. Create LVM snapshot
    create_lvm_snapshot()

    # 3. Unlock tables
    release_master_lock(cursor, conn)

    # 4. Mount snapshot
    mount_snapshot()

    # 5. Stop MySQL slave
    stop_mysql_slave()

    # 6. Sync data via rsync
    rsync_data()

    # 7. Remove snapshot
    print("Removing LVM snapshot...")
    run_cmd(f"umount {SNAPSHOT_MOUNT}")
    run_cmd(f"lvremove -f /dev/{VG_NAME}/{SNAPSHOT_NAME}")

    # 8. Restart slave MySQL and configure replication
    prepare_slave_mysql()
    configure_replication(log_file, log_pos)

    print("MySQL replication is successfully set up!")

except Exception as e:
    print(f"Unexpected error: {e}")
    cleanup_and_exit(1)
