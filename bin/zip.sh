declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
declare addon_id='custom_styles'

"$DIR/bin/compile.sh"

cd "$DIR/src"

zip -r "$DIR/build/$addon_id.ankiaddon" \
  *
