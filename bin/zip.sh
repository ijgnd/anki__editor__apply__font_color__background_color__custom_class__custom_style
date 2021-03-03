declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
declare addon_id='custom_styles'

"$DIR/bin/compile.sh"

cd "$DIR/src"

zip -r "$DIR/build/$addon_id.ankiaddon" \
  *".py" \
  "LICENSE" \
  "manifest.json" \
  "confdialog/"*".py" \
  "confdialog/forms/"*".py" \
  "web/"*".js" \
  "webview/"*".py" \
  "editor/"*".py" \
  "icons/"*
