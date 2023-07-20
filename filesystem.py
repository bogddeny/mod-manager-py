import os

from subprocess import Popen, PIPE

import logger


def mount_mods(mods_dir: str, game_dir: str, mount_dir: str, priority_file: str):
    logger.log.debug("Mounting Mods")

    # Get a list of mod folders from a specific mods directory
    mods = os.listdir(mods_dir)
    mods_list = [os.path.join(mods_dir, mod) for mod in mods]

    # Read the mod priority text file to get the mods to have the mods load in the correct order
    with open(priority_file, 'r') as f:
        priority_list = f.read().splitlines()

    priority_dict = {mod: priority_list.index(mod) if mod in priority_list else len(priority_list) for mod in mods}

    mods_list.sort(key=lambda mod: priority_dict[os.path.basename(mod)], reverse=True)

    # Join all the mods and the game directories into one string separated by ':'
    mods_string = ":".join(mods_list) + ":" + game_dir
    logger.log.debug(mods_string)

    # Mount all the mods and the game to a specific directory
    process = Popen(["fuse-overlayfs", "-o", f"lowerdir={mods_string}", mount_dir], stdout=PIPE, stderr=PIPE)
    process_wait(process)


def unmount_mods(mount_dir: str):
    logger.log.debug("Unmounting Mods")

    # Unmount a specific directory
    process = Popen(["fusermount", "-uz", mount_dir], stdout=PIPE, stderr=PIPE)
    process_wait(process)


def process_wait(process: Popen[bytes]):
    stdout, stderr = process.communicate()

    if len(stdout) > 0:
        print(stdout.decode().strip())
    if len(stderr) > 0:
        print(stderr.decode().strip())
