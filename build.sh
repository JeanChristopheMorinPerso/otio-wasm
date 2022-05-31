#!/usr/bin/env bash
# docker run -ti --rm -v $(pwd):/src/otio-wasm pyodide/pyodide:0.20.0 bash

repoPath="$1"
if [[ repoPath == "" ]]; then
    echo "You need to specify the path to the repo"
    exit 1
fi

cd /src/pyodide

mkdir /src/pyodide/packages/opentimelineio
cd /src/pyodide/packages/opentimelineio

echo '
package:
  name: opentimelineio
  version: 0.15.0.dev1

source:
  url: "file://'"$repoPath"'/OpenTimelineIO-0.15.0.dev1.tar.gz"
  sha256: '$(sha256sum "$repoPath/OpenTimelineIO-0.15.0.dev1.tar.gz" | cut -d' ' -f1)'
  patches:
  - patches/patch.patch
' > meta.yaml

mkdir /src/pyodide/packages/opentimelineio/patches
cp "$repoPath/patch.patch" /src/pyodide/packages/opentimelineio/patches/

cat /src/pyodide/packages/opentimelineio/meta.yaml

python -m pyodide_build buildpkg meta.yaml
