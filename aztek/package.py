"""Packs mGear for Aztek: its scripts and icons, and the plug-ins built with Aztek's kit, as a module.

    python aztek/package.py --plugins build-aztek/plug-ins --devkit /path/to/Aztek/devkit --platform linux-x64 --out dist

The zip holds the module's definition and its folder, to unpack into a user folder's modules folder:

    aztek-mGear.mod
    mGear-aztek/scripts, icons, plug-ins

The definition's block is for MAYAVERSION:aztek, so Maya passes over it when both read the same modules folder, and
Aztek takes it before Maya's own mGear.mod there. Its name says the mGear version, the plug-in ABI of the kit it was
built with, and the platform: mgear-5.4.8-aztek-abi3-linux-x64.zip.
"""

import argparse
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODULE = "mGear-aztek"


def mgear_version():
    with open(os.path.join(ROOT, "release", "scripts", "mgear", "__init__.py")) as f:
        m = re.search(r"^VERSION\s*=\s*\[(\d+),\s*(\d+),\s*(\d+)\]", f.read(), re.M)
    return ".".join(m.groups())


def abi_version(devkit):
    with open(os.path.join(devkit, "include", "aztek", "abi.h")) as f:
        return re.search(r"#define\s+AZTEK_ABI_VERSION\s+(\d+)", f.read()).group(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plugins", required=True, help="the build's plug-ins folder")
    p.add_argument("--devkit", required=True, help="Aztek's devkit folder the plug-ins were built with")
    p.add_argument("--platform", required=True, help="linux-x64, windows-x64 or macos")
    p.add_argument("--out", default="dist")
    a = p.parse_args()

    version = mgear_version()
    abi = abi_version(a.devkit)
    name = "mgear-%s-aztek-abi%s-%s" % (version, abi, a.platform)
    stage = os.path.join(a.out, name)
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    folder = os.path.join(stage, MODULE)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.afdesign")
    shutil.copytree(os.path.join(ROOT, "release", "scripts"), os.path.join(folder, "scripts"), ignore=ignore)
    shutil.copytree(os.path.join(ROOT, "release", "icons"), os.path.join(folder, "icons"), ignore=ignore)
    # weightDriver 3.6.1's own scripts and icons, for rigs made with mGear 4.
    legacy = os.path.join(HERE, "weightDriver-legacy")
    for sub in ("scripts", "icons"):
        for f in sorted(os.listdir(os.path.join(legacy, sub))):
            shutil.copy2(os.path.join(legacy, sub, f), os.path.join(folder, sub, f))
    plugins = os.path.join(folder, "plug-ins")
    os.makedirs(plugins)
    built = [f for f in sorted(os.listdir(a.plugins)) if os.path.splitext(f)[1] in (".so", ".dll", ".bundle")]
    if not built:
        sys.exit("no plug-ins in " + a.plugins)
    for f in built:
        shutil.copy2(os.path.join(a.plugins, f), plugins)
    with open(os.path.join(stage, "aztek-mGear.mod"), "w", newline="\n") as f:
        f.write("+ MAYAVERSION:aztek mGear %s ./%s\n" % (version, MODULE))

    zip_path = os.path.join(a.out, name + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(stage):
            for f in files:
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, stage).replace(os.sep, "/"))
    shutil.rmtree(stage)
    print(zip_path)


if __name__ == "__main__":
    main()
