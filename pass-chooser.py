import os
import fnmatch
import subprocess

pass_path = os.path.join(os.path.expanduser("~/.password-store"), '')


def get_secrets():

    secret_list = []

    for path, directories, file_names in os.walk(pass_path, followlinks=True):

        secrets = fnmatch.filter(file_names, '*.gpg')

        if not secrets:
            continue
        
        for secret in secrets:
            secret_list.append(os.path.join(path[len(pass_path):], secret[:-4]))

    return secret_list

secrets = get_secrets()
process = subprocess.run(["yofi", "--quiet", "--config-file", "/home/zoe/.config/yofi/password.conf", "dialog"], input='\n'.join(secrets).encode("UTF-8"), stdout=subprocess.PIPE)

selected_secret = process.stdout.decode("UTF-8").strip()

pass_command = ["pass", "-c", selected_secret]
if selected_secret.endswith("/otp"):
    pass_command.insert(1, "otp")

process = subprocess.run(pass_command)