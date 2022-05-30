#!/usr/bin/env bash
# docker run -ti --rm -v $(pwd):/src/otio-wasm pyodide/pyodide:0.20.0 bash

cd pyodide
# make

mkdir /src/pyodide/packages/opentimelineio
cd /src/pyodide/packages/opentimelineio

echo '
package:
  name: opentimelineio
  version: 0.15.0.dev1

source:
  url: "file:///src/otio-wasm/OpenTimelineIO-0.15.0.dev1.tar.gz"
  sha256: '$(sha256sum /src/otio-wasm/OpenTimelineIO-0.15.0.dev1.tar.gz | cut -d' ' -f1)'
  patches:
  - patches/patch.patch
' > meta.yaml

mkdir /src/pyodide/packages/opentimelineio/patches
cp /src/otio-wasm/patch.patch /src/pyodide/packages/opentimelineio/patches

python -m pyodide_build buildpkg meta.yaml
