#!/usr/bin/env bash
declare DIR="$(cd "$(dirname "$0")/" && pwd -P)"

mkdir -p "${DIR}/src/forms"
rm -f "${DIR}/src/forms/"*.py

for filename in "${DIR}/designer/"*'.ui'; do
  pyuic5 "$filename" > "${DIR}/src/forms/$(basename ${filename%.*}).py"
done
