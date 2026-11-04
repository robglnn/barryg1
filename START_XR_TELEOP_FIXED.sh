#!/bin/bash
# Hand-tracking teleop via the xr_teleop conda env.
# Extra args are passed through to teleop_hand_and_arm.py.
# CONDA_SH overrides conda discovery. CONDA_ENV overrides the env name.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

resolve_conda_sh() {
  if [[ -n "${CONDA_SH:-}" ]]; then
    printf '%s\n' "$CONDA_SH"
    return
  fi
  local candidate
  for candidate in \
    "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" \
    "/usr/local/Caskroom/miniconda/base/etc/profile.d/conda.sh" \
    "$HOME/miniconda3/etc/profile.d/conda.sh" \
    "$HOME/miniforge3/etc/profile.d/conda.sh" \
    "$HOME/mambaforge/etc/profile.d/conda.sh" \
    "$HOME/anaconda3/etc/profile.d/conda.sh"
  do
    if [[ -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  printf '%s\n' "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
}

CONDA_SH="$(resolve_conda_sh)"
if [[ ! -f "$CONDA_SH" ]]; then
  echo "conda.sh not found at: $CONDA_SH" >&2
  echo "Set CONDA_SH to your conda install's etc/profile.d/conda.sh" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$CONDA_SH"
conda activate "${CONDA_ENV:-xr_teleop}"
cd "$REPO_ROOT/dependencies/xr_teleoperate/teleop"
exec python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive "$@"
