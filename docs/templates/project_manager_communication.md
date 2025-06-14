# Project Manager Communication Templates

## 🎯 PURPOSE
Standardized communication templates for Project Manager Agent to ensure consistent, professional interaction with project owners (humans) throughout the development lifecycle.

## 📋 TEMPLATE CATEGORIES

### 1. Issue Acknowledgment Templates

#### Feature Request Acknowledged
```markdown
# 🎯 Feature Request Acknowledged - {story_id}

Hej {requester_name}!

Your feature request **"{feature_title}"** has been received and assigned story ID: `{story_id}`

## 📊 Initial Analysis
- **Priority Level:** {priority}
- **Estimated Complexity:** {complexity_level}
- **Target Persona:** {user_persona}
- **Time Constraint:** {time_constraint} minutes

## 🔄 Next Steps
1. **Feature Analysis** - Analyzing requirements and breaking down into implementable tasks
2. **DNA Compliance Check** - Validating alignment with DigiNativa design principles
3. **Technical Specification** - Creating detailed technical requirements
4. **Agent Handoff** - Passing to Game Designer for UX specification

## ⏱️ Expected Timeline
- Analysis Complete: Within 2 hours
- Game Design: Within 1 day
- Development Start: Within 2 days
- Feature Complete: Within 1 week

I'll keep you updated on progress. Feel free to add any additional requirements or clarifications to the GitHub issue.

Mvh,
DigiNativa AI Team (Project Manager)
```

#### Issue Needs Clarification
```markdown
# ❓ Clarification Needed - {story_id}

Hej {requester_name}!

I've reviewed your request **"{feature_title}"** but need some clarification to ensure we build exactly what you need.

## 🚨 Missing Information
{missing_fields_list}

## ❓ Specific Questions
{clarification_questions}

## 🎯 Why This Matters
Clear requirements ensure:
- ✅ Feature meets your exact needs
- ✅ Development stays within budget
- ✅ Anna persona gets the best experience
- ✅ Municipal policies are properly supported

## 🔄 Next Steps
Please update the GitHub issue with the requested information. Once complete, I'll proceed with feature analysis immediately.

Estimated delay: {estimated_delay}

Mvh,
DigiNativa AI Team (Project Manager)
```

### 2. Progress Update Templates

#### Analysis Complete
```markdown
# 📊 Feature Analysis Complete - {story_id}

Hej {requester_name}!

Great news! Analysis of **"{feature_title}"** is complete.

## 🎯 Feature Breakdown
{feature_breakdown_summary}

## ✅ DNA Compliance Validation
- **Pedagogical Value:** {pedagogical_score}/5.0
- **Policy-to-Practice:** {policy_score}/5.0  
- **Time Respect:** {time_score}/5.0
- **Holistic Thinking:** {holistic_score}/5.0
- **Professional Tone:** {professional_score}/5.0

**Overall DNA Score:** {overall_dna_score}/5.0 ✅

## 🎮 Technical Approach
- **Frontend Components:** {component_count} React components
- **Backend Endpoints:** {endpoint_count} FastAPI endpoints
- **Database Changes:** {database_changes}
- **External Integrations:** {integrations}

## 🔄 Next Steps
Feature is now being handed off to Game Designer for UX specification. You'll receive an update when design is complete.

**Current Status:** Analysis ✅ → Design 🔄 → Development → Testing → Deployment

Mvh,
DigiNativa AI Team (Project Manager)
```

#### Feature Deployed
```markdown
# 🚀 Feature Deployed Successfully - {story_id}

Hej {requester_name}!

Excellent news! **"{feature_title}"** has been successfully deployed and is now live.

## 📊 Final Quality Metrics
- **Overall Quality Score:** {quality_score}/100
- **Performance:** API <{api_response_time}ms, Lighthouse {lighthouse_score}/100
- **Accessibility:** WCAG AA {accessibility_score}% compliant
- **Test Coverage:** {test_coverage}% (all tests passing)
- **User Experience:** {ux_score}/5.0 for Anna persona

## 🎯 Feature Capabilities
{feature_capabilities_summary}

## 🔗 Access Information
- **Live URL:** {feature_url}
- **Documentation:** {documentation_url}
- **Training Materials:** {training_materials_url}

## 📈 Success Metrics
We'll monitor these metrics for the first week:
- User completion rate (target: >90%)
- User satisfaction (target: >4.0/5.0)
- Average completion time (target: <{target_time} minutes)

## 💡 Recommended Next Steps
{recommended_next_steps}

Thank you for your clear requirements and patience during development!

Mvh,
DigiNativa AI Team (Project Manager)
```

### 3. Error/Issue Templates

#### Feature Rejected
```markdown
# ⚠️ Feature Request Requires Revision - {story_id}

Hej {requester_name}!

After thorough analysis, **"{feature_title}"** requires revision before we can proceed with development.

## 🚨 Issues Identified
{blocking_issues_list}

## 📋 DNA Compliance Concerns
{dna_compliance_issues}

## 💡 Recommended Solutions
{recommended_solutions}

## 🔄 Next Steps
1. Please revise the feature request addressing the concerns above
2. Update the GitHub issue with revised requirements
3. I'll re-analyze and provide updated assessment within 2 hours

This quality gate ensures we deliver features that truly serve Swedish municipalities and provide excellent user experience for Anna.

Mvh,
DigiNativa AI Team (Project Manager)
```

#### Development Blocked
```markdown
# 🛑 Development Temporarily Blocked - {story_id}

Hej {requester_name}!

Development of **"{feature_title}"** has encountered a blocking issue that requires your input.

## 🚨 Blocking Issue
{blocking_issue_description}

## 🎯 Impact Assessment
- **Timeline Impact:** {timeline_impact}
- **Development Status:** {current_progress}
- **Alternative Options:** {alternative_options}

## ❓ Decision Required
{decision_required}

## ⏱️ Response Timeline
To minimize project delay, please respond within {response_deadline}.

I'm monitoring this issue and will proceed immediately once resolved.

Mvh,
DigiNativa AI Team (Project Manager)
```

## 🎯 USAGE GUIDELINES

### Template Selection Rules
1. **Issue Acknowledgment:** Use within 30 minutes of issue creation
2. **Progress Updates:** Send at each major milestone
3. **Error/Issue:** Send immediately when blocking issues occur
4. **Final Deployment:** Send within 1 hour of successful deployment

### Personalization Requirements
- Always use requester's name if available
- Reference specific feature details from the issue
- Include relevant metrics and scores
- Maintain professional Swedish business tone

### Quality Standards
- All templates must be professional and informative
- Include specific next steps and timelines
- Provide clear contact information for follow-up
- Maintain consistency with DigiNativa brand voice

## 🔄 TEMPLATE MAINTENANCE
These templates should be updated when:
- New agent capabilities are added
- Quality metrics change
- Communication feedback is received
- Business processes evolve

---

**Note:** These templates are used by the Project Manager Agent's automated communication system. They ensure consistent, professional communication that builds trust with municipal clients.