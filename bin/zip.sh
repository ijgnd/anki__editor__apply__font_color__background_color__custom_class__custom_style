declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
declare addon_id='persitent_editor'

cd "$DIR"

"$DIR/bin/compile.sh"

zip -r "$DIR/build/$addon_id.ankiaddon" \
  "src/"*
