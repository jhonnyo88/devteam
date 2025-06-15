#!/usr/bin/env python3
"""
Create GitHub Issue for DigiNativa End-to-End Test

This script creates the exact GitHub issue described in the end-to-end test plan
for testing the Digital Medarbetarhandbok feature.
"""

import json
import os
from pathlib import Path

# GitHub issue content from the test plan
GITHUB_ISSUE_CONTENT = """---
name: DigiNativa Feature Request
about: Request a new pedagogical feature for Swedish municipalities
title: '[FEATURE] Digital Medarbetarhandbok med Interaktiv Utbildning'
labels: ['feature-request', 'priority-high', 'pedagogical-content', 'municipal-training']
assignees: []
---

# 🎯 Feature Request for DigiNativa

## 📋 Feature Description
**Brief description of the feature:**
En interaktiv digital medarbetarhandbok som hjälper nya kommunanställda att snabbt lära sig organisationens policies och rutiner genom spelifierade utbildningsmoduler.

**Detailed description:**
Systemet ska erbjuda en välstrukturerad digital handbok där nya medarbetare kan:
- Navigera genom olika avdelningar och deras specifika riktlinjer
- Ta del av interaktiva scenarion baserade på verkliga arbetssituationer
- Genomföra kunskapstest för att validera förståelse
- Få personlig progress-tracking och certifiering

## 👥 Target User
**Primary Persona:** Anna (Municipal Training Coordinator)
**Alternative Persona:** Nya medarbetare inom kommunal förvaltning

## 🎓 Learning Objectives
<!-- What should users learn or achieve with this feature? -->
- [ ] Förstå kommunens organisationsstruktur och hierarki
- [ ] Lära sig grundläggande policies för GDPR och informationssäkerhet
- [ ] Behärska kommunens interna processer för ärendehantering
- [ ] Känna till kommunens värdegrund och etiska riktlinjer

## ✅ Acceptance Criteria
<!-- Specific, testable requirements that define when this feature is complete -->
- [ ] Användare kan navigera genom minst 4 olika avdelningar (HR, IT, Ekonomi, Medborgarservice)
- [ ] System validerar användarnas förståelse genom interaktiva quiz med minst 80% rätt
- [ ] Funktionen fungerar felfritt inom 8 minuter för en komplett genomgång
- [ ] Funktionen följer WCAG AA accessibility standards för skärmläsare
- [ ] All content använder professionell svensk kommunal terminologi

## ⏱️ Time Constraints
**Maximum completion time:** 8 minuter
**Target completion time:** 6 minuter

## 🏛️ Municipal Context
**Department:** HR och Utbildning
**Use case scenario:** 
Nya medarbetare på Malmö stad ska genomgå obligatorisk introduktionsutbildning. Anna behöver ett system som automatiserar kunskapsöverföring och säkerställer att alla nya medarbetare får samma höga kvalitet på introduktionen, oavsett vilken avdelning de börjar på.

**Policy alignment:**
Funktionen stödjer kommunens policy för systematisk kompetensutveckling och säkerställer GDPR-compliance genom strukturerad utbildning om informationshantering.

## 🎮 Game Design Requirements
**Interaction type:** Interaktiv Simulation med Quiz-element
**Pedagogical approach:** Storytelling kombinerat med Problem-solving
**Difficulty level:** Beginner till Intermediate

## 📊 Success Metrics
**How will we measure success?**
- User completion rate: >95%
- User satisfaction score: >4.2/5.0
- Average completion time: <8 minutes
- Knowledge retention: >85% efter 2 veckor
- Accessibility compliance: 100% WCAG AA

## 🔗 References
**GDD Section:** Municipal Training Framework v2.1
**Related Issues:** N/A (första implementering)
**Documentation:** Malmö Stads HR-policy för introduktionsutbildning

## 🚨 Priority Justification
**Why is this important?**
Effektiv introduktionsutbildning är kritisk för att nya medarbetare snabbt ska bli produktiva och förstå kommunens arbetssätt. Manuell introduktionsutbildning är resurskrävande och inkonsistent. Denna lösning standardiserar kvaliteten och frigör HR-resurser för mer strategiska uppgifter.

**Urgency level:** 
- [x] High - Important for upcoming deadline (ny medarbetarintag i september)
- [ ] Critical - Blocks other features
- [ ] Medium - Normal priority
- [ ] Low - Nice to have

---

## 🤖 For AI Team Processing
<!-- DO NOT EDIT - This section is for automated processing -->

**Processing Status:** Pending
**Story ID:** Will be generated as STORY-GH-{issue_number}
**Assigned Agent:** project_manager
**DNA Compliance:** To be validated

### Required Technical Specifications
- **Frontend:** React + TypeScript + Shadcn/UI
- **Backend:** FastAPI + Python
- **Database:** PostgreSQL för progress tracking
- **Testing:** Jest + Cypress + Playwright
- **Accessibility:** WCAG 2.1 AA compliance
- **Performance:** <200ms API response, >90 Lighthouse score
"""

def create_local_test_file():
    """Create local test file for the GitHub issue."""
    test_file_path = Path("test_feature_request.md")
    
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(GITHUB_ISSUE_CONTENT)
    
    print(f"✅ Test feature request created: {test_file_path}")
    print("📋 Use this content to create a GitHub issue in your repository")
    print()
    print("🚀 Instructions:")
    print("1. Go to your GitHub repository")
    print("2. Click 'Issues' → 'New Issue'") 
    print("3. Copy content from test_feature_request.md")
    print("4. Add labels: feature-request, priority-high, pedagogical-content, municipal-training, e2e-test")
    print("5. Submit the issue")
    print("6. Run: python run_e2e_test.py")

def create_mock_github_response():
    """Create mock GitHub API response for testing."""
    mock_response = {
        "number": 1001,
        "title": "[FEATURE] Digital Medarbetarhandbok med Interaktiv Utbildning",
        "body": GITHUB_ISSUE_CONTENT,
        "state": "open",
        "labels": [
            {"name": "feature-request"},
            {"name": "priority-high"},
            {"name": "pedagogical-content"},
            {"name": "municipal-training"},
            {"name": "e2e-test"}
        ],
        "created_at": "2024-01-15T10:00:00Z",
        "html_url": "https://github.com/test-repo/issues/1001",
        "user": {
            "login": "test-user"
        }
    }
    
    mock_file_path = Path("test_github_issue_mock.json")
    with open(mock_file_path, 'w', encoding='utf-8') as f:
        json.dump(mock_response, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Mock GitHub response created: {mock_file_path}")
    print("📋 This can be used for testing GitHub integration without real API calls")

if __name__ == "__main__":
    print("🎯 DigiNativa E2E Test - GitHub Issue Creator")
    print("=" * 50)
    print()
    
    create_local_test_file()
    create_mock_github_response()
    
    print()
    print("📊 Test Assets Created:")
    print("  📄 test_feature_request.md - Issue content for GitHub")
    print("  📄 test_github_issue_mock.json - Mock API response for testing")
    print()
    print("🚀 Next step: Run 'python run_e2e_test.py' to test the pipeline!")