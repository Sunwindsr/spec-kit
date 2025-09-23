---
description: Create or update test cases from EARS requirements with structured validation scenarios
scripts:
  sh: scripts/bash/create-new-test-cases.sh --json --feature-name "<extracted-feature-name>" --target "{ARGS}"
  ps: scripts/powershell/create-new-test-cases.ps1 -Json -FeatureName "<extracted-feature-name>" "{ARGS}"
---

The text the user typed after `/test-cases` in the triggering message **is** the target system description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that target system description, do this:

1. **Feature Name Extraction**: Extract a meaningful feature name from the target path:
   - Extract the core system/module identifier from the path or description
   - For paths like "/home/sd_dev/projects/business-management/frontend/ClientApp/src/app/Entrances/Frontend/ViewsEntrance/BizModules/ViewAppFilesBiz", extract "ViewAppFilesBiz" as the core component
   - Remove generic prefixes like "src", "app", "frontend" and focus on the business module
   - Generate a clean, kebab-case feature name (2-5 words)
   - Examples: "view-app-files-biz", "file-viewer-component", "payment-service", "data-access-layer"

2. **Load Existing Specifications**: Load existing specifications to understand context:
   - If refactoring: Load refactoring specification from `/specs/[###-refactoring-name]/spec.md`
   - If new feature: Load feature specification from `/specs/[###-feature-name]/spec.md`
   - Extract all EARS requirements and user stories
   - Identify all interfaces, data models, and business rules

3. **Test Case Strategy Selection**: Choose appropriate template based on project type:
   - For refactoring: Use `test-cases-refactoring-template.md` (behavior preservation focus)
   - For new features: Use `test-cases-template.md` (EARS requirements focus)

4. **Deep Requirements Analysis**: Go beyond surface-level requirements:
   - **Business Logic Scenarios**: Identify all business rule combinations and edge cases
   - **Data Validation Scenarios**: Extract all validation rules, constraints, and data dependencies
   - **Integration Points**: Identify all external system interactions and API calls
   - **State Transition Scenarios**: Map all possible state changes and transitions
   - **Error Handling Scenarios**: Define all error conditions and recovery paths
   - **Performance Requirements**: Extract response times, throughput, and scalability needs
   - **Security Requirements**: Identify authentication, authorization, and data protection needs

5. **Test Case Generation**: Generate comprehensive test cases by category:
   - **Happy Path Tests**: Primary success scenarios with realistic data
   - **Boundary Value Tests**: Edge cases, limits, and critical values
   - **Error Path Tests**: Exception handling and error recovery
   - **State-Dependent Tests**: Behavior under different system states
   - **Integration Tests**: External system and API interaction
   - **Performance Tests**: Response time and resource usage validation
   - **Security Tests**: Authentication, authorization, and data protection

6. **Precision Requirements Definition**: For each test case, define:
   - **Exact Pre-conditions**: Specific system state required before test execution
   - **Specific Input Data**: Realistic test data with variations (valid, invalid, boundary)
   - **Detailed Execution Steps**: Precise user actions or API calls to execute
   - **Measurable Expected Results**: Objectively verifiable outcomes with specific values
   - **Clear Success Criteria**: Unambiguous conditions for test pass/fail determination

7. **Test Data Management**: Define comprehensive test data sets:
   - **Positive Test Data**: Valid data that should succeed
   - **Negative Test Data**: Invalid data that should fail appropriately
   - **Boundary Test Data**: Data at the edges of valid ranges
   - **Realistic Production Data**: Data that mimics real-world usage patterns
   - **Security Test Data**: Data that tests security vulnerabilities

8. **Behavior Preservation (Refactoring Only)**: For refactoring projects, ensure:
   - **Baseline Establishment**: Document current system behavior before refactoring
   - **Comparison Testing**: Tests that verify identical behavior between old and new systems
   - **Performance Benchmarking**: Tests that ensure no performance degradation
   - **Interface Compatibility**: Tests that verify backward compatibility

9. **Quality Validation**: Validate generated test cases:
   - **Completeness**: All requirements have corresponding test cases
   - **Specificity**: Test cases are specific and unambiguous
   - **Verifiability**: Expected results are objectively measurable
   - **Realism**: Test scenarios reflect real-world usage
   - **Coverage**: All critical scenarios are covered

10. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and TEST_FILE. All file paths must be absolute.
    **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

11. Write the comprehensive test cases to TEST_FILE using the selected template structure, replacing placeholders with concrete details derived from the deep requirements analysis.

12. Report completion with test file path, test case count, and readiness for implementation.

**Key Philosophy**: Test cases serve as the precise bridge between ambiguous requirements and concrete implementation. Well-defined test cases eliminate interpretation gaps and ensure implementation exactly matches business needs.

**Critical Success Factors**:
- **Precision**: Each test case must be specific and unambiguous
- **Completeness**: Cover all requirements, including edge cases and error scenarios
- **Verifiability**: Expected results must be objectively measurable
- **Realism**: Test scenarios should reflect real-world usage patterns
- **Traceability**: Each test case must trace back to specific EARS requirements