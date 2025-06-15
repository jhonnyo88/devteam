# GitHub Issue: Grundläggande kommunal onboarding-modul

**Använd den nya DigiNativa AI Team templaten i:** `https://github.com/jhonnyo88/diginativa-game/issues/new`

**Välj:** "🚀 Feature Request (DigiNativa AI Team)" template

---

## 📝 Hur du fyller i templaten:

### **Feature Summary**
```
Grundläggande kommunal onboarding-modul för nya medarbetare
```

### **User Story**
```
As Anna (kommunal förvaltare), I want a simple onboarding module that introduces new employees to our organization structure and basic processes so that they can become productive faster and feel confident in their new role without requiring extensive manual guidance from HR.
```

### **🧬 DNA Compliance**

#### Design Principles Alignment:
- ✅ **Pedagogik Framför Allt** - Clear educational goals about municipal organization
- ✅ **Policy till Praktik** - Bridges organizational policies to daily work
- ✅ **Respekt för Tid** - 4-minute maximum completion time
- ✅ **Helhetssyn** - Shows organizational connections and context
- ✅ **Intelligens, Inte Infantilisering** - Professional tone for adult learners

#### Architecture Principles:
- ✅ **API-First Design** - All functionality via REST APIs
- ✅ **Stateless Backend** - No server-side sessions needed
- ✅ **Separation of Concerns** - Clear frontend/backend separation
- ✅ **Simplicity First** - Minimal complexity for maximum impact

### **🏛️ Municipal Context**

#### Primary Target Persona:
```
Anna (Offentlig förvaltare - primary learning persona)
```

#### Municipal Department Focus:
```
HR/Personalavdelning (Human resources)
```

#### Municipal Use Case & Policy Alignment:
```
**Municipal Process:** New employee onboarding and orientation process

**Policy Alignment:** Supports municipal HR policy for systematic employee introduction and ensures consistent quality in the onboarding experience across all departments

**Expected Impact:** 
- 50% reduction in HR time spent on manual onboarding
- Improved new employee confidence and faster time-to-productivity
- Standardized organizational knowledge transfer
```

### **🎯 Learning Objectives**
- ✅ **Policy Understanding** - Comprehend basic municipal organization structure
- ✅ **Practical Application** - Apply organizational knowledge to daily work context
- ✅ **Stakeholder Engagement** - Understand different department roles and interactions

### **Success Metrics & Measurement**
```
**Completion Rate Target:** >85% of new employees complete within first week

**Satisfaction Score Target:** >4.0/5.0 user satisfaction

**Knowledge Retention Measure:** >75% pass rate on follow-up quiz after 1 week

**Behavioral Impact Expected:** 25% faster integration into work teams, reduced questions to HR
```

### **⏰ Time Constraints**

#### Maximum Completion Time:
```
5 minutes (quick task)
```

#### Target Completion Time:
```
3 minutes
```

### **💻 Technical Requirements**
- ✅ **React Components** - Custom UI components needed
- ✅ **Shadcn/UI Integration** - Use existing component library
- ✅ **Mobile Responsive** - Must work on mobile devices
- ✅ **Accessibility (WCAG AA)** - Screen reader & keyboard navigation
- ✅ **Analytics Integration** - Usage tracking and metrics

### **Performance Requirements**
- ✅ **API Response Time** - All endpoints must respond <200ms
- ✅ **Lighthouse Score** - Performance score >90
- ✅ **Mobile Performance** - Smooth operation on mobile devices
- ✅ **TypeScript Compliance** - Zero TypeScript errors
- ✅ **Test Coverage** - 100% code coverage required

### **Implementation Planning**

#### Estimated Implementation Complexity:
```
Simple (1-2 components, minimal logic) - 2-4 hours
```

#### Business Priority Level:
```
P1 - High (key business value, current focus area)
```

### **Acceptance Criteria (Detailed)**
```
- [ ] User can access onboarding module from main navigation
- [ ] Module displays 3 department sections (Kommunledning, HR, IT)
- [ ] Each section loads within 2 seconds
- [ ] Progress indicator shows completion status
- [ ] Knowledge check with 3 questions, 80% pass requirement
- [ ] All content available in Swedish
- [ ] Works correctly on desktop, tablet, and mobile
- [ ] Keyboard navigation works for all interactive elements
- [ ] Screen reader announces section transitions correctly
- [ ] Completion tracked in user progress system
- [ ] Success metrics automatically collected
- [ ] Graceful error handling with helpful Swedish messages
```

### **Feature Dependencies**
```
None (foundational feature)
```

### **Technical Considerations & Constraints**
```
**Integrations Required:**
- User authentication system integration
- Progress tracking API integration
- Analytics/metrics collection system

**Security Considerations:**
- GDPR compliance for employee data
- Municipal data privacy requirements
- Secure employee information handling

**Performance Constraints:**
- Must load quickly on government network infrastructure
- Support for older browsers used in municipal environments
- Efficient data usage for mobile access

**Browser/Device Support:**
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile devices (iOS Safari, Android Chrome)
- Basic accessibility for screen readers
```

### **Story ID Prefix (Optional)**
```
ONBOARD
```

### **Special Agent Instructions**
- ✅ **Game Designer Focus** - Simple, clear visual design suitable for all ages
- ✅ **QA Focus** - Test with real municipal employee scenarios

### **Additional Context & Resources**
```
**Visual References:** 
- Clean, professional design similar to government websites
- Simple iconography for department representation
- Clear progress indicators

**Related Research:** 
- Municipal HR onboarding best practices
- Swedish government digital accessibility standards
- Employee feedback on current manual onboarding process

**Similar Features:** 
- Standard corporate onboarding modules but adapted for municipal context
- Focus on public sector values and procedures

**Stakeholder Input:** 
- HR department requires tracking completion rates
- IT department needs simple maintenance and updates
- New employees want self-paced, clear guidance
```

---

## 🚀 Instruktioner för att skapa GitHub Issue:

1. **Gå till:** https://github.com/jhonnyo88/diginativa-game/issues/new
2. **Välj:** "🚀 Feature Request (DigiNativa AI Team)" template
3. **Fyll i formuläret** med informationen ovan
4. **Klicka "Submit new issue"**
5. **Kopiera URL:en** till den nya issuen

### Test med AI Team:
```bash
# Sätt din GitHub token i .env först
source .env
python start_production_pipeline.py https://github.com/jhonnyo88/diginativa-game/issues/NUMMER
```

---

## 📊 Förväntade Resultat:

- **Project Manager:** DNA validering + story breakdown (30 min)
- **Game Designer:** UX spec med Shadcn/UI komponenter (2-4 tim)
- **Developer:** React + FastAPI implementation (4-8 tim)
- **Test Engineer:** 100% test coverage (2 tim)
- **QA Tester:** Anna persona validering (1-2 tim)
- **Quality Reviewer:** Production godkännande (30 min)

**Total tid:** ~1-2 dagar för komplett implementation

Detta blir vår första riktiga test av hela DigiNativa AI Team pipeline! 🎉