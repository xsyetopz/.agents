#!/usr/bin/env bash
# Run the catalog's package-contract checks in disposable Linux containers.
#
# The default lane is static-only.  `--codex` explicitly opts into the
# behavioral lane; it never mounts host Codex state or credentials, and marks
# authentication/network failures UNVERIFIED rather than treating them as a
# behavior pass.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly SCRIPT_DIR REPO_ROOT
readonly DEFAULT_EVIDENCE_ROOT="/tmp/skizzles-orchestration/skill-standard-20260813/evidence"
readonly DEFAULT_IMAGE="xsyetopz/codex-evaluator:0.147.0"
readonly LABEL_KEY="com.xsyetopz.skill-evaluator"

MODE="static"
IMAGE="$DEFAULT_IMAGE"
EVIDENCE_ROOT="$DEFAULT_EVIDENCE_ROOT"
CODEX_NETWORK="none"
CODEX_TIMEOUT=30
BUILD_IMAGE=1
PACKAGES=()
RUN_ID=""
RUN_DIR=""
CID_DIR=""
EXIT_STATUS=0

usage() {
    cat <<'USAGE'
Usage: evals/run_container_eval.sh [OPTIONS]

Run every catalog package's checks in disposable Linux containers. The default
--static-only lane runs each package's actual scripts/check.py and parses
evals/evals.json. --codex runs that lane first, probes the exact in-image
`codex exec --help`, and then runs each declared case. It never mounts host
credentials or Codex state; auth/network failures are UNVERIFIED.

Options:
  --static-only             Run static checks only (the default).
  --codex                   Run static checks, then the Codex case lane.
  --package NAME            Select one package (repeat; default: all 12).
  --all                     Select all catalog packages explicitly.
  --evidence-dir DIR        Evidence root (default: /tmp/.../evidence).
  --image IMAGE             Use an existing evaluator image; implies --no-build.
  --no-build                Do not build the pinned Dockerfile image.
  --build                   Build the pinned image before running (default).
  --codex-network NETWORK   Codex network: none (default) or bridge only.
  --codex-timeout SECONDS   Per-case limit (default: 30; range: 1..600).
  --help                    Show this help and exit.

The image is defined by docker/Dockerfile.codex-evaluator. It pins a Linux
base-image digest and installs the real @openai/codex npm package. Every run
uses docker run --rm, a scoped label, a read-only root, a non-root UID,
cap-drop-all, no-new-privileges, synthetic HOME/CODEX_HOME, and no host
credential/SSH/socket/global-skill mounts. Evidence is written outside this
checkout under --evidence-dir/<run-id>/.

Exit status:
  0  all requested static checks pass; Codex cases may be UNVERIFIED.
  1  a static check, safety invariant, or cleanup proof failed.
  2  Docker/daemon/image preflight was unavailable (exact blocker is recorded).
USAGE
}

die_usage() {
    printf 'error: %s\n\n' "$1" >&2
    usage >&2
    exit 2
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --static-only) MODE="static"; shift ;;
        --codex) MODE="codex"; shift ;;
        --package)
            [[ $# -ge 2 ]] || die_usage "--package requires a name"
            PACKAGES+=("$2")
            shift 2
            ;;
        --all) PACKAGES=(); shift ;;
        --evidence-dir)
            [[ $# -ge 2 ]] || die_usage "--evidence-dir requires a directory"
            EVIDENCE_ROOT="$2"
            shift 2
            ;;
        --image)
            [[ $# -ge 2 ]] || die_usage "--image requires a tag or digest"
            IMAGE="$2"
            BUILD_IMAGE=0
            shift 2
            ;;
        --no-build) BUILD_IMAGE=0; shift ;;
        --build) BUILD_IMAGE=1; shift ;;
        --codex-network)
            [[ $# -ge 2 ]] || die_usage "--codex-network requires none or bridge"
            CODEX_NETWORK="$2"
            shift 2
            ;;
        --codex-timeout)
            [[ $# -ge 2 ]] || die_usage "--codex-timeout requires seconds"
            CODEX_TIMEOUT="$2"
            shift 2
            ;;
        --help|-h) usage; exit 0 ;;
        *) die_usage "unknown option: $1" ;;
    esac
done

if [[ "$CODEX_NETWORK" != "none" && "$CODEX_NETWORK" != "bridge" ]]; then
    die_usage "--codex-network must be none or bridge (host networking is forbidden)"
fi
if ! [[ "$CODEX_TIMEOUT" =~ ^[0-9]+$ ]] || [[ "$CODEX_TIMEOUT" -lt 1 || "$CODEX_TIMEOUT" -gt 600 ]]; then
    die_usage "--codex-timeout must be an integer from 1 to 600"
fi

if [[ -z "$RUN_ID" ]]; then
    RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
fi
RUN_DIR="${EVIDENCE_ROOT}/${RUN_ID}"
CID_DIR="${RUN_DIR}/cids"
mkdir -p "$CID_DIR" || {
    printf 'error: cannot create evidence directory: %s\n' "$RUN_DIR" >&2
    exit 2
}
chmod 0755 "$RUN_DIR" "$CID_DIR" 2>/dev/null || true

readonly LABEL_VALUE="$RUN_ID"
readonly LABEL_FILTER="${LABEL_KEY}=${LABEL_VALUE}"

cleanup() {
    local prior_status=$?
    set +e
    trap - EXIT INT TERM

    # A cidfile is retained until the wrapper removes it. `--rm` should make
    # these IDs disappear on normal completion; rm -f is for interrupts.
    if [[ -d "$CID_DIR" ]]; then
        while IFS= read -r cidfile; do
            [[ -s "$cidfile" ]] || continue
            cid="$(cat "$cidfile" 2>/dev/null)"
            [[ -n "$cid" ]] && docker rm -f "$cid" >/dev/null 2>&1 || true
            rm -f "$cidfile"
        done < <(find "$CID_DIR" -type f -name '*.cid' -print 2>/dev/null)
    fi

    remaining_containers="$(docker ps -a --filter "label=${LABEL_FILTER}" --format '{{.ID}} {{.Status}} {{.Names}}' 2>&1)"
    containers_rc=$?
    remaining_volumes="$(docker volume ls --filter "label=${LABEL_FILTER}" --format '{{.Name}}' 2>&1)"
    volumes_rc=$?
    {
        printf 'cleanup label: %s\n' "$LABEL_FILTER"
        printf 'containers_remaining (exit=%s):\n%s\n' "$containers_rc" "$remaining_containers"
        printf 'volumes_remaining (exit=%s):\n%s\n' "$volumes_rc" "$remaining_volumes"
    } >"${RUN_DIR}/cleanup-proof.txt" 2>&1

    if [[ "$containers_rc" -ne 0 || "$volumes_rc" -ne 0 ]]; then
        printf 'CLEANUP_UNVERIFIED: scoped resource inspection failed; no cleanup pass claimed\n' >>"${RUN_DIR}/cleanup-proof.txt"
        [[ "$prior_status" -eq 0 ]] && prior_status=1
    elif [[ -n "$remaining_containers" || -n "$remaining_volumes" ]]; then
        printf 'FAIL: labelled resources survived cleanup\n' >>"${RUN_DIR}/cleanup-proof.txt"
        [[ "$prior_status" -eq 0 ]] && prior_status=1
    else
        printf 'CLEANUP_PASS: no labelled containers or volumes remain\n' >>"${RUN_DIR}/cleanup-proof.txt"
    fi
    EXIT_STATUS="$prior_status"
    exit "$prior_status"
}
trap cleanup EXIT INT TERM

capture_split() {
    local name="$1"
    shift
    {
        printf '$'
        printf ' %q' "$@"
        printf '\n'
    } >"${RUN_DIR}/${name}.command.txt"
    "$@" >"${RUN_DIR}/${name}.stdout" 2>"${RUN_DIR}/${name}.stderr"
    local rc=$?
    printf 'exit=%s\n' "$rc" >>"${RUN_DIR}/${name}.command.txt"
    return "$rc"
}

printf 'run_id=%s\nmode=%s\nimage=%s\nnetwork=%s\ncodex_timeout=%s\nevidence=%s\n' \
    "$RUN_ID" "$MODE" "$IMAGE" "$CODEX_NETWORK" "$CODEX_TIMEOUT" "$RUN_DIR" >"${RUN_DIR}/run-metadata.txt"

# Host preflight is always recorded, even when the Docker daemon is blocked.
{
    printf '== which codex ==\n'
    command -v codex
    printf '== codex --version ==\n'
    codex --version
    printf '== docker --version ==\n'
    docker --version
    printf '== docker compose version ==\n'
    docker compose version
    printf '== docker info (OrbStack/daemon) ==\n'
    docker info --format '{{.ServerVersion}} {{.OperatingSystem}}'
    printf '== orbctl version ==\n'
    if command -v orbctl >/dev/null 2>&1; then orbctl version; else printf 'orbctl: unavailable\n'; fi
} >"${RUN_DIR}/preflight.txt" 2>&1

if ! command -v docker >/dev/null 2>&1; then
    printf 'BLOCKED: docker executable is unavailable\n' | tee "${RUN_DIR}/blocker.txt" >&2
    exit 2
fi
if ! docker info >/dev/null 2>"${RUN_DIR}/docker-info-blocker.txt"; then
    printf 'BLOCKED: Docker daemon/OrbStack unavailable; see docker-info-blocker.txt\n' | tee "${RUN_DIR}/blocker.txt" >&2
    exit 2
fi

if [[ "$BUILD_IMAGE" -eq 1 ]]; then
    if ! capture_split image-build docker build --pull --file "$REPO_ROOT/docker/Dockerfile.codex-evaluator" --tag "$IMAGE" "$REPO_ROOT"; then
        printf 'BLOCKED: evaluator image build failed; see image-build.stdout/stderr\n' | tee "${RUN_DIR}/blocker.txt" >&2
        exit 2
    fi
fi

if ! docker image inspect "$IMAGE" >"${RUN_DIR}/image-inspect.json" 2>"${RUN_DIR}/image-inspect.stderr"; then
    printf 'BLOCKED: evaluator image is unavailable: %s\n' "$IMAGE" | tee "${RUN_DIR}/blocker.txt" >&2
    exit 2
fi
docker image inspect "$IMAGE" --format 'image={{.RepoTags}}\nid={{.Id}}\nrepo_digests={{json .RepoDigests}}\n' \
    >"${RUN_DIR}/image-digest.txt" 2>"${RUN_DIR}/image-digest.stderr" || true

ALL_PACKAGES=()
while IFS= read -r package_dir; do
    ALL_PACKAGES+=("$(basename "$package_dir")")
done < <(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d -print | sort)

if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    PACKAGES=("${ALL_PACKAGES[@]}")
fi
if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    printf 'FAIL: no skills packages found\n' >&2
    exit 1
fi
for package in "${PACKAGES[@]}"; do
    found=0
    for known in "${ALL_PACKAGES[@]}"; do
        [[ "$package" == "$known" ]] && found=1
    done
    if [[ "$found" -eq 0 ]]; then
        printf 'error: unknown package: %s\n' "$package" >&2
        exit 2
    fi
done

run_container() {
    local name="$1"
    local package="$2"
    local command="$3"
    local output_dir="${RUN_DIR}/${name}"
    local cidfile="${CID_DIR}/${name}.cid"
    mkdir -p "$output_dir"
    # The evaluator UID is intentionally non-root. This directory is an
    # explicit disposable output target, not a source or credential mount.
    chmod 0777 "$output_dir"
    local package_mount="$REPO_ROOT/skills/${package}"
    local container_network="none"
    docker run --rm --entrypoint /bin/sh \
        --cidfile "$cidfile" \
        --label "${LABEL_KEY}=${LABEL_VALUE}" \
        --label "${LABEL_KEY}.package=${package}" \
        --label "${LABEL_KEY}.mode=${MODE}" \
        --read-only --user 10001:10001 --cap-drop=ALL \
        --security-opt no-new-privileges --network "$container_network" \
        --tmpfs /tmp:rw,noexec,nosuid,nodev,size=256m \
        --tmpfs /tmp/home:rw,noexec,nosuid,nodev,size=32m \
        --tmpfs /tmp/codex-home:rw,noexec,nosuid,nodev,size=32m \
        --env HOME=/tmp/home --env CODEX_HOME=/tmp/codex-home \
        --env XDG_CONFIG_HOME=/tmp/home/.config --env PYTHONDONTWRITEBYTECODE=1 \
        --volume "${package_mount}:/work/package/${package}:ro" \
        --volume "${output_dir}:/work/out:rw" \
        --workdir /work "$IMAGE" -ceu "$command" \
        >"${output_dir}/stdout" 2>"${output_dir}/stderr"
    local rc=$?
    printf '%s\n' "$rc" >"${output_dir}/exit-code"
    printf 'package=%s\nmode=%s\nnetwork=%s\nrequested_codex_network=%s\nread_only_root=true\nuser=10001:10001\ncap_drop=ALL\nno_new_privileges=true\nsource_mount=/work/package/%s:ro\ncodex_timeout=%ss\ncredentials_mounts=none\nssh_mounts=none\nsocket_mounts=none\n' \
        "$package" "$MODE" "$container_network" "$CODEX_NETWORK" "$package" "$CODEX_TIMEOUT" >"${output_dir}/isolation.txt"
    return "$rc"
}

static_failures=0
for package in "${PACKAGES[@]}"; do
    static_command="cd /work/package/${package} && test -f scripts/check.py && python3 scripts/check.py && python3 -m json.tool evals/evals.json >/dev/null"
    if ! run_container "static-${package}" "$package" "$static_command"; then
        static_failures=$((static_failures + 1))
        printf 'FAIL static %s\n' "$package" | tee -a "${RUN_DIR}/summary.txt" >&2
    else
        printf 'PASS static %s\n' "$package" | tee -a "${RUN_DIR}/summary.txt"
    fi
done

if [[ "$static_failures" -ne 0 ]]; then
    printf 'FAIL: %s static package check(s) failed; Codex lane is blocked\n' "$static_failures" | tee -a "${RUN_DIR}/summary.txt" >&2
    exit 1
fi

if [[ "$MODE" == "codex" ]]; then
    # Probe this exact image before any prompt invocation. The probe output is
    # retained as evidence and is not satisfied by the host's Codex binary.
    probe_dir="${RUN_DIR}/codex-probe"
    mkdir -p "$probe_dir"
    chmod 0777 "$probe_dir"
    docker run --rm --entrypoint /bin/sh \
        --cidfile "${CID_DIR}/codex-probe.cid" \
        --label "${LABEL_KEY}=${LABEL_VALUE}" --label "${LABEL_KEY}.mode=probe" \
        --read-only --user 10001:10001 --cap-drop=ALL \
        --security-opt no-new-privileges --network none \
        --tmpfs /tmp:rw,noexec,nosuid,nodev,size=256m \
        --tmpfs /tmp/home:rw,noexec,nosuid,nodev,size=32m \
        --tmpfs /tmp/codex-home:rw,noexec,nosuid,nodev,size=32m \
        --env HOME=/tmp/home --env CODEX_HOME=/tmp/codex-home \
        --env XDG_CONFIG_HOME=/tmp/home/.config \
        "$IMAGE" -ceu 'printf "codex_path="; command -v codex; codex --version; codex exec --help' \
        >"${probe_dir}/stdout" 2>"${probe_dir}/stderr"
    probe_rc=$?
    printf '%s\n' "$probe_rc" >"${probe_dir}/exit-code"
    if [[ "$probe_rc" -ne 0 ]]; then
        printf 'UNVERIFIED codex probe (exit %s); cases skipped\n' "$probe_rc" | tee -a "${RUN_DIR}/summary.txt"
    else
        printf 'PASS codex exec help probe (manual case output review still required)\n' | tee -a "${RUN_DIR}/summary.txt"
        for package in "${PACKAGES[@]}"; do
            manifest="$REPO_ROOT/skills/${package}/evals/evals.json"
            case_index=0
            while IFS=$'\t' read -r case_id prompt_b64; do
                [[ -n "$case_id" ]] || continue
                case_name="codex-${package}-${case_index}-${case_id}"
                case_dir="${RUN_DIR}/${case_name}"
                prompt_file="${case_dir}/prompt.txt"
                mkdir -p "$case_dir"
                chmod 0777 "$case_dir"
                python3 - "$prompt_b64" "$prompt_file" <<'PY'
import base64
import pathlib
import sys
pathlib.Path(sys.argv[2]).write_bytes(base64.b64decode(sys.argv[1]))
PY
                # Prompt and source are read-only. Only /work/out is writable;
                # an edit attempt outside it therefore fails closed.
                codex_command="cat /work/prompt | timeout ${CODEX_TIMEOUT}s codex exec --ephemeral --ignore-user-config --ignore-rules --sandbox read-only --skip-git-repo-check --cd /work/package/${package} -o /work/out/last-message -"
                docker run --rm --entrypoint /bin/sh \
                    --cidfile "${CID_DIR}/${case_name}.cid" \
                    --label "${LABEL_KEY}=${LABEL_VALUE}" \
                    --label "${LABEL_KEY}.package=${package}" \
                    --label "${LABEL_KEY}.mode=codex" \
                    --label "${LABEL_KEY}.case=${case_id}" \
                    --read-only --user 10001:10001 --cap-drop=ALL \
                    --security-opt no-new-privileges --network "$CODEX_NETWORK" \
                    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=256m \
                    --tmpfs /tmp/home:rw,noexec,nosuid,nodev,size=32m \
                    --tmpfs /tmp/codex-home:rw,noexec,nosuid,nodev,size=32m \
                    --env HOME=/tmp/home --env CODEX_HOME=/tmp/codex-home \
                    --env XDG_CONFIG_HOME=/tmp/home/.config \
                    --env PYTHONDONTWRITEBYTECODE=1 \
                    --volume "$REPO_ROOT/skills/${package}:/work/package/${package}:ro" \
                    --volume "$prompt_file:/work/prompt:ro" \
                    --volume "$case_dir:/work/out:rw" \
                    --workdir /work "$IMAGE" -ceu "$codex_command" \
                    >"${case_dir}/stdout" 2>"${case_dir}/stderr"
                case_rc=$?
                printf '%s\n' "$case_rc" >"${case_dir}/exit-code"
                if [[ "$case_rc" -eq 0 ]]; then
                    printf 'PASS_TOOL %s (review final response; no semantic grade claimed)\n' "$case_id" | tee -a "${RUN_DIR}/summary.txt"
                elif [[ "$case_rc" -eq 124 ]]; then
                    printf 'UNVERIFIED %s (Codex case timeout after %ss; see stdout/stderr)\n' "$case_id" "$CODEX_TIMEOUT" | tee -a "${RUN_DIR}/summary.txt"
                elif grep -Eiq 'auth|credential|login|api[ _-]*key|unauthor|forbidden|network|connect|timed out|offline|dns|fetch' "$case_dir/stdout" "$case_dir/stderr"; then
                    printf 'UNVERIFIED %s (Codex auth/network unavailable; see stdout/stderr)\n' "$case_id" | tee -a "${RUN_DIR}/summary.txt"
                else
                    printf 'FAIL safety/tool %s (exit %s; see stdout/stderr)\n' "$case_id" "$case_rc" | tee -a "${RUN_DIR}/summary.txt" >&2
                    EXIT_STATUS=1
                fi
                {
                    for output_path in "$case_dir"/*; do
                        [[ -e "$output_path" ]] || continue
                        output_name="$(basename "$output_path")"
                        [[ "$output_name" == "prompt.txt" ]] || printf '%s\n' "$output_name"
                    done
                } | sort >"${case_dir}/output-inventory.txt"
                case_index=$((case_index + 1))
            done < <(python3 - "$manifest" <<'PY'
import base64
import json
import pathlib
import sys
payload = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for case in payload.get("codex_cases", []):
    print(f"{case['id']}\t{base64.b64encode(case['prompt'].encode()).decode()}")
PY
            )
        done
    fi
fi

if [[ "$EXIT_STATUS" -ne 0 ]]; then
    exit "$EXIT_STATUS"
fi
printf 'DONE: static checks passed; any Codex UNVERIFIED/PASS_TOOL statuses are recorded for review\n' | tee -a "${RUN_DIR}/summary.txt"
exit 0
