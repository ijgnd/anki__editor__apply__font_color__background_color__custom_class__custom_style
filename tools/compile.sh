#!/usr/bin/env bash
declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"

rm -f "${DIR}/src/confdialog/forms/"*.py

for filename in "${DIR}/designer/"*'.ui'; do
  pyuic6 "$filename" > "${DIR}/src/confdialog/forms/$(basename ${filename%.*}).py"
done
