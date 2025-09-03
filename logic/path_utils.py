import os
import ctypes
import winreg

def get_env_variable(name, scope="user"):
    """環境変数を取得（user/system）"""
    if scope == "system":
        root = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    else:
        root = winreg.HKEY_CURRENT_USER
        subkey = r"Environment"

    try:
        with winreg.OpenKey(root, subkey) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        return ""


def set_env_variable(name, value, scope="user"):
    """環境変数を設定（user/system）"""
    if scope == "system":
        root = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    else:
        root = winreg.HKEY_CURRENT_USER
        subkey = r"Environment"

    with winreg.OpenKey(root, subkey, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)

    # 環境変数の即時反映
    send_message = 0x1A
    ctypes.windll.user32.SendMessageW(0xFFFF, send_message, 0, "Environment")


def path_exists(path):
    """指定パスが存在するか確認"""
    return os.path.exists(path)
