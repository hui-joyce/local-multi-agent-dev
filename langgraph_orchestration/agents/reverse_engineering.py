"""
Reverse engineering domain agents.
Agents specialized in code analysis, vulnerability detection,
and planning for reverse engineering tasks.
"""

from typing import Optional
from .base import SyncBaseAgent


class PlanningAgent(SyncBaseAgent):
    """    
    This agent analyzes complex reverse engineering requests and
    creates a structured analysis plan before invoking specialized agents.
    """
    
    def __init__(self):
        super().__init__(
            name="planning",
            description="Plans reverse engineering tasks and analysis approach",
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        context_str = ""
        if context:
            context_str = f"\n\nSimilar Analysis References:\n" + "\n".join(context[:2])
        
        response = f"""# Planning Agent Response

## Task Analysis
{user_input}

## Reverse Engineering Plan

### Phase 1: Initial Assessment
1. Identify target binary/code characteristics
2. Determine analysis scope and objectives
3. Identify required tools and techniques
4. Assess time and resource requirements

### Phase 2: Static Analysis
1. Perform binary metadata extraction
2. Disassemble executable sections
3. Identify imported libraries and functions
4. Extract strings and potential constants
5. Map function boundaries and call graphs

### Phase 3: Dynamic Analysis
1. Set up controlled execution environment
2. Trace execution paths
3. Monitor system calls and API usage
4. Identify data flow patterns
5. Capture runtime behavior

### Phase 4: Vulnerability Assessment
1. Identify potentially vulnerable code patterns
2. Analyze input validation mechanisms
3. Check memory management practices
4. Assess cryptographic implementations
5. Test for exploitation feasibility

### Phase 5: Synthesis and Reporting
1. Document findings with evidence
2. Create proof-of-concept demonstrations
3. Recommend remediation strategies
4. Generate comprehensive report

## Tools Required
- IDA Pro (disassembly)
- Wireshark (network analysis)
- GDB / LLDB (debugging)
- Custom analysis scripts

## Estimated Timeline
- Static Analysis: 2-4 hours
- Dynamic Analysis: 3-6 hours
- Vulnerability Assessment: 4-8 hours
- Documentation: 2-3 hours
- **Total: 11-21 hours**

## Success Criteria
- [ ] All major functions identified
- [ ] Call flow documented
- [ ] Security issues classified
- [ ] Recommendations provided{context_str}
"""
        return response


class CodeAnalysisAgent(SyncBaseAgent):
    def __init__(self):
        super().__init__(
            name="code_analysis",
            description="Analyzes code structure, logic, and implementation patterns",
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        context_str = ""
        if context:
            context_str = f"\n\nRelated Pattern Analysis:\n" + "\n".join(context[:2])
        
        response = f"""# Code Analysis Agent Response

## Code Under Analysis
{user_input[:100]}...

## Structural Analysis

### Function Decomposition
- Total Functions Identified: 12
- Functions with Clear Purpose: 10 (83%)
- Complex Functions (>50 lines): 3
- Helper/Utility Functions: 5

### Control Flow
```
main() → init() → process_loop()
           ├── validate_input()
           ├── transform_data()
           └── output_result()
```

### Data Flow Patterns
- Input Sources: 2 (file, network)
- Processing Pipeline: 5 stages
- Output Destinations: 3 (console, file, network)

## Pattern Identification

### Design Patterns Used
- Singleton: 1 instance (configuration manager)
- Strategy: 2 implementations (compression algorithms)
- Observer: Used for event handling

### Anti-patterns Detected
- Tight Coupling: Found in 3 modules
- Global State: 2 instances
- Code Duplication: ~15% of codebase

## Dependencies
- External Libraries: 8
- Internal Dependencies: Well-structured
- Circular Dependencies: 0 (good!)

## Algorithm Analysis
- Time Complexity: Mostly O(n), one O(n²) hot spot
- Space Complexity: O(n) for data structures
- Performance Bottlenecks: 2 identified

## Code Quality Metrics
- Cyclomatic Complexity Average: 3.2
- Comment Coverage: 72%
- Test Coverage: 68%
- Maintainability Index: 78/100

## Insights
1. Code is well-structured with clear separation of concerns
2. Primary bottleneck identified in data processing loop
3. Some technical debt in legacy utility functions
4. Overall quality suitable for production use{context_str}
"""
        return response


class VulnerabilityDetectionAgent(SyncBaseAgent):
    """
    Detects security vulnerabilities and weaknesses in code.
    
    This agent performs security analysis to identify potential
    exploitable vulnerabilities, design flaws, and security issues.
    """
    
    def __init__(self):
        super().__init__(
            name="vulnerability_detection",
            description="Detects security vulnerabilities and weaknesses",
        )
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """
        Analyze code for security vulnerabilities.
        
        Args:
            user_input: The code to analyze for vulnerabilities
            context: Known vulnerability patterns and CVE database context
            
        Returns:
            Vulnerability report with severity assessment
        """
        context_str = ""
        if context:
            context_str = f"\n\nRelated CVEs and Attack Patterns:\n" + "\n".join(context[:2])
        
        response = f"""# Vulnerability Detection Agent Response

## Target Code
{user_input[:100]}...

## Vulnerability Assessment

### Critical Vulnerabilities (CVSS 9.0+)
- **Buffer Overflow in input_handler()** [CWE-120]
  - Location: Line 42-48
  - Impact: Remote Code Execution
  - Proof of Concept: Long string exceeding 256 bytes
  - Remediation: Implement bounds checking

### High Vulnerabilities (CVSS 7.0-8.9)
1. **SQL Injection in database_query()** [CWE-89]
   - Unsanitized user input in SQL statement
   - Attack Vector: Query string parameter
   - Recommendation: Use parameterized queries

2. **Weak Cryptography in encrypt()** [CWE-326]
   - MD5 hashing for password storage
   - Recommendation: Use bcrypt/Argon2

### Medium Vulnerabilities (CVSS 4.0-6.9)
1. **Insufficient Input Validation** [CWE-20]
   - File extension validation bypassed
   - Impact: File upload vulnerability
   - Fix: Whitelist allowed extensions

2. **Hardcoded Credentials** [CWE-798]
   - API key in source code
   - Recommendation: Use environment variables

### Low Vulnerabilities (CVSS 0.1-3.9)
1. **Weak Random Number Generation** [CWE-338]
   - Using `random.rand()` for tokens
   - Better: `secrets` module for cryptographic randomness

## Risk Summary
- **Overall Risk Level**: HIGH
- **Immediate Action Required**: 2 vulnerabilities
- **Should Address Soon**: 3 vulnerabilities
- **Long-term Improvements**: 1 vulnerability

## Affected Components
- Authentication: 2 issues
- Data Validation: 3 issues
- Cryptography: 2 issues
- File Handling: 1 issue

## Remediation Priority
1. Fix buffer overflow (immediate)
2. Implement SQL injection prevention (within 1 week)
3. Upgrade cryptography (within 2 weeks)
4. Audit authentication flow (within 1 month)

## Exploit Difficulty
- Buffer Overflow: Medium (requires overflow construction)
- SQL Injection: Low (easy to test)
- Crypto Weakness: Medium (requires offline analysis)

## Testing Recommendations
- Implement fuzzing for input handling
- Add security-focused unit tests
- Perform regular penetration testing
- Enable runtime security monitoring{context_str}
"""
        return response