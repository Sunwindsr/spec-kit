---
description: Mandatory validation and verification checkpoint after requirements definition phase
scripts:
  sh: scripts/bash/validate-requirements.sh --json --target "{ARGS}"
  ps: scripts/powershell/validate-requirements.ps1 -Json "{ARGS}"
---

The text the user typed after `/validate-requirements` in the triggering message **is** the target specification or test cases file to validate. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that target specification file, do this:

1. **Load Requirements Definition**: Load the test cases file from the specified path
   - If path is a directory: Look for `test-cases.md` in that directory
   - If path is a file: Use that file directly
   - If not found: ERROR "No test cases file found at {path}"

2. **Mandatory Validation Gateway**: Execute comprehensive validation checks
   - This is a FORCED checkpoint that MUST pass before any implementation can begin
   - Validation failures BLOCK progression to implementation phase
   - All checks must pass with strict criteria

3. **Completeness Validation**:
   - **EARS Requirements Coverage**: Every EARS requirement has corresponding test cases
   - **Test Case Quality**: Each test case is specific, measurable, and unambiguous
   - **Scenario Coverage**: Covers happy path, boundary cases, error paths, and edge cases
   - **Data Coverage**: Includes positive, negative, and boundary test data

4. **Precision Validation**:
   - **Input Specifications**: All inputs have exact formats, validation rules, and constraints
   - **Output Specifications**: All outputs have exact formats, structures, and content requirements
   - **Processing Logic**: Business logic is completely specified with step-by-step algorithms
   - **Error Handling**: All error conditions are identified with specific responses
   - **Performance Metrics**: All performance requirements have quantifiable metrics

5. **Traceability Validation**:
   - **Bidirectional Traceability**: Each requirement maps to test cases and vice versa
   - **Requirement Implementation**: Each requirement can be implemented based on test cases
   - **Test Verifiability**: Each test case can be objectively verified
   - **Acceptance Criteria**: Success criteria are measurable and unambiguous

6. **Quality Gate Validation**:
   - **Specificity Check**: No ambiguous language like "fast", "good", "user-friendly"
   - **Measurability Check**: All criteria have objective measurement methods
   - **Completeness Check**: No missing scenarios or edge cases
   - **Consistency Check**: No contradictory requirements or test cases
   - **Feasibility Check**: Requirements are technically achievable

7. **Validation Scoring**: Calculate quality score (0-100)
   - **Completeness**: 30 points (all requirements covered)
   - **Precision**: 30 points (specific and measurable)
   - **Traceability**: 20 points (clear bidirectional mapping)
   - **Quality**: 20 points (no ambiguity, complete coverage)

8. **Validation Results**:
   - **PASS (≥85 points)**: Requirements are ready for implementation
   - **WARNING (70-84 points)**: Requirements need minor improvements
   - **FAIL (<70 points)**: Requirements must be revised and resubmitted

9. **Validation Report**: Generate detailed validation report
   - **Quality Score**: Overall score and breakdown by category
   - **Pass/Fail Status**: Clear go/no-go recommendation
   - **Identified Issues**: Specific problems found and recommended fixes
   - **Improvement Suggestions**: Concrete suggestions for enhancement

10. **Enforcement Mechanism**: 
    - **FAIL Status**: Block implementation until requirements pass validation
    - **WARNING Status**: Require explicit acknowledgment before proceeding
    - **PASS Status**: Grant approval to proceed to implementation phase

11. **Validation Certificate**: Generate validation certificate file
    - Create `validation-certificate.md` in the same directory as test cases
    - Include validation score, status, and approval details
    - This certificate is REQUIRED for implementation phase to begin

12. **Integration with Implementation Workflow**: Update related files
    - Mark requirements as validated in project tracking
    - Update status in any project management systems
    - Prepare for handoff to implementation phase

**Critical Philosophy**: This validation gateway ensures that requirements are precise, complete, and unambiguous BEFORE any implementation begins, eliminating the root cause of AI implementation failures.

**Quality Thresholds**:
- **Blocking Issues**: Any ambiguity, missing scenarios, or unmeasurable criteria
- **Must Fix**: Specificity problems, completeness gaps, or traceability issues
- **Should Fix**: Quality improvements, consistency enhancements
- **Nice to Have**: Documentation improvements, formatting standardization

**Success Criteria**: The validation process transforms vague requirements into implementation-ready specifications that AI can execute with precision and confidence.