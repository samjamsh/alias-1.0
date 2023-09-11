def restore_envpath():
    username = getlogin()
    with open(f"/home/{username}/alias" + "/etc/environment_backup", "r") as backup:
        backup_data = backup.read()
    try:
        with open("/etc/environment", 'w') as env_file:
            env_file.write(backup_data)
        print("env path restored")

    except PermissionError:

        print(backup_data)
        print("you don't have permission to restore env path")


def creates_alias_envpath():
    try:
        user_home = 'home'
        username = getlogin()
        program_dir = "alias"

        path = "/" + user_home + "/" + username + "/" + program_dir

        makedirs(path + "/bin")
        makedirs(path + "/etc")

        return path + "/bin"

    except:
        print("bin and etc already exists")
        return path + "/bin"


def backup_path_env(env_path):

    def backup_original(username):
        with open("/etc/environment", "r") as original:
            original_envpath = original.read()
            try:
                with open(f"/home/{username}/alias" + "/etc/environment_backup", "r") as backup:
                    data = backup.read()
                    print("backup already exists")

            except FileNotFoundError:
                with open(f"/home/{username}/alias" + "/etc/environment_backup", "w") as backup:
                    backup.write(original_envpath)
                    print("backup created")

    username = getlogin()
    backup_original(username)


def env_update(env_path, dir_loc):
    def read(filename):
        with open(filename, "r") as file:
            data = file.readlines()
            return data

    lines = read(env_path)
    new_lines = ''

    for line in lines:
        if 'PATH=' in line[:5] and dir_loc not in line:
            new_line = line[:-1] + ":" + dir_loc + '\n'
            line = new_line
            new_lines += line

        elif 'PATH=' in line[:5] and dir_loc in line:
            print("env path already updated"); return 0

        else:
            new_lines += line


    print(new_lines, end='')
    org = open(env_path, "r").readlines();
    try:
        with open(env_path, "w") as file:
            file.write(new_lines)
        print("env path updated")
    except PermissionError:
        print("you do not have permission to modify the env path")


def operating_sys():
    if os == 'linux':
        pass
    else:
        exit("operational system error: this program was written just to work on linux systems")



from os import system as shell, getlogin, makedirs, unlink, chmod, listdir
from sys import platform as os, argv as arg

operating_sys()

def get_os_binpath():
    username = getlogin()
    path = "/home/" + username + "/alias/bin"

    linux = os == 'linux'
    ios = os == 'darwin'

    if linux == True:
        return path

    elif ios == True:
               '/private/var/mobile/Containers/Shared/AppGroup/1DAE09F2-6240-4B36-8B6D-E3890D78B3E1/Documents'
               '~/Library/bin'
               '/private/var/mobile/Containers/Data/Application/3AF3FE01-2CCE-4E07-A778-AF60422816AB/Library' 
               '/private/var/mobile/Containers/Data/Application/3AF3FE01-2CCE-4E07-A778-AF60422816AB/Documents'

    else:
        exit("operational system error")



def terminal_session():
    shell(f". /etc/environment")
    print("path environment updated on current terminal session")


def user_permanent():

    def get_bashrc():
        user = getlogin()
        path = f"/home/{user}/.bashrc"

        with open(path, "rt") as file:
            file_content = file.read()
            return file_content, path


    def update_bashrc(path, data):
        with open(path, "wt") as file:
            file.write(data)
        print(".bashrc updated")

    original_bashrc, path = get_bashrc()

    new_data = f"\n. /etc/environment"

    data = original_bashrc + new_data

    exists = new_data in original_bashrc or new_data + "\n" in original_bashrc

    if exists == True:
        print("source /etc/environment is already in bashrc")
    else:
        update_bashrc(path, data)

def delete_alias(alias_name):
    try:
        path = "/home/%s/alias/bin" %(getlogin())
        aliases = listdir(path)
        valid = alias_name in aliases
        if valid is True:
            alias = path + "/" + alias_name
            unlink(alias)
        else:
            exit("the given alias name does not exists or is invalid")

    except Exception as error:
        print(error)
        exit("try running python3 %s update-envpath " %(arg[0]))

def show_aliases():
    try:
        id = 0
        path = "/home/%s/alias/bin" %(getlogin())
        aliases = listdir(path)
        print("there's %i aliases" %(len(aliases)))
        for alias in aliases:
            id+=1
            print("%s %s" %(id, alias))
    except Exception as error:
        print(error)
        exit("try running python3 %s update-envpath " %(arg[0]))

def create(new_alias, target, bin_path, mode):
    try:
        def move(filename, bin_path):
            with open(filename, "rb") as file:
                file_bytes = file.read()

            filename = f"/{new_alias}"
            with open(bin_path + filename, "wb") as file:
                file.write(file_bytes)

            chmod(bin_path + filename, 0o755)


        code = """#include <stdio.h>\n#include <stdlib.h>\nint main(void){ system("%s"); return 0;}
 """ %(target)

        with open(new_alias + '.c', "w") as file:
            file.write(code)

        shell(f"gcc {new_alias + '.c'} -o {new_alias}")

        move(new_alias, bin_path)

        unlink(new_alias + '.c')

        unlink(new_alias)

    except FileNotFoundError:
        exit(f"try running python3 {arg[0]} update-envpath")


    finally:
        if mode == "ts":
            terminal_session()
            print("terminal session mode enabled")
        elif mode == "pu":
            user_permanent()
            print("user permanent mode enabled")


def params():
    parameters = len(arg) - 1
    parameter = arg
    help_msg = """AMT (Alias Managment Tool) version 1.0, created by samjamsh the cyb3rguy
usage: python3 %s command-name alias-name [option] {value}

options:
        update-envpath  - update system environment path
        list-alias      - lists or shows aliases
        restore-envpath - restore system environment path to original content
        remove          - removes or deletes an alias
        -p : permanent  ( updates the system environment path and restarts the computer)
        -pu : permanent user ( updates system environment path only for current user)
        -ts : terminal session ( updates system environment path in current terminal session only)

examples: python3 %s command alias   -   creates a new alias to command
          python3 %s remove alias    -   deletes alias
""" %(arg[0], arg[0], arg[0])


    help = f"use: python3 {parameter[0]} program_name alias_name"

    if parameters == 2:
        if parameter[1] == 'remove':
            target = parameter[2]
            delete_alias(target);
            exit("alias %s was deleted" %(target))
        else:
            target = parameter[1]
            alias = parameter[2]
            return target, alias, None


    elif parameters == 3:
        if parameter[3] == "-ts":
            target = parameter[1]
            alias = parameter[2]
            return target, alias, "ts"

        elif parameter[3] == "-us":
            exit("option reserved to future")

        elif parameter[3] == "-pu":
            target = parameter[1]
            alias = parameter[2]
            return target, alias, "pu"

        elif parameter[3] == "-p":
            environment_path = "/etc/environment"
            directory = creates_alias_envpath()
            env_update(environment_path, directory)
            backup_path_env(environment_path)
            shell("reboot")
            exit()
        else:
            exit("option error: choice -ts, -us, or -p!")

    elif parameters == 1:
        if parameter[1] == "restore-envpath":
            print("this option requires super user privileges or sudo power")
            restore_envpath(); exit()

        elif parameter[1] == "--help" or parameter[1] == "-h":
            exit(help_msg)

        elif parameter[1] == "update-envpath":
            environment_path = "/etc/environment"
            directory = creates_alias_envpath()
            env_update(environment_path, directory)
            backup_path_env(environment_path)
            exit()

        elif parameter[1] == "list-alias":
            show_aliases(); exit()

        else:
            exit("invalid program managment option")

    else:
        exit(help)


bin_path = get_os_binpath()
target_program, alias_name, option = params()
create(alias_name, target_program, bin_path, option)
                                                     
