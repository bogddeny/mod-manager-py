import time

import filesystem as fs

LOG_DEBUG = True
MODS_DIR = "test/mods"
GAME_DIR = "test/game"
MOUNT_DIR = "test/mount"
PRIORITY_FILE = "profile/mods_priority.txt"


if __name__ == '__main__':
    fs.mount_mods(MODS_DIR, GAME_DIR, MOUNT_DIR, PRIORITY_FILE)
    time.sleep(30)
    fs.unmount_mods(MOUNT_DIR)
