# GitHub Issue Validation Standards

## 🎯 PURPOSE
Define validation rules and quality gates for GitHub issues to ensure consistent feature development and prevent parsing errors in the AI Team pipeline.

## 📋 VALIDATION CATEGORIES

### 1. Required Fields Validation

#### Feature Request Requirements
```yaml
required_fields:
  title:
    pattern: "^\\[FEATURE\\]\\s+.+"
    min_length: 20
    max_length: 100
    
  description:
    min_length: 100
    max_length: 2000
    required_sections:
      - "Feature Description"
      - "Target User" 
      - "Learning Objectives"
      - "Acceptance Criteria"
      - "Time Constraints"
      
  labels:
    required:
      - "feature-request"
    priority_required: true
    valid_priorities:
      - "priority-critical"
      - "priority-high" 
      - "priority-medium"
      - "priority-low"
      
  acceptance_criteria:
    min_count: 3
    max_count: 10
    format: "- [ ] {criterion}"
    
  learning_objectives:
    min_count: 1
    max_count: 5
    format: "- [ ] {objective}"
```

#### Bug Report Requirements
```yaml
required_fields:
  title:
    pattern: "^\\[BUG\\]\\s+.+"
    min_length: 15
    max_length: 100
    
  reproduction_steps:
    min_count: 3
    format: "numbered list"
    
  environment:
    required:
      - "Browser"
      - "Operating System"
      - "Device"
      
  severity:
    valid_values:
      - "Critical"
      - "High" 
      - "Medium"
      - "Low"
```

### 2. Content Quality Validation

#### Feature Description Quality Gates
```python
def validate_feature_description(description: str) -> ValidationResult:
    """Validate feature description quality."""
    
    quality_checks = {
        "clarity": check_description_clarity(description),
        "completeness": check_description_completeness(description),
        "municipal_context": check_municipal_relevance(description),
        "anna_persona_mention": check_persona_relevance(description),
        "policy_alignment": check_policy_references(description),
        "technical_feasibility": check_technical_scope(description)
    }
    
    return ValidationResult(
        passed=all(quality_checks.values()),
        issues=[k for k, v in quality_checks.items() if not v],
        score=sum(quality_checks.values()) / len(quality_checks)
    )
```

#### Acceptance Criteria Quality Standards
```python
def validate_acceptance_criteria(criteria: List[str]) -> ValidationResult:
    """Validate acceptance criteria quality."""
    
    validation_rules = {
        "testable": all(is_testable(criterion) for criterion in criteria),
        "specific": all(is_specific(criterion) for criterion in criteria),
        "measurable": all(is_measurable(criterion) for criterion in criteria),
        "user_focused": all(is_user_focused(criterion) for criterion in criteria),
        "time_bounded": any(has_time_constraint(criterion) for criterion in criteria),
        "accessibility_mentioned": any("accessibility" in criterion.lower() for criterion in criteria)
    }
    
    return ValidationResult(
        passed=sum(validation_rules.values()) >= 4,  # At least 4/6 rules must pass
        score=sum(validation_rules.values()) / len(validation_rules),
        required_improvements=[k for k, v in validation_rules.items() if not v]
    )
```

### 3. DNA Compliance Pre-Validation

#### Design Principles Alignment Check
```python
def pre_validate_dna_compliance(issue_content: str) -> DNAComplianceCheck:
    """Pre-validate DNA compliance before full PM analysis."""
    
    design_principles = {
        "pedagogical_value": {
            "keywords": ["learn", "teach", "education", "training", "skill", "knowledge"],
            "score": calculate_keyword_relevance(issue_content, keywords),
            "threshold": 0.6
        },
        "policy_to_practice": {
            "keywords": ["policy", "procedure", "guideline", "regulation", "municipal"],
            "score": calculate_keyword_relevance(issue_content, keywords),
            "threshold": 0.4
        },
        "time_respect": {
            "time_mention": extract_time_constraints(issue_content),
            "realistic_scope": assess_scope_feasibility(issue_content),
            "threshold": 0.5
        },
        "holistic_thinking": {
            "integration_mentions": count_integration_references(issue_content),
            "workflow_awareness": check_workflow_understanding(issue_content),
            "threshold": 0.3
        },
        "professional_tone": {
            "language_quality": assess_language_professionalism(issue_content),
            "municipal_context": check_governmental_awareness(issue_content),
            "threshold": 0.7
        }
    }
    
    return DNAComplianceCheck(
        passed=all(p["score"] >= p["threshold"] for p in design_principles.values()),
        scores={k: v["score"] for k, v in design_principles.items()},
        warnings=generate_dna_warnings(design_principles)
    )
```

### 4. Automated Validation Rules

#### Project Manager GitHub Integration Enhancement
```python
# Add to GitHubIntegration class

async def validate_issue_before_processing(self, issue_data: Dict[str, Any]) -> ValidationResult:
    """Validate GitHub issue before creating contract."""
    
    validation_results = []
    
    # 1. Required fields validation
    required_validation = self._validate_required_fields(issue_data)
    validation_results.append(required_validation)
    
    # 2. Content quality validation  
    quality_validation = self._validate_content_quality(issue_data)
    validation_results.append(quality_validation)
    
    # 3. DNA compliance pre-check
    dna_validation = self._pre_validate_dna_compliance(issue_data)
    validation_results.append(dna_validation)
    
    # 4. Technical feasibility check
    feasibility_validation = self._validate_technical_feasibility(issue_data)
    validation_results.append(feasibility_validation)
    
    # Combine results
    overall_passed = all(result.passed for result in validation_results)
    all_issues = []
    for result in validation_results:
        all_issues.extend(result.issues)
    
    if not overall_passed:
        # Post clarification comment to GitHub issue
        await self._request_issue_clarification(
            issue_data["number"], 
            all_issues
        )
    
    return ValidationResult(
        passed=overall_passed,
        issues=all_issues,
        validation_score=sum(r.score for r in validation_results) / len(validation_results)
    )

async def _request_issue_clarification(self, issue_number: int, issues: List[str]) -> None:
    """Post clarification request comment to GitHub issue."""
    
    clarification_template = """
# ❓ Clarification Needed - Issue #{issue_number}

Hej! I've reviewed this issue but need some clarification to ensure we build exactly what you need.

## 🚨 Issues Found
{issues_list}

## 💡 How to Fix
1. Please update the issue description addressing the points above
2. Use our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) for guidance
3. Check the [Issue Quality Guidelines](docs/contracts/github_issue_validation.md)

## 🔄 Next Steps
Once updated, I'll automatically re-analyze and proceed with feature development.

**Estimated delay:** 2-4 hours after clarification

Mvh,
DigiNativa AI Team (Project Manager)
    """.format(
        issue_number=issue_number,
        issues_list="\n".join(f"- {issue}" for issue in issues)
    )
    
    await self._add_issue_comment(issue_number, clarification_template)
    await self._add_issue_label(issue_number, "needs-clarification")
```

### 5. Quality Gates Configuration

#### Validation Thresholds
```yaml
quality_gates:
  feature_request:
    minimum_score: 0.8
    required_fields_score: 1.0  # All required fields must be present
    content_quality_score: 0.7
    dna_compliance_score: 0.6
    technical_feasibility_score: 0.8
    
  critical_features:
    minimum_score: 0.9
    manual_review_required: true
    stakeholder_approval_required: true
    
  bug_reports:
    minimum_score: 0.7
    reproduction_steps_required: true
    environment_details_required: true
    
validation_actions:
  score_below_threshold:
    action: "request_clarification"
    auto_retry: true
    max_retry_attempts: 3
    
  score_above_threshold:
    action: "proceed_to_processing"
    auto_assign: "project_manager"
    
  critical_feature_detected:
    action: "escalate_to_human"
    notify_stakeholders: true
```

### 6. Error Messages and Guidance

#### Common Validation Errors
```markdown
## Common Issues and Solutions

### ❌ "Feature description too vague"
**Problem:** Description lacks specific details about functionality
**Solution:** Add concrete examples of user interactions and expected outcomes

### ❌ "Missing acceptance criteria"
**Problem:** No testable acceptance criteria provided
**Solution:** Add 3-10 specific, testable criteria using checkbox format

### ❌ "No time constraints specified"
**Problem:** No mention of completion time expectations
**Solution:** Specify maximum time users should need to complete the feature

### ❌ "Municipal context unclear"
**Problem:** Feature doesn't clearly relate to Swedish municipal operations
**Solution:** Explain which department would use this and how it supports their work

### ❌ "Anna persona not considered"
**Problem:** No mention of how this serves Anna's needs as training coordinator
**Solution:** Describe Anna's specific use case and workflow integration
```

### 7. Integration with PM Agent

#### Contract Creation Enhancement
```python
# Update in GitHubIntegration.convert_issue_to_contract()

def convert_issue_to_contract(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced contract creation with validation results."""
    
    # Run validation first
    validation_result = await self.validate_issue_before_processing(issue_data)
    
    if not validation_result.passed:
        raise BusinessLogicError(
            f"GitHub issue fails validation: {validation_result.issues}",
            business_rule="github_issue_validation",
            context={
                "issue_number": issue_data["number"],
                "validation_score": validation_result.validation_score,
                "issues": validation_result.issues
            }
        )
    
    # Include validation metadata in contract
    contract = self._create_base_contract(issue_data)
    contract["validation_metadata"] = {
        "validation_score": validation_result.validation_score,
        "validation_timestamp": datetime.now().isoformat(),
        "quality_gates_passed": validation_result.passed
    }
    
    return contract
```

## 🔄 MAINTENANCE AND UPDATES

### Monthly Review Process
1. **Validation Effectiveness Analysis:** Review rejected vs. accepted issue ratios
2. **False Positive Reduction:** Adjust thresholds based on feedback
3. **Template Updates:** Update templates based on common clarification requests
4. **Quality Metrics:** Track improvement in issue quality over time

### Success Metrics
- **Issue Clarity Rate:** >90% of issues pass validation on first submission
- **Clarification Request Rate:** <10% of issues require clarification
- **Development Blocking Issues:** <5% of features blocked due to unclear requirements
- **Client Satisfaction:** >4.5/5.0 rating for requirement clarity

---

**Note:** These validation standards ensure consistent, high-quality input to the AI Team pipeline, reducing development delays and improving feature delivery quality.