#!/bin/sh
os_name="$(uname -s)"
case "$os_name" in
  Linux*) echo "Detected Linux" ;;
  Darwin*) echo "Detected macOS" ;;
  CYGWIN*|MINGW*|MSYS*) echo "Detected Windows" ;;
  *) echo "Unknown OS: $os_name" ;;
esac
