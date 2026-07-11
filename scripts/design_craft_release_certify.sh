#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

MODE="${1:-certify}"
if [[ "${MODE}" != "certify" && "${MODE}" != "tag" ]]; then
  echo "Usage: scripts/design_craft_release_certify.sh [certify|tag]" >&2
  exit 2
fi

GIT_DIR="$(git rev-parse --absolute-git-dir)"
LOCK_DIR="${GIT_DIR}/design-craft-release.lock"
LOCK_HELD=0

cleanup() {
  if [[ "${LOCK_HELD}" == "1" ]]; then
    rm -f "${LOCK_DIR}/pid" "${LOCK_DIR}/head"
    rmdir "${LOCK_DIR}" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

acquire_lock() {
  if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
    local owner=""
    if [[ -f "${LOCK_DIR}/pid" ]]; then
      owner="$(sed -n '1p' "${LOCK_DIR}/pid" 2>/dev/null || true)"
    fi
    if [[ "${owner}" =~ ^[0-9]+$ ]] && ! kill -0 "${owner}" 2>/dev/null; then
      rm -f "${LOCK_DIR}/pid" "${LOCK_DIR}/head"
      rmdir "${LOCK_DIR}" 2>/dev/null || true
      mkdir "${LOCK_DIR}"
    else
      echo "Another release certification owns ${LOCK_DIR} (pid=${owner:-unknown})" >&2
      exit 1
    fi
  fi
  printf '%s\n' "$$" > "${LOCK_DIR}/pid"
  git rev-parse HEAD > "${LOCK_DIR}/head"
  LOCK_HELD=1
}

assert_stable_repository() {
  local expected_head="$1"
  local observed_head
  observed_head="$(git rev-parse HEAD)"
  if [[ "${observed_head}" != "${expected_head}" ]]; then
    echo "Repository HEAD changed during release certification:" >&2
    echo "  expected: ${expected_head}" >&2
    echo "  observed: ${observed_head}" >&2
    exit 1
  fi
  if [[ -n "$(git status --porcelain=v1 --untracked-files=all)" ]]; then
    echo "Repository became dirty during release certification" >&2
    exit 1
  fi
}

acquire_lock
START_HEAD="$(git rev-parse HEAD)"
assert_stable_repository "${START_HEAD}"

make release-certify-prepublish
assert_stable_repository "${START_HEAD}"

make release-certify-publish
assert_stable_repository "${START_HEAD}"

if [[ "${MODE}" == "tag" ]]; then
  python3 scripts/design_craft_release_verify.py \
    --certify \
    --require-tag \
    --require-remote
  python3 scripts/design_craft_github_checks.py --require-tag-run
  assert_stable_repository "${START_HEAD}"
fi

echo "design-craft release ${MODE} verified at ${START_HEAD}"
