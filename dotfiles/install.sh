SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$SCRIPT_DIR"/git/config_identity-template ~/.gitconfig
cp "$SCRIPT_DIR"/tmux/conf ~/.tmux.conf

echo "Don't forget to set your email address in ~/.gitconfig if this is a company env!"
