#!/usr/bin/env python3
"""Quick validation script to verify harness structure without model loading.

This runs a dry-run of the benchmark harness to check that:
- All imports resolve correctly
- Test cases are well-formed
- Output directory creation works
- No structural errors exist
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def validate_imports() -> bool:
    """Test that all required imports work."""
    try:
        from langgraph_orchestration.schemas.state import AgentState
        from langgraph_orchestration.prompts.software_dev import (
            build_dev_task_router_prompt,
            build_code_generation_prompt,
        )
        from langgraph_orchestration.prompts.reverse_engineering import (
            build_re_task_router_prompt,
            build_planning_prompt,
        )
        print("✓ All imports resolved successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def validate_test_cases() -> bool:
    """Load and validate test cases from harness"""
    try:
        from benchmarks.no_rag_harness import get_benchmark_cases
        
        cases = get_benchmark_cases()
        print(f"✓ Loaded {len(cases)} test cases:")
        for case in cases:
            print(f"  - {case.case_id}: {case.domain_focus} ({case.description[:50]}...)")
        return len(cases) > 0
    except Exception as e:
        print(f"✗ Failed to load test cases: {e}")
        return False

def validate_output_directory() -> bool:
    """Test that output directory can be created."""
    try:
        from pathlib import Path
        output_dir = Path("benchmarks/results")
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory ready: {output_dir.resolve()}")
        return True
    except Exception as e:
        print(f"✗ Failed to create output directory: {e}")
        return False

def validate_prompt_templates() -> bool:
    """Test that prompt template builders work"""
    try:
        from langgraph_orchestration.prompts.software_dev import (
            build_dev_task_router_prompt,
            build_code_generation_prompt,
            build_unit_testing_prompt,
        )
        from langgraph_orchestration.prompts.reverse_engineering import (
            build_re_task_router_prompt,
            build_planning_prompt,
            build_code_analysis_prompt,
        )
        
        # Test each builder
        test_input = "Test request"
        
        prompts = {
            "dev_router": build_dev_task_router_prompt(test_input),
            "dev_codegen": build_code_generation_prompt(test_input, 1),
            "dev_testing": build_unit_testing_prompt(test_input),
            "re_router": build_re_task_router_prompt(test_input),
            "re_planning": build_planning_prompt(test_input),
            "re_analysis": build_code_analysis_prompt(test_input),
        }
        
        for name, prompt in prompts.items():
            if not isinstance(prompt, str) or len(prompt) < 10:
                print(f"✗ Invalid prompt from {name}")
                return False
        
        print(f"✓ All {len(prompts)} prompt templates validated")
        return True
    except Exception as e:
        print(f"✗ Prompt template validation failed: {e}")
        return False

def main() -> None:
    """Run all validation checks."""
    print("\n" + "=" * 70)
    print("No-RAG Harness: Structure Validation")
    print("=" * 70 + "\n")
    
    checks = [
        ("Imports", validate_imports),
        ("Test Cases", validate_test_cases),
        ("Output Directory", validate_output_directory),
        ("Prompt Templates", validate_prompt_templates),
    ]
    
    results = []
    for check_name, check_fn in checks:
        print(f"\n[{check_name}]")
        results.append(check_fn())
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Validation: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All structural checks passed. Ready to run full harness:")
        print("  python3 benchmarks/no_rag_harness.py")
    else:
        print("\n✗ Some checks failed. Review errors above and fix before running harness.")
    
    print("=" * 70 + "\n")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()