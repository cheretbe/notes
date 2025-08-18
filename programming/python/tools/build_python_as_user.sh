#!/bin/bash
set -e

# -W|--show [<pattern> ...] Show information on package(s)
# -f changes the format of the output
# db:Status-abbrev contains the abbreviated package status (as three characters),
#   such as "ii " or "iHR" (since dpkg 1.16.2) See the --list command example below
#   for more details.
# So here we are checking for presence of "i" at position 2 of three-char output
if ! dpkg-query -Wf'${db:Status-abbrev}' "build-essential" 2>/dev/null | grep -q '^.i'; then
  echo "build-essential package is not installed"
  echo "It contains too much dependencies to manually download and install them"
  exit 1
fi

# Default Python version (short, e.g. 3.12)
PYTHON_VERSION="3.12"
PYTHON_FULL_VERSION=""

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --python-version|-p)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Fetch latest patch version for the given Python version
wget -q -O - https://endoflife.date/api/python.json | jq -r ".[] | select(.cycle==\"${PYTHON_VERSION}\") | .latest" > /tmp/python_latest_version.txt
PYTHON_FULL_VERSION=$(cat /tmp/python_latest_version.txt)

if [[ -z "$PYTHON_FULL_VERSION" || "$PYTHON_FULL_VERSION" == "null" ]]; then
    echo "Could not determine latest version for Python $PYTHON_VERSION"
    exit 1
fi

PYTHON_SOURCE="Python-${PYTHON_FULL_VERSION}"
INSTALL_DIR="$HOME/.local"
BUILD_DIR="$HOME/pybuild"
SOURCE_DIR="$BUILD_DIR/${PYTHON_SOURCE}"

printf "Installing Python %s to %s\n" "$PYTHON_FULL_VERSION" "$INSTALL_DIR"

# Create build directory
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Download and extract build dependencies
# When adding new *-dev packages, ensure to also download the corresponding runtime package
# (e.g., libssl-dev requires libssl1.1, etc.)
echo "Downloading dependencies..."
for pkg in libssl-dev libssl1.1 libffi-dev libffi7 \
            libdb5.3-dev libdb5.3 libgdbm-dev libgdbm6 \
            libsqlite3-dev libsqlite3-0 libbz2-dev libbz2-1.0 \
            zlib1g-dev zlib1g libexpat1-dev libexpat1 liblzma-dev \
            liblzma5 libreadline-dev pkg-config; do
    apt-get download "$pkg"
    dpkg -x "${pkg}"_*.deb "$BUILD_DIR"
done
# Set environment variables
export PATH="$BUILD_DIR/usr/bin:$PATH"
export CPATH="$BUILD_DIR/usr/include:$BUILD_DIR/usr/include/x86_64-linux-gnu:$CPATH"
export LIBRARY_PATH="$BUILD_DIR/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH"
export LD_LIBRARY_PATH="$BUILD_DIR/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export PKG_CONFIG_PATH="$BUILD_DIR/usr/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS="-L$BUILD_DIR/usr/lib/x86_64-linux-gnu"
export CPPFLAGS="-I$BUILD_DIR/usr/include -I$BUILD_DIR/usr/include/x86_64-linux-gnu"

echo "Downloading Python $PYTHON_FULL_VERSION..."
if [ ! -d "$SOURCE_DIR" ]; then
    wget "https://www.python.org/ftp/python/${PYTHON_FULL_VERSION}/${PYTHON_SOURCE}.tgz"
    tar xzf "${PYTHON_SOURCE}.tgz"
fi
cd "$SOURCE_DIR"

echo "Configuring Python..."
./configure --prefix="$INSTALL_DIR" \
            --with-openssl="$BUILD_DIR/usr" \
            --enable-optimizations \
            LDFLAGS="$LDFLAGS" \
            CPPFLAGS="$CPPFLAGS"

echo "Building Python..."
make -j$(nproc)

echo "Installing Python..."
make altinstall

"$INSTALL_DIR/bin/python${PYTHON_VERSION}" -c "import _ctypes; print('_ctypes module available')"
"$INSTALL_DIR/bin/python${PYTHON_VERSION}" -c "import ssl; print(ssl.OPENSSL_VERSION)"

echo "Cleaning up..."
rm -rf "$BUILD_DIR"

echo -e "\nPython ${PYTHON_FULL_VERSION} successfully installed to ${INSTALL_DIR}"
echo -e "Add to your ~/.bashrc:\nexport PATH=\"${INSTALL_DIR}/bin:\$PATH\""
echo -e "Use command: python${PYTHON_VERSION} to run"
