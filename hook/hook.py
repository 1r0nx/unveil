import os
import stat


def post_safe_import_module(api):
    base = api.application.binaries[0][1]

    for root, dirs, files in os.walk(base):
        for name in files:
            path = os.path.join(root, name)
            try:
                st = os.stat(path)
                os.chmod(path, st.st_mode | stat.S_IEXEC)
            except Exception as e:
                print(f"[chmod hook] Failed on {path}: {e}")
