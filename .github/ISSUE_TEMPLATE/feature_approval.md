---
name: DigiNativa Feature Approval/Rejection
about: Approve or reject a delivered feature from the AI Team
title: '[APPROVAL] {feature_title} - {story_id}'
labels: ['feature-approval', 'awaiting-decision']
assignees: []
---

# 🎯 Feature Approval Decision - {story_id}

## 📋 Feature Information
**Original Story ID:** {story_id}
**Feature Title:** {feature_title}
**Delivery Date:** {delivery_date}
**Quality Score:** {quality_score}/100

## ✅ APPROVAL DECISION
<!-- Choose ONE option by checking the box -->

- [ ] **APPROVED** - Feature meets requirements and is ready for production
- [ ] **REJECTED** - Feature needs revision before approval
- [ ] **APPROVED WITH MINOR ISSUES** - Feature is acceptable but has non-blocking issues

---

## 📊 Detailed Evaluation

### ✅ Acceptance Criteria Review
<!-- Review each original acceptance criterion -->
**Original Criteria:**
{original_acceptance_criteria}

**Evaluation:**
- [ ] ✅ Criterion 1: Met / ❌ Not Met - {detailed_feedback}
- [ ] ✅ Criterion 2: Met / ❌ Not Met - {detailed_feedback}
- [ ] ✅ Criterion 3: Met / ❌ Not Met - {detailed_feedback}

### 🎯 Feature Quality Assessment
**Anna Persona Experience:** {rating}/5.0
**Time Completion:** {actual_time} minutes (target: {target_time} minutes)
**Ease of Use:** {rating}/5.0
**Municipal Relevance:** {rating}/5.0
**Policy Alignment:** {rating}/5.0

### 💻 Technical Performance
**Page Load Speed:** {load_speed}ms (target: <2000ms)
**Mobile Responsiveness:** ✅ Good / ❌ Issues / ⚠️ Minor Issues
**Accessibility:** ✅ WCAG AA Compliant / ❌ Issues Found / ⚠️ Minor Issues
**Browser Compatibility:** {browser_test_results}

---

## ❌ REJECTION FEEDBACK (Complete if REJECTED)

### 🚨 Critical Issues (Must Fix)
<!-- List issues that prevent approval -->
1. **Issue:** {specific_issue_description}
   **Expected:** {what_should_happen}
   **Actual:** {what_actually_happens}
   **Priority:** Critical / High / Medium
   **Screenshots:** {attach_if_applicable}

2. **Issue:** {specific_issue_description}
   **Expected:** {what_should_happen}
   **Actual:** {what_actually_happens}
   **Priority:** Critical / High / Medium

### ⚠️ Minor Issues (Nice to Fix)
<!-- List non-blocking improvements -->
- {minor_issue_1}
- {minor_issue_2}
- {minor_issue_3}

### 🎯 Specific Requirements for Next Version
<!-- Detailed requirements for revision -->
1. **Requirement:** {specific_requirement}
   **Acceptance Criteria:** {how_to_test_this}
   **Business Justification:** {why_this_matters}

2. **Requirement:** {specific_requirement}
   **Acceptance Criteria:** {how_to_test_this}
   **Business Justification:** {why_this_matters}

### 📚 Additional Context
**Municipal Context:** {specific_municipal_use_case_issues}
**Policy Concerns:** {any_policy_compliance_issues}
**User Experience Issues:** {specific_ux_problems}
**Integration Concerns:** {workflow_integration_issues}

---

## ✅ APPROVAL CONFIRMATION (Complete if APPROVED)

### 🎉 What Works Well
- {positive_feedback_1}
- {positive_feedback_2}
- {positive_feedback_3}

### 📈 Business Value Delivered
**Problem Solved:** {how_this_solves_municipal_problem}
**User Impact:** {expected_user_adoption_and_impact}
**ROI Potential:** {revenue_or_efficiency_gains}

### 🚀 Ready for Production
- [ ] Feature tested in realistic municipal scenario
- [ ] Anna persona workflow validated
- [ ] Documentation reviewed and approved
- [ ] Training materials adequate
- [ ] No blocking integration issues

---

## 🔄 Next Steps Instructions

### If APPROVED:
**Project Manager Instructions:**
1. Deploy feature to production environment
2. Update feature status to "Live"
3. Begin work on next highest priority feature
4. Schedule follow-up review in 2 weeks

### If REJECTED:
**Project Manager Instructions:**
1. Analyze feedback and create revision plan
2. Break down feedback into specific development tasks
3. Ensure all critical issues are addressed in next version
4. Provide revised timeline estimate
5. Send acknowledgment within 4 hours

### Priority Queue Update:
**Next Feature to Work On:** {next_priority_feature_id}
**Dependencies Check:** {any_blocking_dependencies}
**Estimated Start Date:** {when_can_start_next}

---

## 📞 Follow-up Communication

**Preferred Communication Method:**
- [ ] GitHub comment updates
- [ ] Email notifications
- [ ] Slack/Teams messages
- [ ] Scheduled review meeting

**Response Timeline Expectation:**
- Feedback acknowledgment: Within 4 hours
- Revision plan: Within 1 business day
- Revised feature delivery: Within {estimated_revision_time}

**Additional Notes:**
{any_additional_context_or_requirements}

---

## 🤖 For AI Team Processing
<!-- DO NOT EDIT - This section is for automated processing -->

**Approval Status:** Pending Review
**Processing Agent:** project_manager
**Feedback Integration:** To be processed
**Original Contract:** {original_contract_reference}
**Quality Metrics:** {technical_quality_data}

### Automated Processing Triggers
- **On APPROVAL:** Deploy to production + start next feature
- **On REJECTION:** Process feedback + create revision tasks
- **On MINOR ISSUES:** Deploy with issue tracking