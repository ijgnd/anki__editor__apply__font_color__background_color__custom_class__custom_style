#!/usr/bin/env bash
declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"

rm -f "${DIR}/src/confdialog/forms/"*.py

for filename in "${DIR}/designer/"*'.ui'; do
  python3 -m PyQt5.uic.pyuic -o "${DIR}/src/confdialog/forms5/$(basename ${filename%.*}).py" "$filename"
  python3 -m PyQt6.uic.pyuic -o "${DIR}/src/confdialog/forms6/$(basename ${filename%.*}).py" "$filename"
done
