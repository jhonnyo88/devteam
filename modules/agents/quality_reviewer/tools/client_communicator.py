"""
Client Communicator - Professional Swedish municipal communication for Quality Reviewer.

Handles GitHub approval requests, quality reporting, and feedback communication
specifically designed for Swedish municipal training coordinators like Anna.

REVENUE IMPACT:
- Ensures professional client communication maintaining trust
- Provides transparent quality reporting building confidence  
- Automates approval workflow reducing manual overhead
- Creates feedback loop for continuous client satisfaction
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pathlib import Path


class ClientCommunicator:
    """
    Professional client communication for Swedish municipal contexts.
    
    Specializes in:
    - GitHub approval workflow automation
    - Professional Swedish municipal quality reporting
    - Rejection feedback with actionable improvement plans
    - Staging environment coordination
    """
    
    def __init__(self):
        """Initialize client communicator."""
        self.logger = logging.getLogger(f"{__name__}.ClientCommunicator")
        
        # Swedish municipal communication templates
        self.communication_templates = {
            "approval_request": {
                "title_sv": "Godkännande begärs: {feature_name} (Kvalitetspoäng: {quality_score})",
                "title_en": "Approval Requested: {feature_name} (Quality Score: {quality_score})"
            },
            "rejection_feedback": {
                "title_sv": "Kvalitetsgranskning - Förbättringar krävs: {feature_name}",
                "title_en": "Quality Review - Improvements Required: {feature_name}"
            }
        }
        
        # Quality categories for Swedish municipalities
        self.municipal_quality_categories = {
            "accessibility": "Tillgänglighet (WCAG)",
            "performance": "Prestanda", 
            "security": "Säkerhet",
            "usability": "Användarvänlighet",
            "pedagogical": "Pedagogisk effektivitet",
            "compliance": "Regelefterlevnad"
        }
        
        self.logger.info("ClientCommunicator initialized for Swedish municipal communication")
    
    async def create_approval_request(self, story_id: str, quality_analysis: Dict[str, Any], 
                                    deployment_readiness: Dict[str, Any], staging_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Create professional GitHub approval request for Swedish municipal client.
        
        Args:
            story_id: Story identifier
            quality_analysis: Complete quality analysis results
            deployment_readiness: Deployment readiness validation
            staging_url: Optional staging environment URL
            
        Returns:
            GitHub approval request data
        """
        try:
            self.logger.info(f"Creating approval request for {story_id}")
            
            # Extract key metrics
            overall_score = quality_analysis.get("overall_score", 0)
            feature_name = self._extract_feature_name(story_id)
            
            # Generate approval request content
            approval_content = await self._generate_approval_request_content(
                story_id, quality_analysis, deployment_readiness, staging_url
            )
            
            # Create GitHub issue data
            github_request = {
                "title": self.communication_templates["approval_request"]["title_sv"].format(
                    feature_name=feature_name,
                    quality_score=f"{overall_score:.1f}/100"
                ),
                "body": approval_content,
                "labels": [
                    "approval-request",
                    "quality-reviewed", 
                    f"score-{int(overall_score//10)*10}",  # score-90, score-80, etc.
                    "municipal-ready"
                ],
                "assignees": [],  # Will be populated with project owner
                "project_data": {
                    "story_id": story_id,
                    "quality_score": overall_score,
                    "staging_url": staging_url,
                    "approval_deadline": self._calculate_approval_deadline(),
                    "deployment_ready": deployment_readiness.get("deployment_ready", False)
                }
            }
            
            self.logger.info(f"Approval request created for {story_id} with score {overall_score}")
            return github_request
            
        except Exception as e:
            self.logger.error(f"Failed to create approval request for {story_id}: {e}")
            raise
    
    async def handle_rejection_feedback(self, story_id: str, quality_issues: List[Dict[str, Any]], 
                                      recommendations: List[str], blocking_issues: List[str]) -> Dict[str, Any]:
        """
        Handle rejection feedback with professional Swedish municipal communication.
        
        Args:
            story_id: Story identifier
            quality_issues: List of quality issues found
            recommendations: Improvement recommendations
            blocking_issues: Critical blocking issues
            
        Returns:
            Rejection feedback data
        """
        try:
            self.logger.info(f"Creating rejection feedback for {story_id}")
            
            feature_name = self._extract_feature_name(story_id)
            
            # Generate rejection feedback content
            feedback_content = await self._generate_rejection_feedback_content(
                story_id, quality_issues, recommendations, blocking_issues
            )
            
            # Create improvement plan
            improvement_plan = await self._create_improvement_plan(
                quality_issues, recommendations, blocking_issues
            )
            
            # Create GitHub comment/issue data
            rejection_feedback = {
                "title": self.communication_templates["rejection_feedback"]["title_sv"].format(
                    feature_name=feature_name
                ),
                "body": feedback_content,
                "labels": [
                    "quality-rejected",
                    "improvements-needed",
                    "municipal-feedback"
                ],
                "improvement_plan": improvement_plan,
                "project_data": {
                    "story_id": story_id,
                    "rejection_reason": "quality_standards_not_met",
                    "critical_issues_count": len(blocking_issues),
                    "estimated_fix_time": self._estimate_fix_time(quality_issues),
                    "next_review_suggested": self._suggest_next_review_date()
                }
            }
            
            self.logger.info(f"Rejection feedback created for {story_id}")
            return rejection_feedback
            
        except Exception as e:
            self.logger.error(f"Failed to create rejection feedback for {story_id}: {e}")
            raise
    
    async def generate_quality_report(self, story_id: str, quality_analysis: Dict[str, Any], 
                                    deployment_readiness: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate professional Swedish municipal quality report.
        
        Args:
            story_id: Story identifier
            quality_analysis: Complete quality analysis
            deployment_readiness: Deployment readiness validation
            
        Returns:
            Professional quality report
        """
        try:
            self.logger.info(f"Generating quality report for {story_id}")
            
            # Generate report sections
            report_sections = {
                "executive_summary": await self._generate_executive_summary(quality_analysis),
                "quality_metrics": await self._generate_quality_metrics_section(quality_analysis),
                "compliance_status": await self._generate_compliance_section(deployment_readiness),
                "recommendations": await self._generate_recommendations_section(quality_analysis),
                "next_steps": await self._generate_next_steps_section(quality_analysis, deployment_readiness)
            }
            
            # Create full report
            quality_report = {
                "report_id": f"QR-{story_id}-{datetime.now().strftime('%Y%m%d')}",
                "story_id": story_id,
                "generated_date": datetime.now(timezone.utc).isoformat(),
                "report_language": "sv",
                "target_audience": "swedish_municipal_coordinators",
                "sections": report_sections,
                "metadata": {
                    "overall_score": quality_analysis.get("overall_score", 0),
                    "deployment_ready": deployment_readiness.get("deployment_ready", False),
                    "reviewer_agent": "quality_reviewer",
                    "compliance_level": self._determine_compliance_level(quality_analysis)
                }
            }
            
            self.logger.info(f"Quality report generated for {story_id}")
            return quality_report
            
        except Exception as e:
            self.logger.error(f"Failed to generate quality report for {story_id}: {e}")
            raise
    
    async def create_staging_notification(self, story_id: str, staging_url: str, 
                                        quality_score: float, test_instructions: List[str]) -> Dict[str, Any]:
        """
        Create staging environment notification for client testing.
        
        Args:
            story_id: Story identifier
            staging_url: Staging environment URL
            quality_score: Overall quality score
            test_instructions: Testing instructions for client
            
        Returns:
            Staging notification data
        """
        try:
            self.logger.info(f"Creating staging notification for {story_id}")
            
            feature_name = self._extract_feature_name(story_id)
            
            # Generate staging notification content
            notification_content = await self._generate_staging_notification_content(
                story_id, feature_name, staging_url, quality_score, test_instructions
            )
            
            staging_notification = {
                "title": f"Testversion redo: {feature_name} (Kvalitet: {quality_score:.1f}/100)",
                "body": notification_content,
                "labels": [
                    "staging-ready",
                    "client-testing",
                    "municipal-review"
                ],
                "staging_data": {
                    "story_id": story_id,
                    "staging_url": staging_url,
                    "quality_score": quality_score,
                    "test_deadline": self._calculate_test_deadline(),
                    "contact_support": "quality.reviewer@digitativa.se"
                }
            }
            
            self.logger.info(f"Staging notification created for {story_id}")
            return staging_notification
            
        except Exception as e:
            self.logger.error(f"Failed to create staging notification for {story_id}: {e}")
            raise
    
    async def _generate_approval_request_content(self, story_id: str, quality_analysis: Dict[str, Any],
                                               deployment_readiness: Dict[str, Any], staging_url: Optional[str]) -> str:
        """Generate professional approval request content in Swedish."""
        overall_score = quality_analysis.get("overall_score", 0)
        readiness_score = deployment_readiness.get("readiness_score", 0)
        
        content_parts = [
            "# 🎯 Godkännande Begärs - Funktionen är Klar för Driftsättning",
            "",
            f"**Story ID:** {story_id}",
            f"**Övergripande Kvalitetspoäng:** {overall_score:.1f}/100 ⭐",
            f"**Driftsättningsberedskap:** {readiness_score:.1f}/100 ✅",
            "",
            "## 📊 Kvalitetssammanfattning",
            "",
            "### Kvalitetsdimensioner:"
        ]
        
        # Add quality dimensions
        for dimension, analysis in quality_analysis.items():
            if isinstance(analysis, dict) and "score" in analysis:
                swedish_name = self.municipal_quality_categories.get(dimension, dimension.replace("_", " ").title())
                score = analysis["score"]
                status_emoji = "✅" if score >= 85 else "⚠️" if score >= 70 else "❌"
                content_parts.append(f"- **{swedish_name}:** {score:.1f}/100 {status_emoji}")
        
        content_parts.extend([
            "",
            "## 🛡️ Regelefterlevnad & Säkerhet",
            ""
        ])
        
        # Add compliance status
        readiness_checks = deployment_readiness.get("readiness_checks", {})
        for check_name, check_result in readiness_checks.items():
            passed = check_result.get("passed", False)
            status_emoji = "✅" if passed else "❌"
            check_swedish = self._translate_check_name(check_name)
            content_parts.append(f"- **{check_swedish}:** {status_emoji}")
        
        # Add staging URL if available
        if staging_url:
            content_parts.extend([
                "",
                "## 🔗 Testmiljö",
                "",
                f"**Staging URL:** {staging_url}",
                "",
                "### Testinstruktioner:",
                "1. Logga in med dina testuppgifter",
                "2. Testa grundläggande användarflöden",
                "3. Kontrollera att funktionen fungerar som förväntat",
                "4. Rapportera eventuella problem direkt i detta ärende"
            ])
        
        content_parts.extend([
            "",
            "## ✅ Rekommendation",
            "",
            "Kvalitetsgranskningsteamet rekommenderar **GODKÄNNANDE** för driftsättning.",
            "",
            "Funktionen uppfyller alla kvalitetsstandarder för svenska kommunala miljöer.",
            "",
            "---",
            "",
            "**För att godkänna:** Kommentera med `@digitativa approve`",
            "**För att avslå:** Kommentera med `@digitativa reject` och beskriv anledning",
            "",
            "*Detta ärende är automatiskt genererat av DigiNativa AI Quality Reviewer*"
        ])
        
        return "\n".join(content_parts)
    
    async def _generate_rejection_feedback_content(self, story_id: str, quality_issues: List[Dict[str, Any]],
                                                 recommendations: List[str], blocking_issues: List[str]) -> str:
        """Generate professional rejection feedback content in Swedish."""
        content_parts = [
            "# ⚠️ Kvalitetsgranskning - Förbättringar Krävs",
            "",
            f"**Story ID:** {story_id}",
            f"**Granskningsdatum:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 🚫 Orsak till Avslag",
            "",
            "Funktionen uppfyller tyvärr inte DigiNativas kvalitetsstandarder för svenska kommunala miljöer.",
            ""
        ]
        
        # Add blocking issues
        if blocking_issues:
            content_parts.extend([
                "### Kritiska Problem (måste åtgärdas):",
                ""
            ])
            for issue in blocking_issues:
                content_parts.append(f"- ❌ {issue}")
            content_parts.append("")
        
        # Add quality issues by category
        if quality_issues:
            content_parts.extend([
                "### Kvalitetsproblem per Kategori:",
                ""
            ])
            
            issues_by_category = {}
            for issue in quality_issues:
                category = issue.get("category", "general")
                if category not in issues_by_category:
                    issues_by_category[category] = []
                issues_by_category[category].append(issue)
            
            for category, category_issues in issues_by_category.items():
                swedish_category = self.municipal_quality_categories.get(category, category.replace("_", " ").title())
                content_parts.append(f"#### {swedish_category}:")
                for issue in category_issues:
                    severity_emoji = "🔴" if issue.get("blocking") else "🟡"
                    content_parts.append(f"- {severity_emoji} {issue.get('message', 'Okänt problem')}")
                content_parts.append("")
        
        # Add recommendations
        if recommendations:
            content_parts.extend([
                "## 💡 Rekommendationer för Förbättring",
                ""
            ])
            for i, recommendation in enumerate(recommendations, 1):
                content_parts.append(f"{i}. {recommendation}")
            content_parts.append("")
        
        content_parts.extend([
            "## 📋 Nästa Steg",
            "",
            "1. **Utvecklingsteamet** åtgärdar identifierade problem",
            "2. **Ny kvalitetsgranskning** begärs när förbättringarna är klara",
            "3. **Automatisk testning** körs för att verifiera förbättringar",
            "",
            "### Uppskattat Förbättringstid:",
            f"**{self._estimate_fix_time(quality_issues)} arbetsdagar**",
            "",
            "---",
            "",
            "**För frågor:** Kontakta quality.reviewer@digitativa.se",
            "",
            "*Detta feedback är automatiskt genererat av DigiNativa AI Quality Reviewer*"
        ])
        
        return "\n".join(content_parts)
    
    async def _generate_executive_summary(self, quality_analysis: Dict[str, Any]) -> str:
        """Generate executive summary in Swedish for municipal coordinators."""
        overall_score = quality_analysis.get("overall_score", 0)
        
        if overall_score >= 90:
            summary = f"Funktionen har uppnått utmärkt kvalitet ({overall_score:.1f}/100) och är redo för driftsättning i kommunala miljöer."
        elif overall_score >= 80:
            summary = f"Funktionen har god kvalitet ({overall_score:.1f}/100) med mindre förbättringsområden."
        else:
            summary = f"Funktionen behöver betydande förbättringar ({overall_score:.1f}/100) innan driftsättning."
        
        return summary
    
    async def _generate_quality_metrics_section(self, quality_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed quality metrics section."""
        metrics = {}
        
        for dimension, analysis in quality_analysis.items():
            if isinstance(analysis, dict) and "score" in analysis:
                swedish_name = self.municipal_quality_categories.get(dimension, dimension.replace("_", " ").title())
                metrics[swedish_name] = {
                    "score": analysis["score"],
                    "status": "Godkänd" if analysis["score"] >= 85 else "Behöver förbättring",
                    "issues": analysis.get("issues", [])
                }
        
        return metrics
    
    async def _generate_compliance_section(self, deployment_readiness: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance status section."""
        compliance = {}
        
        readiness_checks = deployment_readiness.get("readiness_checks", {})
        for check_name, check_result in readiness_checks.items():
            swedish_name = self._translate_check_name(check_name)
            compliance[swedish_name] = {
                "status": "Uppfylld" if check_result.get("passed", False) else "Ej uppfylld",
                "details": check_result.get("issues", [])
            }
        
        return compliance
    
    async def _generate_recommendations_section(self, quality_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations section."""
        recommendations = []
        
        # Collect recommendations from all quality dimensions
        for dimension, analysis in quality_analysis.items():
            if isinstance(analysis, dict) and "recommendations" in analysis:
                recommendations.extend(analysis["recommendations"])
        
        return list(set(recommendations))  # Remove duplicates
    
    async def _generate_next_steps_section(self, quality_analysis: Dict[str, Any], 
                                         deployment_readiness: Dict[str, Any]) -> List[str]:
        """Generate next steps section."""
        overall_score = quality_analysis.get("overall_score", 0)
        deployment_ready = deployment_readiness.get("deployment_ready", False)
        
        if deployment_ready and overall_score >= 90:
            return [
                "Godkänn funktionen för driftsättning",
                "Övervaka prestanda efter driftsättning",
                "Samla användarfeedback från kommunala medarbetare"
            ]
        else:
            return [
                "Åtgärda identifierade kvalitetsproblem",
                "Begär ny kvalitetsgranskning",
                "Testa förbättringar i staging-miljö"
            ]
    
    async def _generate_staging_notification_content(self, story_id: str, feature_name: str, 
                                                   staging_url: str, quality_score: float, 
                                                   test_instructions: List[str]) -> str:
        """Generate staging notification content."""
        content_parts = [
            f"# 🧪 Testversion Redo: {feature_name}",
            "",
            f"**Story ID:** {story_id}",
            f"**Kvalitetspoäng:** {quality_score:.1f}/100",
            f"**Staging URL:** {staging_url}",
            "",
            "## 🎯 Testinstruktioner",
            ""
        ]
        
        for i, instruction in enumerate(test_instructions, 1):
            content_parts.append(f"{i}. {instruction}")
        
        content_parts.extend([
            "",
            "## ⏰ Testperiod",
            "",
            f"**Testdeadline:** {self._calculate_test_deadline()}",
            "",
            "## 📞 Support",
            "",
            "Vid tekniska problem, kontakta: quality.reviewer@digitativa.se",
            "",
            "---",
            "",
            "*Automatiskt genererat av DigiNativa AI Quality Reviewer*"
        ])
        
        return "\n".join(content_parts)
    
    async def _create_improvement_plan(self, quality_issues: List[Dict[str, Any]], 
                                     recommendations: List[str], blocking_issues: List[str]) -> Dict[str, Any]:
        """Create structured improvement plan."""
        return {
            "priority_1_critical": blocking_issues,
            "priority_2_quality": [issue.get("message", "") for issue in quality_issues if issue.get("blocking", False)],
            "priority_3_improvements": [issue.get("message", "") for issue in quality_issues if not issue.get("blocking", False)],
            "recommendations": recommendations,
            "estimated_completion": self._estimate_fix_time(quality_issues)
        }
    
    def _extract_feature_name(self, story_id: str) -> str:
        """Extract readable feature name from story ID."""
        # Convert STORY-001-001 to "Funktionalitet 001-001"
        if story_id.startswith("STORY-"):
            return f"Funktionalitet {story_id[6:]}"
        return story_id
    
    def _translate_check_name(self, check_name: str) -> str:
        """Translate check names to Swedish."""
        translations = {
            "performance": "Prestanda",
            "security": "Säkerhet", 
            "accessibility": "Tillgänglighet",
            "dna_compliance": "DNA-efterlevnad",
            "test_coverage": "Testtäckning",
            "compatibility": "Kompatibilitet"
        }
        return translations.get(check_name, check_name.replace("_", " ").title())
    
    def _calculate_approval_deadline(self) -> str:
        """Calculate approval deadline (5 business days)."""
        from datetime import timedelta
        deadline = datetime.now() + timedelta(days=7)  # 1 week for approval
        return deadline.strftime("%Y-%m-%d")
    
    def _calculate_test_deadline(self) -> str:
        """Calculate test deadline (3 business days)."""
        from datetime import timedelta
        deadline = datetime.now() + timedelta(days=5)  # 5 days for testing
        return deadline.strftime("%Y-%m-%d")
    
    def _estimate_fix_time(self, quality_issues: List[Dict[str, Any]]) -> str:
        """Estimate fix time based on quality issues."""
        critical_issues = len([issue for issue in quality_issues if issue.get("blocking", False)])
        other_issues = len(quality_issues) - critical_issues
        
        # Simple estimation: critical = 2 days, others = 0.5 days
        total_days = (critical_issues * 2) + (other_issues * 0.5)
        
        if total_days <= 1:
            return "1"
        elif total_days <= 3:
            return "2-3"
        elif total_days <= 5:
            return "3-5"
        else:
            return "5+"
    
    def _suggest_next_review_date(self) -> str:
        """Suggest next review date."""
        from datetime import timedelta
        next_review = datetime.now() + timedelta(days=3)  # 3 days for fixes
        return next_review.strftime("%Y-%m-%d")
    
    def _determine_compliance_level(self, quality_analysis: Dict[str, Any]) -> str:
        """Determine compliance level for municipal requirements."""
        overall_score = quality_analysis.get("overall_score", 0)
        
        if overall_score >= 95:
            return "exemplary"
        elif overall_score >= 90:
            return "excellent"  
        elif overall_score >= 80:
            return "good"
        elif overall_score >= 70:
            return "acceptable"
        else:
            return "insufficient"