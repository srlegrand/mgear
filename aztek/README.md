# mGear for Aztek

mGear's plug-ins built with [Aztek](https://github.com/srlegrand/Aztek)'s plug-in kit, packed with mGear's scripts and
icons as a module. Aztek installs it from Help > Install mGear, into the user folder chosen at its first start
(`~/aztek` or a Maya user folder), under `modules/`:

    aztek-mGear.mod
    mGear-aztek/scripts, icons, plug-ins

The definition's block is for `MAYAVERSION:aztek`: Maya passes over it, and Aztek takes it before a Maya build of mGear
in the same modules folder.

## Plug-ins

- `mgear_solvers`: `../src`, unchanged.
- `mGearWeightDriver`: `weightDriver/`, the `source/` folder of https://github.com/mgear-dev/mgear_weightDriver (3.6.3,
  commit 65a0133), unchanged; its CMakeLists.txt left out. Licence: MIT, `weightDriver/LICENSE`.
- `cvwrap`: `cvwrap/`, the `src/` folder of https://github.com/mgear-dev/cvwrap (commit 882469a), unchanged; its
  CMakeLists.txt left out. Licence: MIT, `cvwrap/LICENSE`.
- `weightDriver`: `weightDriver-legacy/`, Ingo Clemens' weightDriver 3.6.1 before mGear renamed it (the `source/`
  folder of https://github.com/mgear-dev/mgear_weightDriver at commit ca1fb04, with the module's scripts and icons),
  unchanged. Rigs made with mGear 4 use its `weightDriver` node. Licence: MIT, `weightDriver-legacy/LICENSE`.

## Building

    cmake -S aztek -B build-aztek -DAZTEK_DEVKIT=/path/to/Aztek/devkit -DCMAKE_BUILD_TYPE=Release
    cmake --build build-aztek --config Release
    python aztek/package.py --plugins build-aztek/plug-ins --devkit /path/to/Aztek/devkit --platform linux-x64

## Releases

The Aztek release workflow (Actions > Aztek release > Run workflow) builds Linux, Windows and macOS against the Aztek
commit given and publishes `v<mGear version>-aztek-abi<N>` with one zip a platform:
`mgear-5.4.8-aztek-abi3-linux-x64.zip`, `...-windows-x64.zip`, `...-macos.zip`. A plug-in works with every Aztek of the
same plug-in ABI (`AZTEK_ABI_VERSION` in Aztek's `devkit/include/aztek/abi.h`).
