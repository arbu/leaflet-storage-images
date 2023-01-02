#! /usr/bin/env bash
set -eu -o pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

FAILED=0
FAILED_VERSIONS=""

runtest() {
  echo >&2 "Running with Python $1, Django $2 and Pillow $3"
  if ! docker run --rm "$(docker build -q -f Dockerfile \
      --build-arg PYTHON_VERSION="$1" \
      --build-arg DJANGO_VERSION="$2" \
      --build-arg PILLOW_VERSION="$3" \
      ..)"; then
        FAILED=1
        FAILED_VERSIONS="$FAILED_VERSIONS\nPython $1, Django $2, Pillow $3"
  fi
}


#          Python      Django          Pillow        # Distribution
runtest    3.7         ""              ""            # latest from pip
runtest    3.8         ""              ""            # latest from pip
runtest    3.9         ""              ""            # latest from pip
runtest    3.10        ""              ""            # latest from pip
runtest    3.11        ""              ""            # latest from pip
runtest    3.8         ~=2.2.12        ~=7.0.0       # Ubuntu focal
runtest    3.10        ~=3.2.12        ~=9.0.1       # Ubuntu jammy
runtest    3.10        ~=3.2.15        ~=9.2.0       # Ubuntu kinetic + lunar
runtest    3.7         ~=2.2.24        ~=5.4.1       # Debian buster-backports
runtest    3.9         ~=2.2.28        ~=8.1.2       # Debian bullseye
runtest    3.9         ~=3.2.12        ~=8.1.2       # Debian bullseye-backports
runtest    3.10        ~=3.2.16        ~=9.3.0       # Debian bookworm
runtest    3.9         ~=2.2.24        ~=5.1.0       # RHEL 8
runtest    3.9         ~=3.2.15        ~=5.1.0       # RHEL 8 / python-django3
runtest    3.9         ~=3.1.13        ~=8.2.0       # Alpine 3.14
runtest    3.9         ~=3.1.13        ~=8.4.0       # Alpine 3.15
runtest    3.10        ~=3.2.16        ~=9.1.1       # Alpine 3.16
runtest    3.10        ~=3.2.16        ~=9.3.0       # Alpine 3.17


if [[ $FAILED == 1 ]]; then
  echo >&2 "Some tests failed; affected versions:$FAILED_VERSIONS"
  exit 1
else
  echo >&2 "All tests passed!"
fi