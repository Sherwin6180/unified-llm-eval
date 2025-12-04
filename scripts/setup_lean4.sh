#!/bin/bash
# =============================================================================
# Lean 4 and Mathlib4 Setup Script for MiniF2F Evaluation
# =============================================================================
#
# This script sets up the Lean 4 environment required for MiniF2F evaluation.
# It installs elan (Lean version manager), Lean 4, and builds Mathlib4.
#
# Prerequisites:
#   - Linux system (tested on Ubuntu 20.04+)
#   - curl, git installed
#   - Sufficient disk space (~10GB for Mathlib4)
#   - Sufficient RAM (~16GB recommended for building)
#
# Usage:
#   bash scripts/setup_lean4.sh
#
# The script will:
#   1. Install elan (Lean version manager)
#   2. Install Lean 4.9.0 (required version for Goedel-Prover-V2)
#   3. Build Mathlib4 in vendor/goedel-prover/mathlib4/
#
# =============================================================================

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GOEDEL_DIR="$PROJECT_ROOT/vendor/goedel-prover"
MATHLIB4_DIR="$GOEDEL_DIR/mathlib4"

echo "=============================================="
echo "Lean 4 + Mathlib4 Setup for MiniF2F"
echo "=============================================="
echo "Project root: $PROJECT_ROOT"
echo "Goedel-Prover dir: $GOEDEL_DIR"
echo "Mathlib4 dir: $MATHLIB4_DIR"
echo ""

# =============================================================================
# Step 0: Clone Goedel-Prover-V2 if not present
# =============================================================================
echo "[Step 0/5] Checking for Goedel-Prover-V2..."

if [ ! -d "$GOEDEL_DIR" ]; then
    echo "  Goedel-Prover-V2 not found. Cloning from GitHub..."
    mkdir -p "$PROJECT_ROOT/vendor"
    cd "$PROJECT_ROOT/vendor"
    git clone --recurse-submodules https://github.com/Goedel-LM/Goedel-Prover-V2.git goedel-prover
    echo "  ✓ Goedel-Prover-V2 cloned successfully"
else
    echo "  ✓ Goedel-Prover-V2 found"
    
    # Ensure submodules are initialized
    if [ ! -f "$MATHLIB4_DIR/lakefile.lean" ]; then
        echo "  Initializing mathlib4 submodule..."
        cd "$GOEDEL_DIR"
        git submodule update --init --recursive
    fi
fi

cd "$PROJECT_ROOT"

# =============================================================================
# Step 1: Check if elan is already installed
# =============================================================================
echo ""
echo "[Step 1/5] Checking for elan installation..."

ELAN_HOME="${ELAN_HOME:-$HOME/.elan}"
LAKE_PATH="$ELAN_HOME/bin/lake"

if command -v lake &> /dev/null; then
    echo "  ✓ lake found at: $(which lake)"
    LAKE_PATH="$(which lake)"
elif [ -f "$LAKE_PATH" ]; then
    echo "  ✓ lake found at: $LAKE_PATH"
else
    echo "  Installing elan (Lean version manager)..."
    
    # Install elan non-interactively
    curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --no-modify-path
    
    # Add to PATH for this script
    export PATH="$ELAN_HOME/bin:$PATH"
    
    if [ -f "$LAKE_PATH" ]; then
        echo "  ✓ elan installed successfully"
    else
        echo "  ✗ Failed to install elan"
        exit 1
    fi
fi

# =============================================================================
# Step 2: Install Lean 4.9.0 (required version)
# =============================================================================
echo ""
echo "[Step 2/5] Setting up Lean 4.9.0..."

# Check if we need to add elan to PATH
if ! command -v elan &> /dev/null; then
    export PATH="$ELAN_HOME/bin:$PATH"
fi

# Install the required Lean version
if elan show 2>/dev/null | grep -q "4.9.0"; then
    echo "  ✓ Lean 4.9.0 already installed"
else
    echo "  Installing Lean 4.9.0..."
    elan install leanprover/lean4:v4.9.0
    echo "  ✓ Lean 4.9.0 installed"
fi

# Set default if not set
elan default leanprover/lean4:v4.9.0 2>/dev/null || true

echo "  Current Lean version: $(lean --version 2>/dev/null || echo 'not in PATH')"

# =============================================================================
# Step 3: Check mathlib4 submodule
# =============================================================================
echo ""
echo "[Step 3/5] Checking Mathlib4 submodule..."

if [ ! -d "$MATHLIB4_DIR" ]; then
    echo "  ✗ Mathlib4 directory not found at $MATHLIB4_DIR"
    echo "  Please ensure the goedel-prover submodule is properly initialized:"
    echo "    cd vendor/goedel-prover && git submodule update --init --recursive"
    exit 1
fi

if [ ! -f "$MATHLIB4_DIR/lakefile.lean" ]; then
    echo "  ✗ Mathlib4 appears to be empty. Initializing submodule..."
    cd "$GOEDEL_DIR"
    git submodule update --init --recursive
    cd "$PROJECT_ROOT"
fi

echo "  ✓ Mathlib4 submodule found"

# =============================================================================
# Step 4: Build Mathlib4
# =============================================================================
echo ""
echo "[Step 4/5] Building Mathlib4..."
echo "  This may take 30-60 minutes on first build..."

cd "$MATHLIB4_DIR"

# Check if already built
if [ -d ".lake/build/lib" ] && [ "$(find .lake/build/lib -name '*.olean' 2>/dev/null | wc -l)" -gt 1000 ]; then
    echo "  ✓ Mathlib4 appears to be already built (found .olean files)"
    echo "  To rebuild, run: cd $MATHLIB4_DIR && lake build"
else
    echo "  Running 'lake build'..."
    
    # Make sure lake is in PATH
    export PATH="$ELAN_HOME/bin:$PATH"
    
    # Build mathlib4
    lake build
    
    echo "  ✓ Mathlib4 built successfully"
fi

# =============================================================================
# Step 5: Test the installation
# =============================================================================
echo ""
echo "[Step 5/5] Testing Lean 4 REPL..."

cd "$GOEDEL_DIR"

# Simple test to verify the REPL works
python3 -c "
import sys
sys.path.insert(0, 'lean_compiler')
from repl_scheduler import scheduler, proof_code_list_sample

# Run a simple test
print('  Running simple REPL test...')
results = scheduler(proof_code_list_sample[:1], num_workers=1)
if results:
    print('  ✓ Lean 4 REPL test passed')
else:
    print('  ⚠ REPL test returned empty results')
" 2>/dev/null || {
    echo "  ⚠ Could not run Python test (missing dependencies?)"
    echo "  The Lean installation should still work if you have the conda environment."
}

# =============================================================================
# Done
# =============================================================================
echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Lean 4 is installed at: $ELAN_HOME/bin/"
echo "Mathlib4 is built at: $MATHLIB4_DIR"
echo ""
echo "To use in your shell, add this to your ~/.bashrc:"
echo "  export PATH=\"$ELAN_HOME/bin:\$PATH\""
echo ""
echo "If you need to modify paths for the evaluator, edit:"
echo "  $GOEDEL_DIR/lean_compiler/repl_scheduler.py"
echo "  - DEFAULT_LAKE_PATH"
echo "  - DEFAULT_LEAN_WORKSPACE"
echo ""

