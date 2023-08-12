import json
import os
import re
import sys
from io import StringIO

# pip install tqdm
from tqdm import tqdm

# adding util_scripts depending on if it's an executable or if it's running from the wcm_gui
if getattr(sys, "frozen", False):
    sys.path.append(
        os.path.join(
            os.path.dirname(sys.executable), "resources", "tools", "util_scripts"
        )
    )
else:
    sys.path.append("..")

from resources.tools.util_scripts.global_paths import (
    AppPaths,
    GlobalDef,
    GlobalVar,
    GameListData,
    FtpSettings,
)

sys.path.append(AppPaths.settings)


def __drive_selection_handler__(selected_drive, selected_platform):
    # drive and platforms to fetch
    selected_drives = []
    platform_filter = []

    # add all drive paths based on choice from drive filter
    if any(x in selected_drive for x in ["ALL"]):
        selected_drives.extend(GlobalVar.drive_paths)
        if selected_drives.count(("/dev_usb(*)/", "USB(*)")) > 0:
            selected_drives.remove(("/dev_usb(*)/", "USB(*)"))

    elif any(x in selected_drive for x in ["USB(*)"]):
        selected_drives.extend(GlobalVar.drive_paths)
        if selected_drives.count(("/dev_usb(*)/", "USB(*)")) > 0:
            selected_drives.remove(("/dev_usb(*)/", "USB(*)"))
        if selected_drives.count(("/dev_hdd0/", "HDD0")) > 0:
            selected_drives.remove(("/dev_hdd0/", "HDD0"))
    # single drive choice, i.e. not 'ALL'
    else:
        selected_drives.extend(
            list(filter(lambda x: str(selected_drive) == x[1], GlobalVar.drive_paths))
        )

    # add all drive paths based on choice from platform filter
    if "ALL" in selected_platform:
        platform_filter.extend(GlobalVar.platform_paths)
    # single platform choice
    else:
        platform_filter.extend(
            list(
                filter(
                    lambda x: str(selected_platform) == x[1], GlobalVar.platform_paths
                )
            )
        )

    return [selected_drives, platform_filter]


class FtpGameList:
    def __init__(self, selected_drive, selected_platform):
        self.selected_drive = selected_drive
        self.selected_platform = selected_platform

        self.game_list_data_json = GameListData().get_game_list_from_disk()
        self.new_game_list_data_json = GameListData().get_game_list_data_json_bak()

        self.coding = GlobalVar.coding

        # messages
        self.PAUSE_MESSAGE = "Press ENTER to continue..."
        self.CONNECTION_ERROR_MESSAGE = "TIPS: Check your PS3 ip-address in webMan VSH menu (hold SELECT on the XMB)"
        self.TITLE_ID_EXCEPTION_MESSAGE = (
            """Exception: 'get_image' failed during regex operation."""
        )

        # platform ISO paths
        self.PSPISO_lines = []
        self.PSXISO_lines = []
        self.PS2ISO_lines = []
        self.PS3ISO_lines = []
        self.NTFS_lines = []
        self.GAMES_lines = []
        self.ALL_lines = []

        # singular instances
        self.total_lines_count = 0
        self.game_count = 0

        self.ftp = None
        self.data_chunk = None

    def execute(self, selected_drive, selected_platform):
        try:
            self.ftp = FtpSettings().get_ftp()
            # get a listing of active drives from the machine
            active_drives_list = []
            self.ftp.retrlines("MLSD /", active_drives_list.append)

            # filter out all active drives that are also selected
            _drives_platforms = __drive_selection_handler__(
                selected_drive, selected_platform
            )
            selected_drives = _drives_platforms[0]
            filtered_drive_list = []
            for sd in selected_drives:
                for a in active_drives_list:
                    ad = "/" + str(a).split(";")[6].strip() + "/"
                    if sd[0] == ad:
                        print("DEBUG adding drive: " + ad + " for scanning")
                        filtered_drive_list.append(sd)
            if len(filtered_drive_list) < 1:
                print("""DEBUG: The USB port you're trying to scan is not active""")

            # fetch the requested paths from the PS3
            selected_platforms = _drives_platforms[1]
            for drive in filtered_drive_list:
                for platform in selected_platforms:
                    if "PSPISO" == platform[1]:
                        self.ftp_walk(
                            self.ftp, drive[0] + platform[0], self.PSPISO_lines
                        )
                    elif "PSXISO" == platform[1]:
                        self.ftp_walk(
                            self.ftp, drive[0] + platform[0], self.PSXISO_lines
                        )
                    elif "PS2ISO" == platform[1]:
                        self.ftp_walk(
                            self.ftp, drive[0] + platform[0], self.PS2ISO_lines
                        )
                    elif "PS3ISO" == platform[1]:
                        self.ftp_walk(
                            self.ftp, drive[0] + platform[0], self.PS3ISO_lines
                        )
                    elif "NTFS" == platform[1] and "HDD0" in drive[1]:
                        self.ftp_walk(self.ftp, drive[0] + platform[0], self.NTFS_lines)
                    elif "GAMES" == platform[1]:
                        self.ftp_walk(
                            self.ftp, drive[0] + platform[0], self.GAMES_lines
                        )
                        self.ftp_walk(self.ftp, drive[0] + "GAMEZ/", self.GAMES_lines)

            # filter out any empty entries
            self.ALL_lines.append(self.PSPISO_lines)
            self.ALL_lines.append(self.PSXISO_lines)
            self.ALL_lines.append(self.PS2ISO_lines)
            self.ALL_lines.append(self.PS3ISO_lines)
            self.ALL_lines.append(self.NTFS_lines)
            self.ALL_lines.append(self.GAMES_lines)

            for p in self.ALL_lines:
                self.total_lines_count += len(p)

            # after retrieving the list of filepaths we now request the actual data
            self.data_chunk = FTPDataHandler(self.ftp, self.total_lines_count)

        except Exception as e:
            error_message = str(e)
            print("Connection error: " + error_message)
            print(self.CONNECTION_ERROR_MESSAGE)
            print("\n")

            return

        # append the current platform games to the new list
        for platform in self.game_list_data_json:
            self.game_list_data_builder(str(platform.split("_")[0]))

        # save updated gamelist to disk
        with open(
            os.path.join(AppPaths.application_path, "game_list_data.json"), "w"
        ) as newFile:
            json_text = json.dumps(
                self.game_list_data_json, indent=4, separators=(",", ":")
            )
            newFile.write(json_text)

    def game_list_data_builder(self, original_platform):
        platform_list = original_platform + "_games"
        filtered_platform = None
        if "PSPISO" in platform_list:
            filtered_platform = self.PSPISO_lines
        elif "PSXISO" in platform_list:
            filtered_platform = self.PSXISO_lines
        elif "PS2ISO" in platform_list:
            filtered_platform = self.PS2ISO_lines
        elif "PS3ISO" in platform_list:
            filtered_platform = self.PS3ISO_lines
        elif "NTFS" in platform_list:
            filtered_platform = self.NTFS_lines
        elif "GAMES" in platform_list:
            filtered_platform = self.GAMES_lines

        # instantiate variables
        title_id = None
        meta_data_link = None
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None

        game_exist = False
        skip_already_fetched = False  # should be a config option

        for new_game_path in tqdm(
            filtered_platform,
            desc="Fetching " + original_platform,
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}]\n",
        ):
            new_game_dir_path = str(os.path.dirname(new_game_path).__add__("/"))
            new_game_filename = str(os.path.basename(new_game_path))
            new_game_platform_path = str(new_game_dir_path)
            new_game_platform = str(original_platform)

            # .NTFS[xxx] gets a donor platform for metadata scraping
            if new_game_platform == "NTFS":
                match = re.search("(?<=\[).*?(?=\])", new_game_filename)
                if match is not None:
                    # These will not match: '.NTFS[BDISO]', '.NTFS[DVDISO]', '.NTFS[BDFILE]',
                    tmp_platform = list(
                        filter(
                            lambda x: match.group() in x[0], GlobalVar.platform_paths
                        )
                    )
                    if tmp_platform:
                        new_game_platform = tmp_platform[0][1]
            # GAMES get the PS3 metadata
            elif new_game_platform in {"GAMES", "GAMEZ"}:
                donor_platform = "PS3ISO"
                new_game_platform = donor_platform

            # check if game already exist
            if not skip_already_fetched:
                for game_json in self.game_list_data_json[platform_list]:
                    existing_game_path = str(
                        os.path.join(game_json["path"], game_json["filename"])
                    )

                    if new_game_platform in {"GAMES", "GAMEZ"}:
                        # Since GAMES-folders get variations of the titles we will compare their base paths
                        new_game_path = "/".join(new_game_path.split("/")[:-2]) + "/"
                        existing_game_path = (
                            "/".join(existing_game_path.split("/")[:-1]) + "/"
                        )

                    if new_game_path == existing_game_path:
                        self.game_count += 1
                        print(
                            "\nDEBUG skipping "
                            + new_game_filename
                            + ", already fetched\n"
                        )
                        game_exist = True
                        pass

            if not game_exist:
                # parsing PARAM.SFO should provide correct title_id and title for the GUI
                if original_platform in {"GAMES", "GAMEZ"}:
                    data = []
                    PARAM_SFO_PATH = new_game_platform_path + "PARAM.SFO"
                    self.ftp.retrbinary("RETR " + PARAM_SFO_PATH, callback=data.append)
                    title_id, title = param_sfo_parser(b"".join(data))

                    # if title_id still None, try get it from the folder name
                    if title_id is None:
                        title_id_match = re.search("(\w{4}\d{5})", new_game_dir_path)
                        # find title_id in folder name
                        if title_id_match:
                            title_id = title_id_match.group(0)
                        else:
                            print(
                                "DEBUG: Folder-game in: "
                                + new_game_dir_path
                                + " does not contain mandatory 'title_id' in its folder name\n skipping metadata"
                            )
                            self.game_count += 1
                            break

                    if title is None:
                        title = "[" + title_id + "]"
                    new_game_filename = (
                        "".join(e for e in title if e.isalnum()) + " [" + title_id + "]"
                    )
                    new_game_filename = str(new_game_filename).replace(" ", "_")

                else:
                    title_id, icon0, pic0, pic1, pic2, at3, pam = self.get_game_data(
                        new_game_dir_path, new_game_filename
                    )
                    title = new_game_filename.strip()

                # removes the file extension and use it as title
                for file_ext in GlobalVar.file_extensions:
                    if new_game_filename.upper().endswith(file_ext):
                        title = str(title[0 : len(title) - len(file_ext)])
                        break

                # removes parenthesis & brackets including their content
                tmp_title = re.sub(r"\([^)]*\)", "", title)
                tmp_title = re.sub(r"\[[^)]*\]", "", tmp_title)
                if tmp_title != "":
                    title = tmp_title

                # check for a match in the platform game database
                if title_id is not None and title_id != "":
                    # read platform db
                    platform_db_file = (
                        new_game_platform.replace("ISO", "") + "_all_title_ids.json"
                    )
                    with open(
                        os.path.join(AppPaths.games_metadata, platform_db_file),
                        encoding="utf8",
                    ) as f:
                        self.json_platform_metadata = json.load(f)

                    for game_json in self.json_platform_metadata["games"]:
                        # adapt the title_id format for the xml db
                        if new_game_platform == "PS3ISO":
                            title_id = title_id.replace("-", "")

                        if title_id == game_json["title_id"]:
                            if (
                                new_game_platform == "PSPISO"
                                or new_game_platform == "PSXISO"
                                or new_game_platform == "PS2ISO"
                            ):
                                title = str(game_json["title"]).strip()

                                if game_json["meta_data_link"] is not None:
                                    meta_data_link = game_json["meta_data_link"]

                            elif new_game_platform == "PS3ISO":
                                # use the first element for English
                                title = str(game_json["locale"][0]["title"]).strip()
                            break

                # add game to list of new games
                self.game_count += 1

                if new_game_platform != original_platform:
                    if original_platform in {"GAMES", "GAMEZ"}:
                        split_path = new_game_platform_path.split("/")
                        new_game_platform_path = (
                            "/".join(split_path[0 : len(split_path) - 2]) + "/"
                        )
                    new_game_platform = original_platform
                print("path is", new_game_platform_path)
                game = {
                    "title_id": title_id,
                    "title": title,
                    "platform": new_game_platform,
                    "filename": new_game_filename,
                    "path": new_game_platform_path,
                    "meta_data_link": meta_data_link,
                }
                self.new_game_list_data_json[platform_list].append(game)

                # also append it to the existing list for next iteration
                self.game_list_data_json[platform_list].append(game)

                print(
                    "DEBUG '"
                    + new_game_filename
                    + "' got the title '"
                    + title
                    + "'"
                    + "\n"
                )
                print("Added '" + title + "' to the list:\n", game)

            # save data to game build folder here
            game_build_dir = AppPaths().get_game_build_dir(title_id, new_game_filename)

            if game_build_dir is not None:
                # save images to game work folders
                image_saver(
                    self.ftp,
                    new_game_platform_path,
                    new_game_platform,
                    game_build_dir,
                    [icon0, pic0, pic1, pic2, at3, pam],
                )

            # reset game data for next iteration
            title = None
            title_id = None
            meta_data_link = None
            new_game_platform = original_platform

        return self.new_game_list_data_json

    def get_game_data(self, platform_path, game_filename):
        title_id = None
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None
        platform = None

        game_filepath = os.path.join(platform_path, game_filename)

        try:
            split_folder_path = game_filepath.split("/")
            platform = split_folder_path[2] + "/"
            platform_match = list(
                filter(lambda x: platform in x[0], GlobalVar.platform_paths)
            )
            platform = platform_match[0][1]

            original_platform = platform
            # this is where .NTFS[xxx] files need a donor platform
            if platform == "NTFS":
                match = re.search("(?<=\[).*?(?=\])", game_filename)
                if match is not None:
                    # These will not match: '.NTFS[BDISO]', '.NTFS[DVDISO]', '.NTFS[BDFILE]',
                    donor_platform = list(
                        filter(
                            lambda x: match.group() in x[0], GlobalVar.platform_paths
                        )
                    )
                    if donor_platform:
                        platform = donor_platform[0][1]
            elif platform in {"GAMES", "GAMEZ"}:
                donor_platform = "PS3ISO"
                platform = donor_platform

        except Exception as e:
            print("ERROR could not parse platform")
            print(getattr(e, "message", repr(e)))

        try:
            # if no offset
            (
                title_id,
                icon0,
                pic0,
                pic1,
                pic2,
                at3,
                pam,
            ) = self.data_chunk.ftp_buffer_data(
                game_filepath,
                platform,
                FtpSettings.ftp_chunk_size_kb,
                0,
                self.game_count,
                FtpSettings.ftp_retry_count,
            )

            # make another fetch with rest offset for PSP images
            if platform == "PSPISO":
                (
                    not_used,
                    icon0,
                    pic0,
                    pic1,
                    pic2,
                    at3,
                    pam,
                ) = self.data_chunk.ftp_buffer_data(
                    game_filepath,
                    platform,
                    FtpSettings.ftp_chunk_size_kb,
                    FtpSettings.ftp_psp_png_offset_kb,
                    self.game_count,
                    FtpSettings.ftp_retry_count,
                )

            # PS3 guitar hero games needs a larger chunk to find the PIC1
            elif platform == "PS3ISO" and "guitar" in game_filename.lower():
                (
                    not_used,
                    icon0,
                    pic0,
                    pic1,
                    pic2,
                    at3,
                    pam,
                ) = self.data_chunk.ftp_buffer_data(
                    game_filepath,
                    platform,
                    6000,
                    0,
                    self.game_count,
                    FtpSettings.ftp_retry_count,
                )

        # retry connection
        except Exception as e:
            print("DEBUG Error: " + getattr(e, "message", repr(e)))
            print(
                "Connection timed out, re-connecting in "
                + str(FtpSettings.ftp_timeout)
                + "s...\n"
            )

            self.ftp = FtpSettings().get_ftp()
            self.data_chunk = FTPDataHandler(self.ftp, self.total_lines_count)

            (
                title_id,
                icon0,
                pic0,
                pic1,
                pic2,
                at3,
                pam,
            ) = self.data_chunk.ftp_buffer_data(
                game_filepath,
                platform,
                FtpSettings.ftp_chunk_size_kb,
                0,
                self.game_count,
                FtpSettings.ftp_retry_count,
            )

            # make another fetch with rest offset for PSP images
            if platform == "PSPISO":
                (
                    title_id,
                    icon0,
                    pic0,
                    pic1,
                    pic2,
                    at3,
                    pam,
                ) = self.data_chunk.ftp_buffer_data(
                    game_filepath,
                    platform,
                    FtpSettings.ftp_chunk_size_kb,
                    FtpSettings.ftp_psp_png_offset_kb,
                    self.game_count,
                    FtpSettings.ftp_retry_count,
                )

            # PS3 guitar hero games needs a larger chunk to find the PIC1
            elif platform == "PS3ISO" and "guitar" in game_filename.lower():
                (
                    not_used,
                    icon0,
                    pic0,
                    pic1,
                    pic2,
                    at3,
                    pam,
                ) = self.data_chunk.ftp_buffer_data(
                    game_filepath,
                    platform,
                    6000,
                    0,
                    self.game_count,
                    FtpSettings.ftp_retry_count,
                )

        return title_id, icon0, pic0, pic1, pic2, at3, pam

    def ftp_walk(self, ftp, folder_path, files):
        print("DEBUG adding: " + folder_path + " for scanning")
        depth = len(folder_path.split("/")) - 2
        extensions = GlobalVar.file_extensions
        ftp_folder_depth = FtpSettings.ftp_folder_depth

        # only NTFS extensions are valid in this folder
        if "tmp/wmtmp/" in folder_path:
            extensions = tuple([i for i in list(extensions) if "NTFS" in i])

        elif "GAMES/" in folder_path:
            ftp_folder_depth = 4
            extensions = ".SFO"

        dirs = []
        stuff = []
        try:
            ftp.retrlines("MLSD " + folder_path, stuff.append)
        except Exception as e:
            print(
                "DEBUG retrlines error: "
                + getattr(e, "message", repr(e))
                + "\n during command retrlines('MLSD "
                + folder_path
                + "')"
            )

            try:
                print("DEBUG retrying -> retrlines('MLSD " + folder_path + "')")
                self.ftp = FtpSettings().get_ftp()
                self.ftp.retrlines("MLSD " + folder_path, stuff.append)

            except Exception as e:
                print(
                    "DEBUG retrlines error: "
                    + getattr(e, "message", repr(e))
                    + "\n during retry of command retrlines('MLSD "
                    + folder_path
                    + "')"
                )
                return files

        for item in stuff:
            split_item = item.split(";")
            # check if it's a dir or a file
            if split_item[0] == "type=dir":
                dirs.append(split_item[len(split_item) - 1].strip())

            elif split_item[0] == "type=file":
                # a file must have at least size of 1 byte
                if (
                    "size=" in split_item[1]
                    and int(split_item[1].replace("size=", "")) > 0
                ):
                    filename = split_item[len(split_item) - 1].strip()

                    # make sure that .BIN.ENC files has capitalized extension
                    if filename.upper().endswith(".BIN.ENC"):
                        if filename.endswith(".BIN.ENC"):
                            files.append(
                                os.path.join(
                                    folder_path
                                    + split_item[len(split_item) - 1].strip()
                                )
                            )
                        else:
                            # we need to return here or it will be included in the next clause
                            return files
                    # check if filename ends with any of our white listed extensions
                    elif filename.upper().endswith(extensions):
                        files.append(
                            os.path.join(
                                folder_path + split_item[len(split_item) - 1].strip()
                            )
                        )

        if len(dirs) > 0 and depth < ftp_folder_depth:
            for subdir in sorted(dirs):
                current_dir = os.path.join(folder_path, subdir + "/")
                self.ftp_walk(ftp, current_dir, files)
        return files


class FTPDataHandler:
    def __init__(self, ftp, total_lines):
        self.coding = GlobalVar.coding
        GlobalVar.platform_paths = GlobalVar.platform_paths
        self.ftp_instance = ftp
        self.ftp_instance.voidcmd("TYPE I")
        self.null = None
        self.lines_count = total_lines

        self.data = None
        self.platform = None
        self.image_duplicate = None
        self.image_name = None
        self.current_image_name = None

        self.icon0_image = None
        self.has_icon0 = None

        self.pic0_image = None
        self.has_pic0 = None

        self.pic1_image = None
        self.has_pic1 = None

        self.pic2_image = None
        self.has_pic2 = None

        self.has_at3 = None
        self.at3_image = None
        self.at3_size = None

        self.has_pam = None
        self.pam_image = None
        self.pam_size = None

    def ftp_buffer_data(
        self, filepath, platform, chunk_size, rest, game_count, ftp_retry_count
    ):
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None

        filename = os.path.basename(filepath)
        game_title = filename[0 : len(filename) - 4]

        file_size_bytes = self.ftp_instance.size(filepath)
        if file_size_bytes > 0 and file_size_bytes < (chunk_size * 1024):
            chunk_size = (file_size_bytes / 1024) * 0.95
        elif platform == ("PSX", "PS2"):
            chunk_size = 750

        if rest * 1024 > file_size_bytes:
            rest = 0

        def fill_buffer(self, rec):
            received = rec.decode(self.coding)
            if self.chunk_size <= 0:
                return True
            else:
                self.sio.write(received)
            self.chunk_size -= len(received)

        game_title_id = ""
        self.sio = StringIO()
        self.chunk_size = chunk_size * 1024

        offset = max(rest * 1024, 0)
        conn = self.ftp_instance.transfercmd("RETR " + filepath, rest=offset)
        retry_cnt = 0
        while 1:
            # the buffer size seems a bit random, can't remember why(?)
            try:
                data = conn.recv(1460)
            except Exception as e1:
                error_msg = ""
                if getattr(e1, "message", repr(e1)) != "":
                    error_msg = getattr(e1, "message", repr(e1))
                else:
                    error_msg = repr(e1)
                    # print('DEBUG ERROR traceback: ' + str(traceback.print_exc()))
                    # offset = max(rest*1024, 0)

                print("ERROR when fetching '" + filename + "', reason: " + error_msg)
                print("DEBUG Retrying fetching of '" + filename + "'")
                retry_cnt += 1
                print("DEBUG retry_cnt: " + str(retry_cnt))
                # retry fetching
                if retry_cnt < ftp_retry_count:
                    try:
                        conn = self.ftp_instance.transfercmd(
                            "RETR " + filepath, rest=offset
                        )
                    except:
                        print(
                            "ERROR could not refetch "
                            + filename
                            + ", skipping metadata"
                        )
                        data = None
                else:
                    print("ERROR could not refetch " + filename + ", skipping metadata")
                    break

            # if None: re-fetch attempt has failed => skip game by breaking the loop
            if data is None:
                game_count += 1
                break
            else:
                if fill_buffer(self, data):
                    try:
                        conn.close()
                        self.ftp_instance.voidresp()

                    # intended exception: this is thrown when the full data chunk been stored in buffer
                    except Exception as e:
                        # reset values for next round
                        icon0 = None
                        pic0 = None
                        pic1 = None
                        pic2 = None
                        pam = None
                        at3 = None

                        self.data_chunk = self.sio.getvalue()
                        self.sio.close()

                        # try find title_id from beginning of file for all platforms
                        if rest == 0:
                            game_title_id = get_title_id_from_buffer(
                                self, platform, self.data_chunk
                            )

                        # PS3 and PSP are the only platforms that has game art embedded
                        if platform == "PSPISO" or platform == "PS3ISO":
                            icon0, pic0, pic1, pic2 = get_png_from_buffer(
                                self, platform, filename, self.data_chunk
                            )

                            if platform == "PS3ISO":
                                at3 = get_at3_from_buffer(
                                    self, platform, filename, self.data_chunk
                                )
                                pam = get_PAM_from_buffer(
                                    self, platform, filename, self.data_chunk
                                )

                                try:
                                    at3_size_KB = int(len(at3) * 0.978 / 1000)
                                    pam_size_KB = int(len(at3) * 0.978 / 1000)
                                    if at3_size_KB + pam_size_KB > 24000:
                                        print(
                                            "ERROR: the sum of the sizes of SND0.AT3 + ICON1.PAM can't be larger than 2.4MB"
                                        )
                                except:
                                    pass

                        # Error 451 is normal when closing the connection
                        if "451" not in getattr(e, "message", repr(e)):
                            print(
                                "DEBUG - connection "
                                + getattr(e, "message", repr(e))
                                + " during data fetching of '"
                                + filename
                                + "'"
                            )
                        break

        return game_title_id, icon0, pic0, pic1, pic2, at3, pam


def get_title_id_from_buffer(self, platform, buffer_data):
    title_id = ""
    try:
        # psx and ps2
        if platform == "PSXISO" or platform == "PS2ISO":
            for m in re.finditer("""\w{4}\_\d{3}\.\d{2}""", buffer_data):
                if m is not None:
                    title_id = str(m.group(0)).strip()
                    title_id = title_id.replace("_", "-")
                    title_id = title_id.replace(".", "")

        elif platform == "PS3ISO":
            for m in re.finditer("""\w{4}-\d{5} """, buffer_data):
                if m is not None:
                    title_id = str(m.group(0)).strip()

        elif platform == "PSPISO":
            for m in re.finditer("""\w{4}-\d{5}\|""", buffer_data):
                title_id = str(m.group(0)).strip()
                title_id = title_id[0 : len(title_id) - 1]

    except Exception as e:
        print("ERROR -> get_title_id_from_buffer: " + getattr(e, "message", repr(e)))
    finally:
        return title_id


def get_png_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data

    try:
        self.has_icon0 = False
        self.has_pic0 = False
        self.has_pic1 = False
        self.has_pic2 = False
        self.image_duplicate = False

        self.icon0_image = None
        self.pic0_image = None
        self.pic1_image = None
        self.pic2_image = None
        self.image_name = None

        # these byte sequences are standard start and end of PNGs
        def png_finder(data, image_name):
            index_png_start = data.find(
                (b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A").decode(self.coding)
            )
            png_end_seq = b"\x49\x45\x4E\x44\xAE\x42\x60\x82".decode(self.coding)
            index_png_end = data.find(png_end_seq, index_png_start)

            self.image_duplicate = False
            self.image_name = image_name
            if index_png_start != -1:
                if index_png_end != -1:
                    import PIL.Image as Image
                    import io

                    png_byte_array = data[
                        index_png_start : index_png_end + len(png_end_seq)
                    ].encode(self.coding)
                    tmp_image = Image.open(io.BytesIO(png_byte_array)).convert("RGBA")
                    self.current_image_name = None

                    if self.platform == "PSPISO":
                        # icon image PSP
                        if tmp_image.size == (144, 80):
                            self.current_image_name = "ICON0.PNG"
                            if not self.has_icon0:
                                self.icon0_image = png_byte_array
                                self.has_icon0 = True

                        # this is background image for PSP
                        elif tmp_image.size == (480, 272):
                            self.current_image_name = "PIC1.PNG"
                            if not self.has_pic1:
                                self.pic1_image = png_byte_array
                                self.has_pic1 = True

                    elif self.platform == "PS3ISO":
                        # icon image PS3
                        if tmp_image.size == (320, 176):
                            self.current_image_name = "ICON0.PNG"
                            if not self.has_icon0:
                                self.icon0_image = png_byte_array
                                self.has_icon0 = True

                        # when multiple pic0 we pic the first for English
                        elif tmp_image.size == (1000, 560):
                            self.current_image_name = "PIC0.PNG"
                            if not self.has_pic0:
                                self.pic0_image = png_byte_array
                                self.has_pic0 = True

                        # this is background image PS3
                        elif tmp_image.size == (1920, 1080):
                            self.current_image_name = "PIC1.PNG"
                            if not self.has_pic1:
                                self.pic1_image = png_byte_array
                                self.has_pic1 = True

                        # PIC2 is variant of the PIC0 for 4:3 screens
                        elif tmp_image.size == (310, 250):
                            self.current_image_name = "PIC2.PNG"
                            if not self.has_pic2:
                                self.pic2_image = png_byte_array
                                self.has_pic2 = True

                    if self.current_image_name is not None:
                        # crop data for next iteration
                        self.data = data[index_png_end : len(data) - 1]
                        return True

                return False

        while png_finder(str(self.data), self.image_name):
            print("DEBUG Found " + self.current_image_name + " for '" + game_name + "'")

        return self.icon0_image, self.pic0_image, self.pic1_image, self.pic2_image

    except Exception as e:
        print("ERROR: get_png_from_buffer - " + getattr(e, "message", repr(e)))
        return self.icon0_image, self.pic0_image, self.pic1_image, self.pic2_image


def get_PAM_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data

    try:
        self.has_pam = False
        self.pam_image = None
        self.image_name = None
        self.pam_size = 0

        # these byte sequences are standard start and end of PNGs
        def PAM_finder(data, image_name, pam_size):
            index_pam_start = data.find(
                b"\x50\x41\x4D\x46\x30\x30\x34\x31".decode(self.coding)
            )
            pam_stop_seq = b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF".decode(
                self.coding
            )

            self.image_name = image_name
            if index_pam_start > -1:
                # TODO: make more solid somehow?
                index_png_start = data.find(
                    b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A".decode(self.coding),
                    index_pam_start,
                )

                # find the last occurrence of the stop sequence and use as eof
                index_pam_end = (
                    index_pam_start
                    + data[index_pam_start:index_png_start].rfind(pam_stop_seq)
                    + len(pam_stop_seq)
                )
                if index_pam_end > -1:
                    tmp_image = data[index_pam_start:index_pam_end].encode(self.coding)
                    self.pam_size = len(tmp_image)

                    # PAM image PS3
                    if tmp_image is not None:
                        self.current_image_name = "ICON1.PAM"
                        if not self.has_pam:
                            self.pam_image = tmp_image
                            self.has_pam = True

                    if self.current_image_name is not None:
                        # crop data for next iteration
                        self.data = data[index_pam_end : len(data) - 1].encode(
                            self.coding
                        )
                        return True

                return False

        while PAM_finder(self.data, self.image_name, self.pam_size):
            # if int(self.pam_size) > 0:
            #     print('DEBUG ICON1.PAM size: ' + str(int(self.pam_size*0.978/1000)) + 'KB')
            if int(self.pam_size * 0.978 / 1000) > 24000:
                print("""ERROR The size of ICON1.PAM can't be larger than 2.4MB.""")

            print("DEBUG Found " + self.current_image_name + " for '" + game_name + "'")

        return self.pam_image

    except Exception as e:
        print("ERROR: get_PAM_from_buffer - " + getattr(e, "message", repr(e)))
        return self.pam_image


# TODO The sum of the sizes of SND0.AT3 + ICON1.PAM can't be larger than 2.4MB
def get_at3_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data
    self.at3_image = ""

    try:
        self.has_at3 = False
        self.image_name = None
        self.at3_size = 0
        self.at3_image = None

        # these byte sequences are standard start and end of PNGs
        def at3_finder(data, image_name, file_size):
            index_at3_start = (
                data.find(b"\x57\x41\x56\x45\x66\x6D\x74\x20".decode(self.coding)) - 8
            )
            at3_stop_seq = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00".decode(
                self.coding
            )

            self.image_name = image_name
            if index_at3_start > -1:
                # find the last occurrence of the stop sequence and use as eof
                index_at3_end = index_at3_start + data[index_at3_start:].find(
                    at3_stop_seq
                )

                if index_at3_end > -1:
                    tmp_image = data[index_at3_start:index_at3_end].encode(self.coding)
                    self.at3_size = len(tmp_image)

                    # AT3 image PS3
                    if tmp_image is not None:
                        self.current_image_name = "SND0.AT3"
                        if not self.has_at3:
                            self.at3_image = tmp_image
                            self.has_at3 = True

                    if self.current_image_name is not None:
                        # crop data for next iteration
                        self.data = data[index_at3_end : len(data) - 1].encode(
                            self.coding
                        )
                        return True

                return False

        while at3_finder(self.data, self.image_name, self.at3_size):
            # if int(self.at3_size) > 0:
            #      print('DEBUG SND0.AT3 size: ' + str(int(self.at3_size*0.978/1000)) + 'KB')
            if int(self.at3_size * 0.978 / 1000) > 24000:
                print("""ERROR The size of SND0.AT3 can't be larger than 2.4MB.""")

            print("DEBUG Found " + self.current_image_name + " for '" + game_name + "'")
            break

        # return self.at3_image

    except Exception as e:
        print("ERROR: get_AT3_from_buffer - " + getattr(e, "message", repr(e)))

    return self.at3_image


def image_saver(ftp, platform_path, platform, game_build_dir, images):
    import shutil
    import PIL.Image as Image
    import io

    icon0 = images[0]
    pic0 = images[1]
    pic1 = images[2]
    pic2 = images[3]
    at3 = images[4]
    pam = images[5]

    game_work_dir = os.path.join(game_build_dir, "work_dir")
    game_pkg_dir = os.path.join(game_work_dir, "pkg")
    try:
        if os.path.isdir(game_pkg_dir):
            if "webman-classics-maker" in game_pkg_dir.lower():
                shutil.rmtree(game_pkg_dir)
            os.makedirs(game_pkg_dir)
    except Exception as e:
        print(
            "ERROR: could not clean the folder: "
            + game_work_dir
            + "\n"
            + "Please close any file browser accessing the specific folder."
        )
    GlobalDef().copytree(
        os.path.join(AppPaths.util_resources, "pkg_dir_bak"),
        os.path.join(game_work_dir, "pkg"),
    )

    # check if platform is GAMES
    split_path = platform_path.split("/")
    if split_path[len(split_path) - 3] in {"GAMES", "GAMEZ"}:
        icon0, pic0, pic1, pic2, at3, pam = [None, None, None, None, None, None]

        # fetch a list of names from the game folder
        PS3_GAME_path = platform_path + "PS3_GAME/"
        stuff = []
        try:
            ftp.retrlines("MLSD " + PS3_GAME_path, stuff.append)

        except Exception as e:
            print(
                "DEBUG image_saver - retrlines error: "
                + getattr(e, "message", repr(e))
                + "\n during command retrlines('MLSD "
                + PS3_GAME_path
                + "')"
            )
            # retry
            print("Retrying ...")
            ftp.retrlines("MLSD " + PS3_GAME_path, stuff.append)

        if len(stuff) > 0:
            # sort out filenames only from the list
            fetched_files = []
            for item in stuff:
                split_item = item.split(";")
                if split_item[0] == "type=file":
                    fetched_files.append(str(split_item[len(split_item) - 1]).strip())
            # fetch the files that match our filename_list
            filename_list = [
                "ICON0.PNG",
                "PIC0.PNG",
                "PIC1.PNG",
                "PIC2.PNG",
                "SND0.AT3",
                "ICON1.PAM",
            ]
            file_data_list = [None, None, None, None, None, None]
            for pkg_fname in filename_list:
                if pkg_fname in fetched_files:
                    try:
                        data = []
                        filepath = PS3_GAME_path + pkg_fname
                        ftp.retrbinary("RETR " + filepath, data.append)
                        file_data_list[filename_list.index(pkg_fname)] = b"".join(data)
                        # file_data_list[filename_list.index(pkg_fname)] = data
                    except Exception as e:
                        print(
                            "DEBUG image_saver() - retrlines error: "
                            + getattr(e, "message", repr(e))
                        )
                        print(
                            "Skipping "
                            + pkg_fname
                            + " for "
                            + split_path[len(split_path) - 2]
                        )
                        continue
            # assign any all data values to our file variables
            icon0, pic0, pic1, pic2, at3, pam = file_data_list

    # platforms such as PSP needs rescaling of images
    if icon0 is not None:
        icon0_image = Image.open(io.BytesIO(icon0)).convert("RGBA")

        if platform == "PSPISO":
            t_icon0 = Image.open(
                os.path.join(
                    AppPaths.application_path,
                    "resources",
                    "images",
                    "pkg",
                    "default",
                    "transparent_ICON0.PNG",
                )
            ).convert("RGBA")
            icon0_image = icon0_image.resize(
                (int(icon0_image.width * 2), int(icon0_image.height * 2)),
                Image.ANTIALIAS,
            )
            x_pos = (t_icon0.width - icon0_image.width) / 2
            y_pos = (t_icon0.height - icon0_image.height) / 2
            t_icon0.paste(icon0_image, (x_pos, y_pos), icon0_image)

            t_icon0.save(os.path.join(game_build_dir, "work_dir", "pkg", "ICON0.PNG"))
        else:
            icon0_image.save(
                os.path.join(game_build_dir, "work_dir", "pkg", "ICON0.PNG")
            )

    else:
        default_pkg_img_dir = os.path.join(
            AppPaths.resources, "images", "pkg", "default"
        )
        icon0_platform_path = os.path.join(default_pkg_img_dir, platform, "ICON0.PNG")
        if not os.path.isfile(icon0_platform_path):
            platform = ""
        shutil.copyfile(
            os.path.join(default_pkg_img_dir, platform, "ICON0.PNG"),
            os.path.join(game_build_dir, "work_dir", "pkg", "ICON0.PNG"),
        )

    if pic0 is not None:
        pic0_image = Image.open(io.BytesIO(pic0)).convert("RGBA")
        if platform == "PSPISO":
            t_pic0 = Image.open(
                os.path.join(
                    AppPaths.application_path,
                    "resources",
                    "images",
                    "pkg",
                    "default",
                    "transparent_PIC0.PNG",
                )
            ).convert("RGBA")
            x_pos = (t_pic0.width - pic0_image.width) / 2
            y_pos = (t_pic0.height - pic0_image.height) / 2
            t_pic0.paste(pic0_image, (x_pos, y_pos), pic0_image)

            t_pic0.save(os.path.join(game_build_dir, "work_dir", "pkg", "PIC0.PNG"))
        else:
            pic0_file = open(
                os.path.join(game_build_dir, "work_dir", "pkg", "PIC0.PNG"), "wb"
            )
            pic0_file.write(pic0)
            pic0_file.close()

    if pic1 is not None:
        pic1_image = Image.open(io.BytesIO(pic1)).convert("RGBA")
        if platform == "PSPISO":
            t_pic1 = Image.open(
                os.path.join(
                    AppPaths.application_path,
                    "resources",
                    "images",
                    "pkg",
                    "default",
                    "transparent_PIC1.PNG",
                )
            ).convert("RGBA")
            pic1_image = pic1_image.resize(
                (int(pic1_image.width * 3), int(pic1_image.height * 3)), Image.ANTIALIAS
            )
            x_pos = (t_pic1.width - pic1_image.width) / 2
            y_pos = (t_pic1.height - pic1_image.height) / 2
            t_pic1.paste(pic1_image, (x_pos, y_pos), pic1_image)

            t_pic1.save(os.path.join(game_build_dir, "work_dir", "pkg", "PIC1.PNG"))
        else:
            pic1_file = open(
                os.path.join(game_build_dir, "work_dir", "pkg", "PIC1.PNG"), "wb"
            )
            pic1_file.write(pic1)
            pic1_file.close()

    if pic2 is not None:
        if platform == "PS3ISO":
            pic2_file = open(
                os.path.join(game_build_dir, "work_dir", "pkg", "PIC2.PNG"), "wb"
            )
            pic2_file.write(pic2)
            pic2_file.close()

    if at3 is not None:
        if platform == "PS3ISO" or platform in {"GAMES", "GAMEZ"}:
            # for .AT3 we need to save the binary data to a file
            at3_file = open(
                os.path.join(game_build_dir, "work_dir", "pkg", "SND0.AT3"), "wb"
            )
            at3_file.write(at3)
            at3_file.close()

    if pam is not None:
        if platform == "PS3ISO" or platform in {"GAMES", "GAMEZ"}:
            # for .PAM we need to save the binary data to a file
            pam_file = open(
                os.path.join(game_build_dir, "work_dir", "pkg", "ICON1.PAM"), "wb"
            )
            pam_file.write(pam)
            pam_file.close()

    # TODO: PMF (310x180)
    # elif platform == 'PSPISO':
    #     # for .PMF we need to save the binary data to a file
    #     pmf_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PMF'), "wb")
    #     pmf_file.write(pam)
    #     pmf_file.close()


def param_sfo_parser(param_data):
    title_id = None
    title = None
    filtered_data_list = list(filter(None, param_data.split(b"\x00")))
    for fd in filtered_data_list:
        id_match = re.search("\w{4}\d{5}$", fd.decode("ISO-8859-1"))
        if id_match:
            title_id = id_match.group()
            try:
                title = str(filtered_data_list[filtered_data_list.index(title_id) - 1])
            except:
                title = None
            break

    return title_id, title
