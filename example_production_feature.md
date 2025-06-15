# Exempel Feature Request för DigiNativa Production Test

## 🎯 Rekommenderad första feature för production pipeline

Skapa denna GitHub issue i ditt **project repository** (inte AI-team repot) för att testa hela pipelinen:

---

**Issue Title:**
```
[FEATURE] Snabbstartsguide för nya kommunanställda
```

**Labels att lägga till:**
- `feature-request`
- `priority-high`
- `pedagogical-content`
- `municipal-training`

**Issue Content:**

```markdown
---
name: DigiNativa Feature Request
about: Request a new pedagogical feature for Swedish municipalities
title: '[FEATURE] Snabbstartsguide för nya kommunanställda'
labels: ['feature-request', 'priority-high', 'pedagogical-content', 'municipal-training']
assignees: []
---

# 🎯 Feature Request for DigiNativa

## 📋 Feature Description
**Brief description of the feature:**
En interaktiv snabbstartsguide som hjälper nya kommunanställda att förstå grundläggande kommunala processer och verktyg under sin första vecka.

**Detailed description:**
Systemet ska erbjuda en välstrukturerad introduktionsguide där nya medarbetare kan:
- Få en översikt över kommunens organisation och struktur
- Lära sig de viktigaste IT-systemen och verktygen
- Förstå grundläggande säkerhetsrutiner och GDPR-krav
- Genomföra en enkel kunskapstest för att validera förståelse

## 👥 Target User
**Primary Persona:** Anna (Municipal Training Coordinator)
**Alternative Persona:** Nya medarbetare inom kommunal förvaltning

## 🎓 Learning Objectives
<!-- What should users learn or achieve with this feature? -->
- [ ] Förstå kommunens organisationsstruktur på grundnivå
- [ ] Lära sig använda de 3 viktigaste IT-systemen
- [ ] Känna till grundläggande säkerhetsrutiner

## ✅ Acceptance Criteria
<!-- Specific, testable requirements that define when this feature is complete -->
- [ ] Användare kan navigera genom minst 3 olika sektioner (Organisation, IT-system, Säkerhet)
- [ ] System visar progress-tracking för användarens framsteg
- [ ] Funktionen fungerar felfritt inom 5 minuter för en komplett genomgång
- [ ] Funktionen följer WCAG AA accessibility standards för skärmläsare
- [ ] All content använder professionell svensk kommunal terminologi

## ⏱️ Time Constraints
**Maximum completion time:** 5 minuter
**Target completion time:** 3 minuter

## 🏛️ Municipal Context
**Department:** HR och IT-support
**Use case scenario:** 
Nya medarbetare på svenska kommuner behöver snabbt komma igång med sitt arbete. Anna behöver ett system som ger grundläggande orientation utan att överbelasta nya kollegor med för mycket information första dagen.

**Policy alignment:**
Funktionen stödjer kommunens policy för systematisk introduktion och säkerställer att alla nya medarbetare får samma grundläggande kunskap om organisationen.

## 🎮 Game Design Requirements
**Interaction type:** Interaktiv guide med progressiva steg
**Pedagogical approach:** Steg-för-steg learning med visuella hjälpmedel
**Difficulty level:** Beginner

## 📊 Success Metrics
**How will we measure success?**
- User completion rate: >90%
- User satisfaction score: >4.0/5.0
- Average completion time: <5 minutes
- Knowledge retention: >80% efter 1 vecka
- Accessibility compliance: 100% WCAG AA

## 🔗 References
**GDD Section:** Municipal Onboarding Framework v1.0
**Related Issues:** N/A (första implementering)
**Documentation:** Standard HR-introduktionsprocess

## 🚨 Priority Justification
**Why is this important?**
Effektiv onboarding är kritisk för att nya medarbetare snabbt ska bli produktiva. En standardiserad snabbstartsguide minskar belastningen på HR och IT-support samtidigt som den säkerställer konsistent kvalitet i introduktionen.

**Urgency level:** 
- [x] High - Important for upcoming recruitment
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
- **Database:** SQLite för progress tracking
- **Testing:** Jest + Cypress för E2E
- **Accessibility:** WCAG 2.1 AA compliance
- **Performance:** <200ms API response, >90 Lighthouse score
```

---

## 🚀 Hur du startar teamet

### Steg 1: Förbered din miljö
```bash
# Sätt environment variables
export GITHUB_TOKEN="ditt_github_token"
export GITHUB_REPO_OWNER="ditt_github_användarnamn"
export GITHUB_REPO_NAME="ditt_projekt_repo_namn"
```

### Steg 2: Skapa GitHub Issue
1. Gå till ditt **projekt repository** (inte AI-team repot)
2. Klicka "Issues" → "New Issue"
3. Klistra in ovanstående content
4. Lägg till labels: `feature-request`, `priority-high`, `pedagogical-content`, `municipal-training`
5. Klicka "Submit new issue"
6. Kopiera URL:en till issuen

### Steg 3: Starta AI-teamet
```bash
# Testa först (dry run)
python start_production_pipeline.py --dry-run https://github.com/OWNER/REPO/issues/NUMMER

# Starta produktionspipelinen
python start_production_pipeline.py https://github.com/OWNER/REPO/issues/NUMMER
```

### Steg 4: Övervaka progress
```bash
# Följ loggar
tail -f production_pipeline_*.log

# Kolla genererade filer
ls docs/stories/
ls docs/specs/
ls docs/analysis/
```

### Steg 5: Vänta på godkännande-request
Teamet kommer att:
1. Analysera din issue (Project Manager)
2. Skapa UX specifikationer (Game Designer)  
3. Implementera koden (Developer)
4. Skapa tester (Test Engineer)
5. Validera kvalitet (QA Tester)
6. Förbereda för godkännande (Quality Reviewer)
7. **Skicka dig en GitHub notification** för godkännande

### Steg 6: Godkänn eller underkänn
Använd feature approval workflow för att:
- ✅ Godkänna featuren för production
- ❌ Underkänna med specifik feedback
- ⚠️ Godkänna med mindre issues

---

## 🎯 Varför denna feature är perfekt för första testet

**DNA-kompatibel:**
- ✅ Pedagogical Value: Klar utbildningskomponent
- ✅ Policy to Practice: Kommunala processer
- ✅ Time Respect: 5 minuter är realistiskt
- ✅ Holistic Thinking: Integrerar HR, IT, säkerhet
- ✅ Professional Tone: Kommunal kontext

**Tekniskt genomförbar:**
- ✅ Enkel scope för första implementation
- ✅ Klar success metrics
- ✅ Testbar acceptance criteria
- ✅ Realistisk timeline

**Affärsrelevant:**
- ✅ Löser verkligt problem för kommuner
- ✅ Demonstrerar DigiNativa's värde
- ✅ Skalbar för andra kommuner
- ✅ Mätbara resultat

---

**Lycka till med ditt första production test!** 🚀