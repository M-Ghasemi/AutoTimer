import subprocess
import re


def utf8_string(text):
    return text.decode('utf-8') if text and type(text) is bytes else ''


def get_active_window_info():
    active_window = utf8_string(subprocess.run(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE).stdout)
    window_id = re.search(r'^_NET_ACTIVE_WINDOW.* ([\w]+)$', active_window).group(1)

    window_class = utf8_string(subprocess.run(['xprop', '-id', window_id, 'WM_CLASS'], stdout=subprocess.PIPE).stdout)

    window_name = utf8_string(subprocess.run(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE).stdout)

    class_match = re.match(r"WM_CLASS\(\w+\) = (?P<class>.+)$", window_class)
    name_match = re.match(r"WM_NAME\(\w+\) = (?P<name>.+)$", window_name)

    return ' --> '.join([
        class_match.group('class').replace('"', '') if class_match else 'NOCLASS',
        name_match.group("name").replace('"', '') if name_match else 'NONAME'
    ])
