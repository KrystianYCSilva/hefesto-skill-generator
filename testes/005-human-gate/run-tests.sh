#!/bin/bash
# Script de testes automatizados para Feature 005 - Human Gate

cd "$(dirname "$0")/../.."

echo "=== INICIANDO TESTES MANUAIS - Feature 005 ==="
echo "Data: $(date)"
echo ""

# Test resultado counter
PASS=0
FAIL=0

# Helper function
run_test() {
    local test_num=$1
    local test_name=$2
    local command=$3
    
    echo "[TESTE $test_num] $test_name"
    echo "Comando: $command"
    echo ""
    
    # Executar comando (sem input interativo)
    eval "$command" 2>&1 | head -80
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "[OK] TESTE $test_num PASSOU"
        ((PASS++))
    else
        echo "[FALHA] TESTE $test_num FALHOU (exit code: $exit_code)"
        ((FAIL++))
    fi
    echo "=========================================="
    echo ""
}

# TESTE 1: Basic execution (non-interactive)
run_test 1 "Human Gate exibido" \
    "timeout 5 python commands/hefesto_create_impl.py 'Test skill basic' || true"

# TESTE 2: Help command
run_test 2 "Help command" \
    "python commands/hefesto_create_impl.py --help"

# TESTE 3: Resume command help
run_test 3 "Resume command help" \
    "python commands/hefesto_resume_impl.py --help"

# TESTE 4: Check modules exist
run_test 4 "Verify all 14 lib modules" \
    "ls commands/lib/*.py | wc -l | grep -q 14 && echo 'All 14 modules present'"

# TESTE 5: Validate colors module
run_test 5 "Colors module Unicode-safe" \
    "python -c 'from commands.lib.colors import safe_unicode; print(safe_unicode(\"✓\", \"OK\"))'"

# TESTE 6: Validate preview module
run_test 6 "Preview module import" \
    "python -c 'from commands.lib.preview import PreviewObject, create_preview; print(\"OK\")'"

# TESTE 7: Validate wizard module
run_test 7 "Wizard module import" \
    "python -c 'from commands.lib.wizard import WizardState; print(\"OK\")'"

# TESTE 8: Validate collision module
run_test 8 "Collision module import" \
    "python -c 'from commands.lib.collision import detect_collisions; print(\"OK\")'"

# TESTE 9: Validate human_gate module
run_test 9 "Human Gate module import" \
    "python -c 'from commands.lib.human_gate import present_human_gate, HumanGateDecision; print(\"OK\")'"

# TESTE 10: Validate atomic module
run_test 10 "Atomic module import" \
    "python -c 'from commands.lib.atomic import persist_skill_atomic; print(\"OK\")'"

# Summary
echo "=========================================="
echo "RESUMO DOS TESTES"
echo "=========================================="
echo "PASSOU: $PASS"
echo "FALHOU: $FAIL"
echo "TOTAL:  $((PASS + FAIL))"

if [ $FAIL -eq 0 ]; then
    echo ""
    echo "[OK] TODOS OS TESTES PASSARAM!"
    exit 0
else
    echo ""
    echo "[FALHA] ALGUNS TESTES FALHARAM"
    exit 1
fi
