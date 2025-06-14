"""
AccessibilityChecker - WCAG compliance validation and accessibility testing tool.

PURPOSE:
Validates that implemented features comply with WCAG AA accessibility standards
and provide excellent experience for users with disabilities.

CRITICAL FUNCTIONALITY:
- WCAG 2.1 Level AA compliance validation
- Screen reader compatibility testing
- Keyboard navigation verification
- Color contrast ratio validation
- Alternative text and labeling checks
- Focus management assessment

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update wcag_standards for your compliance requirements
2. Modify accessibility_tests for your specific needs
3. Adjust compliance_thresholds for your quality standards
4. Update assistive_technology_support for your requirements

CONTRACT PROTECTION:
This tool is critical for DigiNativa's accessibility compliance.
Changes must maintain WCAG AA compliance standards.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path


# Setup logging for this module
logger = logging.getLogger(__name__)


@dataclass
class AccessibilityViolation:
    """
    Represents an accessibility compliance violation.
    """
    violation_id: str
    wcag_criterion: str
    severity_level: str  # "critical", "serious", "moderate", "minor"
    component_affected: str
    description: str
    recommended_fix: str
    compliance_level: str  # "A", "AA", "AAA"
    automated_detection: bool
    manual_verification_needed: bool


@dataclass
class AccessibilityTestResult:
    """
    Results from accessibility testing.
    """
    test_name: str
    passed: bool
    score: float  # 0-100 percentage
    violations: List[AccessibilityViolation]
    recommendations: List[str]
    details: Dict[str, Any]


class AccessibilityChecker:
    """
    Validates WCAG compliance and accessibility standards for implemented features.
    
    Focuses on WCAG 2.1 Level AA compliance which is required for
    Swedish public sector digital services.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize AccessibilityChecker.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # WCAG 2.1 Level AA requirements (Swedish public sector standard)
        self.wcag_aa_criteria = {
            # Perceivable
            "1.1.1": {
                "name": "Non-text Content",
                "description": "All non-text content has text alternatives",
                "level": "A",
                "automated": True
            },
            "1.2.1": {
                "name": "Audio-only and Video-only (Prerecorded)",
                "description": "Alternatives for time-based media",
                "level": "A",
                "automated": False
            },
            "1.2.2": {
                "name": "Captions (Prerecorded)",
                "description": "Captions for videos with audio",
                "level": "A",
                "automated": False
            },
            "1.3.1": {
                "name": "Info and Relationships",
                "description": "Information structure can be programmatically determined",
                "level": "A",
                "automated": True
            },
            "1.3.2": {
                "name": "Meaningful Sequence",
                "description": "Content order makes sense when presented sequentially",
                "level": "A",
                "automated": True
            },
            "1.3.3": {
                "name": "Sensory Characteristics",
                "description": "Instructions don't rely solely on sensory characteristics",
                "level": "A",
                "automated": False
            },
            "1.4.1": {
                "name": "Use of Color",
                "description": "Color is not the only means of conveying information",
                "level": "A",
                "automated": True
            },
            "1.4.2": {
                "name": "Audio Control",
                "description": "Audio can be paused or stopped",
                "level": "A",
                "automated": False
            },
            "1.4.3": {
                "name": "Contrast (Minimum)",
                "description": "Text has contrast ratio of at least 4.5:1",
                "level": "AA",
                "automated": True
            },
            "1.4.4": {
                "name": "Resize text",
                "description": "Text can be resized up to 200% without loss of functionality",
                "level": "AA",
                "automated": True
            },
            "1.4.5": {
                "name": "Images of Text",
                "description": "Text is used rather than images of text",
                "level": "AA",
                "automated": True
            },
            
            # Operable
            "2.1.1": {
                "name": "Keyboard",
                "description": "All functionality available via keyboard",
                "level": "A",
                "automated": True
            },
            "2.1.2": {
                "name": "No Keyboard Trap",
                "description": "Keyboard focus is not trapped",
                "level": "A",
                "automated": True
            },
            "2.2.1": {
                "name": "Timing Adjustable",
                "description": "Time limits can be extended or disabled",
                "level": "A",
                "automated": False
            },
            "2.2.2": {
                "name": "Pause, Stop, Hide",
                "description": "Moving content can be controlled",
                "level": "A",
                "automated": False
            },
            "2.3.1": {
                "name": "Three Flashes or Below Threshold",
                "description": "No content flashes more than 3 times per second",
                "level": "A",
                "automated": False
            },
            "2.4.1": {
                "name": "Bypass Blocks",
                "description": "Skip links or other bypass mechanisms provided",
                "level": "A",
                "automated": True
            },
            "2.4.2": {
                "name": "Page Titled",
                "description": "Pages have descriptive titles",
                "level": "A",
                "automated": True
            },
            "2.4.3": {
                "name": "Focus Order",
                "description": "Focus order preserves meaning and operability",
                "level": "A",
                "automated": True
            },
            "2.4.4": {
                "name": "Link Purpose (In Context)",
                "description": "Link purpose can be determined from link text or context",
                "level": "A",
                "automated": True
            },
            "2.4.5": {
                "name": "Multiple Ways",
                "description": "Multiple ways to locate pages",
                "level": "AA",
                "automated": False
            },
            "2.4.6": {
                "name": "Headings and Labels",
                "description": "Headings and labels describe topic or purpose",
                "level": "AA",
                "automated": True
            },
            "2.4.7": {
                "name": "Focus Visible",
                "description": "Keyboard focus indicator is visible",
                "level": "AA",
                "automated": True
            },
            
            # Understandable
            "3.1.1": {
                "name": "Language of Page",
                "description": "Primary language of page can be programmatically determined",
                "level": "A",
                "automated": True
            },
            "3.1.2": {
                "name": "Language of Parts",
                "description": "Language of parts can be programmatically determined",
                "level": "AA",
                "automated": True
            },
            "3.2.1": {
                "name": "On Focus",
                "description": "No unexpected context changes on focus",
                "level": "A",
                "automated": False
            },
            "3.2.2": {
                "name": "On Input",
                "description": "No unexpected context changes on input",
                "level": "A",
                "automated": False
            },
            "3.2.3": {
                "name": "Consistent Navigation",
                "description": "Navigation is consistent across pages",
                "level": "AA",
                "automated": True
            },
            "3.2.4": {
                "name": "Consistent Identification",
                "description": "Components with same functionality identified consistently",
                "level": "AA",
                "automated": True
            },
            "3.3.1": {
                "name": "Error Identification",
                "description": "Errors are identified and described to users",
                "level": "A",
                "automated": True
            },
            "3.3.2": {
                "name": "Labels or Instructions",
                "description": "Labels or instructions provided for user input",
                "level": "A",
                "automated": True
            },
            "3.3.3": {
                "name": "Error Suggestion",
                "description": "Error correction suggestions provided",
                "level": "AA",
                "automated": False
            },
            "3.3.4": {
                "name": "Error Prevention (Legal, Financial, Data)",
                "description": "Error prevention for important submissions",
                "level": "AA",
                "automated": False
            },
            
            # Robust
            "4.1.1": {
                "name": "Parsing",
                "description": "Valid HTML markup",
                "level": "A",
                "automated": True
            },
            "4.1.2": {
                "name": "Name, Role, Value",
                "description": "UI components have accessible name, role, and value",
                "level": "A",
                "automated": True
            }
        }
        
        # Compliance thresholds
        self.compliance_thresholds = {
            "critical_violations": 0,  # No critical violations allowed
            "serious_violations": 2,   # Maximum 2 serious violations
            "moderate_violations": 5,  # Maximum 5 moderate violations
            "overall_score": 90        # Minimum 90% compliance score
        }
        
        # Color contrast requirements
        self.contrast_requirements = {
            "normal_text": 4.5,      # WCAG AA normal text
            "large_text": 3.0,       # WCAG AA large text (18pt+ or 14pt+ bold)
            "graphical_objects": 3.0, # WCAG AA non-text elements
            "enhanced_normal": 7.0,   # WCAG AAA normal text
            "enhanced_large": 4.5     # WCAG AAA large text
        }
        
        logger.info("AccessibilityChecker initialized with WCAG 2.1 Level AA standards")
    
    async def validate_accessibility(self, story_id: str, implementation_data: Dict[str, Any],
                                   wcag_level: str = "AA") -> Dict[str, Any]:
        """
        Validate accessibility compliance for implemented feature.
        
        Args:
            story_id: Story identifier
            implementation_data: Feature implementation details
            wcag_level: WCAG compliance level ("A", "AA", "AAA")
            
        Returns:
            Comprehensive accessibility validation results
        """
        try:
            logger.info(f"Starting WCAG {wcag_level} accessibility validation for story: {story_id}")
            
            # Extract components for testing
            ui_components = implementation_data.get("ui_components", [])
            html_structure = implementation_data.get("html_structure", {})
            css_styles = implementation_data.get("css_styles", {})
            
            # Run comprehensive accessibility tests
            test_results = []
            
            # 1. Automated WCAG tests
            logger.debug("Running automated WCAG compliance tests")
            automated_results = await self._run_automated_wcag_tests(
                ui_components, html_structure, css_styles, wcag_level
            )
            test_results.extend(automated_results)
            
            # 2. Color contrast validation
            logger.debug("Validating color contrast ratios")
            contrast_results = await self._validate_color_contrast(
                ui_components, css_styles
            )
            test_results.append(contrast_results)
            
            # 3. Keyboard navigation testing
            logger.debug("Testing keyboard navigation")
            keyboard_results = await self._test_keyboard_navigation(
                ui_components, html_structure
            )
            test_results.append(keyboard_results)
            
            # 4. Screen reader compatibility
            logger.debug("Testing screen reader compatibility")
            screen_reader_results = await self._test_screen_reader_compatibility(
                ui_components, html_structure
            )
            test_results.append(screen_reader_results)
            
            # 5. Focus management testing
            logger.debug("Testing focus management")
            focus_results = await self._test_focus_management(
                ui_components, html_structure
            )
            test_results.append(focus_results)
            
            # 6. Alternative text validation
            logger.debug("Validating alternative text")
            alt_text_results = await self._validate_alternative_text(
                ui_components
            )
            test_results.append(alt_text_results)
            
            # 7. Form accessibility testing
            logger.debug("Testing form accessibility")
            form_results = await self._test_form_accessibility(
                ui_components
            )
            test_results.append(form_results)
            
            # Calculate overall compliance
            compliance_summary = self._calculate_compliance_summary(test_results, wcag_level)
            
            # Generate detailed report
            accessibility_report = {
                "story_id": story_id,
                "wcag_level": wcag_level,
                "validation_timestamp": datetime.now().isoformat(),
                "compliance_summary": compliance_summary,
                "test_results": [result.__dict__ for result in test_results],
                "violations": self._collect_all_violations(test_results),
                "recommendations": await self._generate_accessibility_recommendations(test_results),
                "assistive_technology_support": await self._assess_assistive_technology_support(test_results),
                "compliance_score": compliance_summary.get("overall_score", 0),
                "certification_status": self._determine_certification_status(compliance_summary, wcag_level)
            }
            
            logger.info(f"Accessibility validation completed for story: {story_id}")
            return accessibility_report
            
        except Exception as e:
            error_msg = f"Accessibility validation failed for story {story_id}: {str(e)}"
            logger.error(error_msg)
            return {
                "error": error_msg,
                "story_id": story_id,
                "validation_failed": True,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _run_automated_wcag_tests(self, ui_components: List[Dict[str, Any]],
                                      html_structure: Dict[str, Any], css_styles: Dict[str, Any],
                                      wcag_level: str) -> List[AccessibilityTestResult]:
        """
        Run automated WCAG compliance tests.
        
        Args:
            ui_components: UI components to test
            html_structure: HTML structure data
            css_styles: CSS styling data
            wcag_level: WCAG compliance level
            
        Returns:
            List of automated test results
        """
        test_results = []
        
        # Filter criteria for the specified WCAG level
        target_criteria = {k: v for k, v in self.wcag_aa_criteria.items() 
                          if v["level"] in ["A"] + (["AA"] if wcag_level in ["AA", "AAA"] else []) +
                          (["AAA"] if wcag_level == "AAA" else [])}
        
        for criterion_id, criterion_info in target_criteria.items():
            if criterion_info["automated"]:
                test_result = await self._test_wcag_criterion(
                    criterion_id, criterion_info, ui_components, html_structure, css_styles
                )
                test_results.append(test_result)
        
        return test_results
    
    async def _test_wcag_criterion(self, criterion_id: str, criterion_info: Dict[str, Any],
                                 ui_components: List[Dict[str, Any]], html_structure: Dict[str, Any],
                                 css_styles: Dict[str, Any]) -> AccessibilityTestResult:
        """
        Test a specific WCAG criterion.
        
        Args:
            criterion_id: WCAG criterion ID (e.g., "1.1.1")
            criterion_info: Criterion information
            ui_components: UI components
            html_structure: HTML structure
            css_styles: CSS styles
            
        Returns:
            Test result for the criterion
        """
        violations = []
        passed = True
        score = 100.0
        recommendations = []
        
        try:
            # Test specific criteria
            if criterion_id == "1.1.1":  # Non-text Content
                violations.extend(await self._check_non_text_content(ui_components))
            elif criterion_id == "1.3.1":  # Info and Relationships
                violations.extend(await self._check_info_relationships(html_structure))
            elif criterion_id == "1.3.2":  # Meaningful Sequence
                violations.extend(await self._check_meaningful_sequence(html_structure))
            elif criterion_id == "1.4.1":  # Use of Color
                violations.extend(await self._check_color_usage(ui_components, css_styles))
            elif criterion_id == "2.1.1":  # Keyboard
                violations.extend(await self._check_keyboard_accessibility(ui_components))
            elif criterion_id == "2.1.2":  # No Keyboard Trap
                violations.extend(await self._check_keyboard_trap(ui_components))
            elif criterion_id == "2.4.1":  # Bypass Blocks
                violations.extend(await self._check_bypass_blocks(html_structure))
            elif criterion_id == "2.4.2":  # Page Titled
                violations.extend(await self._check_page_titles(html_structure))
            elif criterion_id == "2.4.3":  # Focus Order
                violations.extend(await self._check_focus_order(html_structure))
            elif criterion_id == "2.4.4":  # Link Purpose
                violations.extend(await self._check_link_purpose(ui_components))
            elif criterion_id == "2.4.6":  # Headings and Labels
                violations.extend(await self._check_headings_labels(html_structure))
            elif criterion_id == "2.4.7":  # Focus Visible
                violations.extend(await self._check_focus_visible(css_styles))
            elif criterion_id == "3.1.1":  # Language of Page
                violations.extend(await self._check_page_language(html_structure))
            elif criterion_id == "3.3.1":  # Error Identification
                violations.extend(await self._check_error_identification(ui_components))
            elif criterion_id == "3.3.2":  # Labels or Instructions
                violations.extend(await self._check_labels_instructions(ui_components))
            elif criterion_id == "4.1.1":  # Parsing
                violations.extend(await self._check_html_parsing(html_structure))
            elif criterion_id == "4.1.2":  # Name, Role, Value
                violations.extend(await self._check_name_role_value(ui_components))
            
            # Calculate score based on violations
            if violations:
                passed = False
                critical_count = len([v for v in violations if v.severity_level == "critical"])
                serious_count = len([v for v in violations if v.severity_level == "serious"])
                moderate_count = len([v for v in violations if v.severity_level == "moderate"])
                
                # Weighted scoring
                score_reduction = (critical_count * 30) + (serious_count * 15) + (moderate_count * 5)
                score = max(0, 100 - score_reduction)
            
            # Generate recommendations
            if violations:
                recommendations = [v.recommended_fix for v in violations]
            
            return AccessibilityTestResult(
                test_name=f"WCAG {criterion_id}: {criterion_info['name']}",
                passed=passed,
                score=score,
                violations=violations,
                recommendations=recommendations,
                details={
                    "criterion_id": criterion_id,
                    "wcag_level": criterion_info["level"],
                    "description": criterion_info["description"],
                    "automated": criterion_info["automated"]
                }
            )
            
        except Exception as e:
            logger.error(f"Error testing WCAG criterion {criterion_id}: {e}")
            return AccessibilityTestResult(
                test_name=f"WCAG {criterion_id}: {criterion_info['name']}",
                passed=False,
                score=0.0,
                violations=[AccessibilityViolation(
                    violation_id=f"{criterion_id}_error",
                    wcag_criterion=criterion_id,
                    severity_level="critical",
                    component_affected="system",
                    description=f"Testing error: {str(e)}",
                    recommended_fix="Fix testing system",
                    compliance_level=criterion_info["level"],
                    automated_detection=True,
                    manual_verification_needed=False
                )],
                recommendations=["Fix accessibility testing system"],
                details={"error": str(e)}
            )
    
    async def _validate_color_contrast(self, ui_components: List[Dict[str, Any]],
                                     css_styles: Dict[str, Any]) -> AccessibilityTestResult:
        """
        Validate color contrast ratios according to WCAG standards.
        
        Args:
            ui_components: UI components to check
            css_styles: CSS styling information
            
        Returns:
            Color contrast test result
        """
        violations = []
        text_elements = [comp for comp in ui_components if comp.get("type") in ["text", "label", "button", "link"]]
        
        for element in text_elements:
            # Extract color information (simplified - would use actual color extraction in real implementation)
            foreground_color = element.get("color", "#000000")
            background_color = element.get("background_color", "#ffffff")
            font_size = element.get("font_size", "16px")
            font_weight = element.get("font_weight", "normal")
            
            # Calculate contrast ratio (simplified calculation)
            contrast_ratio = self._calculate_contrast_ratio(foreground_color, background_color)
            
            # Determine required contrast based on text size
            is_large_text = self._is_large_text(font_size, font_weight)
            required_contrast = self.contrast_requirements["large_text"] if is_large_text else self.contrast_requirements["normal_text"]
            
            if contrast_ratio < required_contrast:
                violations.append(AccessibilityViolation(
                    violation_id=f"contrast_{element.get('id', 'unknown')}",
                    wcag_criterion="1.4.3",
                    severity_level="serious",
                    component_affected=element.get("type", "text"),
                    description=f"Insufficient color contrast ratio: {contrast_ratio:.2f} (required: {required_contrast})",
                    recommended_fix=f"Increase contrast ratio to at least {required_contrast}:1",
                    compliance_level="AA",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
        
        passed = len(violations) == 0
        score = 100 - (len(violations) * 15)  # Deduct 15 points per violation
        
        return AccessibilityTestResult(
            test_name="Color Contrast Validation",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "elements_tested": len(text_elements),
                "contrast_violations": len(violations),
                "minimum_required_contrast": self.contrast_requirements["normal_text"]
            }
        )
    
    async def _test_keyboard_navigation(self, ui_components: List[Dict[str, Any]],
                                      html_structure: Dict[str, Any]) -> AccessibilityTestResult:
        """
        Test keyboard navigation accessibility.
        
        Args:
            ui_components: UI components to test
            html_structure: HTML structure
            
        Returns:
            Keyboard navigation test result
        """
        violations = []
        interactive_elements = [comp for comp in ui_components 
                              if comp.get("type") in ["button", "link", "input", "select", "textarea"]]
        
        for element in interactive_elements:
            # Check if element is keyboard accessible
            if not element.get("keyboard_accessible", True):
                violations.append(AccessibilityViolation(
                    violation_id=f"keyboard_{element.get('id', 'unknown')}",
                    wcag_criterion="2.1.1",
                    severity_level="critical",
                    component_affected=element.get("type", "element"),
                    description=f"{element.get('type', 'Element')} is not keyboard accessible",
                    recommended_fix="Ensure element can be operated via keyboard",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=True
                ))
            
            # Check for proper tabindex usage
            tabindex = element.get("tabindex")
            if tabindex and int(tabindex) > 0:
                violations.append(AccessibilityViolation(
                    violation_id=f"tabindex_{element.get('id', 'unknown')}",
                    wcag_criterion="2.4.3",
                    severity_level="moderate",
                    component_affected=element.get("type", "element"),
                    description="Positive tabindex values can disrupt natural tab order",
                    recommended_fix="Use tabindex='0' or remove tabindex to follow natural tab order",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
        
        passed = len(violations) == 0
        score = 100 - (len([v for v in violations if v.severity_level == "critical"]) * 25) - \
                (len([v for v in violations if v.severity_level == "moderate"]) * 10)
        
        return AccessibilityTestResult(
            test_name="Keyboard Navigation Testing",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "interactive_elements_tested": len(interactive_elements),
                "keyboard_violations": len(violations)
            }
        )
    
    async def _test_screen_reader_compatibility(self, ui_components: List[Dict[str, Any]],
                                              html_structure: Dict[str, Any]) -> AccessibilityTestResult:
        """
        Test screen reader compatibility.
        
        Args:
            ui_components: UI components to test
            html_structure: HTML structure
            
        Returns:
            Screen reader compatibility test result
        """
        violations = []
        
        # Check for proper semantic markup
        semantic_elements = html_structure.get("semantic_elements", [])
        if not semantic_elements:
            violations.append(AccessibilityViolation(
                violation_id="missing_semantic_markup",
                wcag_criterion="1.3.1",
                severity_level="serious",
                component_affected="page_structure",
                description="No semantic HTML elements detected",
                recommended_fix="Use semantic HTML elements (header, nav, main, section, etc.)",
                compliance_level="A",
                automated_detection=True,
                manual_verification_needed=False
            ))
        
        # Check for proper heading structure
        headings = [comp for comp in ui_components if comp.get("type") == "heading"]
        if headings:
            heading_levels = [int(h.get("level", "1").replace("h", "")) for h in headings]
            if heading_levels:
                # Check for proper heading hierarchy
                for i in range(1, len(heading_levels)):
                    if heading_levels[i] > heading_levels[i-1] + 1:
                        violations.append(AccessibilityViolation(
                            violation_id=f"heading_hierarchy_{i}",
                            wcag_criterion="1.3.1",
                            severity_level="moderate",
                            component_affected="heading_structure",
                            description="Heading levels skip numbers in hierarchy",
                            recommended_fix="Use proper heading hierarchy (h1, h2, h3, etc.)",
                            compliance_level="A",
                            automated_detection=True,
                            manual_verification_needed=False
                        ))
        
        # Check for proper ARIA labels
        for component in ui_components:
            if component.get("type") in ["button", "link", "input"]:
                aria_label = component.get("aria_label")
                accessible_name = component.get("accessible_name")
                
                if not aria_label and not accessible_name and not component.get("text_content"):
                    violations.append(AccessibilityViolation(
                        violation_id=f"missing_aria_label_{component.get('id', 'unknown')}",
                        wcag_criterion="4.1.2",
                        severity_level="serious",
                        component_affected=component.get("type", "element"),
                        description="Interactive element lacks accessible name",
                        recommended_fix="Add aria-label or ensure element has visible text",
                        compliance_level="A",
                        automated_detection=True,
                        manual_verification_needed=False
                    ))
        
        passed = len(violations) == 0
        score = 100 - (len([v for v in violations if v.severity_level == "serious"]) * 20) - \
                (len([v for v in violations if v.severity_level == "moderate"]) * 10)
        
        return AccessibilityTestResult(
            test_name="Screen Reader Compatibility",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "semantic_elements_count": len(semantic_elements),
                "heading_count": len(headings),
                "screen_reader_violations": len(violations)
            }
        )
    
    async def _test_focus_management(self, ui_components: List[Dict[str, Any]],
                                   html_structure: Dict[str, Any]) -> AccessibilityTestResult:
        """
        Test focus management and visibility.
        
        Args:
            ui_components: UI components to test
            html_structure: HTML structure
            
        Returns:
            Focus management test result
        """
        violations = []
        focusable_elements = [comp for comp in ui_components 
                            if comp.get("focusable", False)]
        
        for element in focusable_elements:
            # Check for visible focus indicator
            focus_visible = element.get("focus_visible", False)
            if not focus_visible:
                violations.append(AccessibilityViolation(
                    violation_id=f"focus_visible_{element.get('id', 'unknown')}",
                    wcag_criterion="2.4.7",
                    severity_level="serious",
                    component_affected=element.get("type", "element"),
                    description="Focusable element lacks visible focus indicator",
                    recommended_fix="Add visible focus indicator (outline, border, etc.)",
                    compliance_level="AA",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
        
        passed = len(violations) == 0
        score = 100 - (len(violations) * 15)
        
        return AccessibilityTestResult(
            test_name="Focus Management Testing",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "focusable_elements": len(focusable_elements),
                "focus_violations": len(violations)
            }
        )
    
    async def _validate_alternative_text(self, ui_components: List[Dict[str, Any]]) -> AccessibilityTestResult:
        """
        Validate alternative text for images and non-text content.
        
        Args:
            ui_components: UI components to check
            
        Returns:
            Alternative text validation result
        """
        violations = []
        images = [comp for comp in ui_components if comp.get("type") in ["image", "icon", "graphic"]]
        
        for image in images:
            alt_text = image.get("alt_text", "")
            if not alt_text and not image.get("decorative", False):
                violations.append(AccessibilityViolation(
                    violation_id=f"missing_alt_{image.get('id', 'unknown')}",
                    wcag_criterion="1.1.1",
                    severity_level="serious",
                    component_affected="image",
                    description="Image missing alternative text",
                    recommended_fix="Add meaningful alt text describing the image content",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
            elif alt_text and len(alt_text.strip()) < 3:
                violations.append(AccessibilityViolation(
                    violation_id=f"inadequate_alt_{image.get('id', 'unknown')}",
                    wcag_criterion="1.1.1",
                    severity_level="moderate",
                    component_affected="image",
                    description="Alternative text too brief to be meaningful",
                    recommended_fix="Provide more descriptive alternative text",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=True
                ))
        
        passed = len(violations) == 0
        score = 100 - (len([v for v in violations if v.severity_level == "serious"]) * 20) - \
                (len([v for v in violations if v.severity_level == "moderate"]) * 10)
        
        return AccessibilityTestResult(
            test_name="Alternative Text Validation",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "images_tested": len(images),
                "alt_text_violations": len(violations)
            }
        )
    
    async def _test_form_accessibility(self, ui_components: List[Dict[str, Any]]) -> AccessibilityTestResult:
        """
        Test form accessibility compliance.
        
        Args:
            ui_components: UI components to test
            
        Returns:
            Form accessibility test result
        """
        violations = []
        form_elements = [comp for comp in ui_components 
                        if comp.get("type") in ["input", "select", "textarea", "checkbox", "radio"]]
        
        for element in form_elements:
            # Check for associated labels
            label = element.get("label")
            aria_label = element.get("aria_label")
            aria_labelledby = element.get("aria_labelledby")
            
            if not label and not aria_label and not aria_labelledby:
                violations.append(AccessibilityViolation(
                    violation_id=f"missing_label_{element.get('id', 'unknown')}",
                    wcag_criterion="3.3.2",
                    severity_level="serious",
                    component_affected="form_input",
                    description="Form input missing associated label",
                    recommended_fix="Add label element or aria-label attribute",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
            
            # Check for required field indicators
            if element.get("required", False):
                required_indicator = element.get("required_indicator")
                if not required_indicator:
                    violations.append(AccessibilityViolation(
                        violation_id=f"missing_required_indicator_{element.get('id', 'unknown')}",
                        wcag_criterion="3.3.2",
                        severity_level="moderate",
                        component_affected="form_input",
                        description="Required field lacks accessible indicator",
                        recommended_fix="Add aria-required='true' or visual required indicator",
                        compliance_level="A",
                        automated_detection=True,
                        manual_verification_needed=False
                    ))
        
        passed = len(violations) == 0
        score = 100 - (len([v for v in violations if v.severity_level == "serious"]) * 20) - \
                (len([v for v in violations if v.severity_level == "moderate"]) * 10)
        
        return AccessibilityTestResult(
            test_name="Form Accessibility Testing",
            passed=passed,
            score=max(0, score),
            violations=violations,
            recommendations=[v.recommended_fix for v in violations],
            details={
                "form_elements_tested": len(form_elements),
                "form_violations": len(violations)
            }
        )
    
    # Additional helper methods for specific WCAG checks
    
    async def _check_non_text_content(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 1.1.1 - Non-text Content."""
        violations = []
        non_text_elements = [c for c in ui_components if c.get("type") in ["image", "video", "audio", "canvas"]]
        
        for element in non_text_elements:
            if not element.get("alt_text") and not element.get("text_alternative"):
                violations.append(AccessibilityViolation(
                    violation_id=f"1.1.1_{element.get('id', 'unknown')}",
                    wcag_criterion="1.1.1",
                    severity_level="serious",
                    component_affected=element.get("type", "non_text"),
                    description="Non-text content lacks text alternative",
                    recommended_fix="Provide appropriate text alternative",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
        
        return violations
    
    async def _check_info_relationships(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 1.3.1 - Info and Relationships."""
        violations = []
        
        # Check for proper list markup
        lists = html_structure.get("lists", [])
        for list_item in lists:
            if not list_item.get("proper_markup", True):
                violations.append(AccessibilityViolation(
                    violation_id=f"1.3.1_list_{list_item.get('id', 'unknown')}",
                    wcag_criterion="1.3.1",
                    severity_level="moderate",
                    component_affected="list",
                    description="List not properly marked up",
                    recommended_fix="Use proper ul/ol and li elements",
                    compliance_level="A",
                    automated_detection=True,
                    manual_verification_needed=False
                ))
        
        return violations
    
    def _calculate_contrast_ratio(self, foreground: str, background: str) -> float:
        """
        Calculate color contrast ratio (simplified implementation).
        
        Args:
            foreground: Foreground color (hex)
            background: Background color (hex)
            
        Returns:
            Contrast ratio
        """
        # Simplified calculation - real implementation would use proper color space conversion
        # This is a placeholder that simulates contrast calculation
        
        # Convert hex to luminance (simplified)
        def hex_to_luminance(hex_color: str) -> float:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            r = int(hex_color[0:2], 16) / 255
            g = int(hex_color[2:4], 16) / 255
            b = int(hex_color[4:6], 16) / 255
            
            # Simple luminance calculation
            return 0.299 * r + 0.587 * g + 0.114 * b
        
        try:
            fg_luminance = hex_to_luminance(foreground)
            bg_luminance = hex_to_luminance(background)
            
            lighter = max(fg_luminance, bg_luminance)
            darker = min(fg_luminance, bg_luminance)
            
            return (lighter + 0.05) / (darker + 0.05)
        except:
            return 1.0  # Default to failing ratio if calculation fails
    
    def _is_large_text(self, font_size: str, font_weight: str) -> bool:
        """
        Determine if text qualifies as large text for contrast requirements.
        
        Args:
            font_size: Font size (e.g., "18px", "1.2em")
            font_weight: Font weight (e.g., "normal", "bold", "600")
            
        Returns:
            True if text qualifies as large text
        """
        try:
            # Extract numeric value from font size
            size_value = float(re.findall(r'\d+', font_size)[0])
            
            # Check if font is bold
            is_bold = font_weight in ["bold", "600", "700", "800", "900"]
            
            # WCAG large text criteria
            if "px" in font_size:
                return size_value >= 18 or (is_bold and size_value >= 14)
            elif "pt" in font_size:
                return size_value >= 14 or (is_bold and size_value >= 11)
            elif "em" in font_size:
                return size_value >= 1.2 or (is_bold and size_value >= 1.0)
            
        except:
            pass
        
        return False
    
    def _calculate_compliance_summary(self, test_results: List[AccessibilityTestResult], 
                                    wcag_level: str) -> Dict[str, Any]:
        """
        Calculate overall compliance summary from test results.
        
        Args:
            test_results: List of test results
            wcag_level: WCAG compliance level
            
        Returns:
            Compliance summary
        """
        if not test_results:
            return {
                "overall_score": 0,
                "compliance_level": wcag_level,
                "compliance_percentage": 0,
                "total_tests": 0,
                "tests_passed": 0,
                "tests_failed": 0
            }
        
        total_tests = len(test_results)
        tests_passed = sum(1 for result in test_results if result.passed)
        tests_failed = total_tests - tests_passed
        
        # Calculate weighted average score
        total_score = sum(result.score for result in test_results)
        average_score = total_score / total_tests
        
        compliance_percentage = (tests_passed / total_tests) * 100
        
        return {
            "overall_score": round(average_score, 1),
            "compliance_level": wcag_level,
            "compliance_percentage": round(compliance_percentage, 1),
            "total_tests": total_tests,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "meets_threshold": average_score >= self.compliance_thresholds["overall_score"]
        }
    
    def _collect_all_violations(self, test_results: List[AccessibilityTestResult]) -> List[Dict[str, Any]]:
        """
        Collect all violations from test results.
        
        Args:
            test_results: List of test results
            
        Returns:
            List of all violations
        """
        all_violations = []
        
        for result in test_results:
            for violation in result.violations:
                all_violations.append(violation.__dict__)
        
        return all_violations
    
    async def _generate_accessibility_recommendations(self, test_results: List[AccessibilityTestResult]) -> List[Dict[str, Any]]:
        """
        Generate accessibility improvement recommendations.
        
        Args:
            test_results: List of test results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        violation_categories = {}
        
        # Categorize violations
        for result in test_results:
            for violation in result.violations:
                category = violation.wcag_criterion
                if category not in violation_categories:
                    violation_categories[category] = []
                violation_categories[category].append(violation)
        
        # Generate recommendations based on violation patterns
        for category, violations in violation_categories.items():
            if len(violations) > 1:  # Multiple violations in same category
                recommendations.append({
                    "category": f"wcag_{category}",
                    "priority": "high" if any(v.severity_level == "critical" for v in violations) else "medium",
                    "issue": f"Multiple violations in WCAG {category}: {self.wcag_aa_criteria.get(category, {}).get('name', 'Unknown')}",
                    "recommendation": f"Review and fix all instances of {category} violations",
                    "expected_impact": "Improved accessibility compliance and user experience",
                    "violation_count": len(violations)
                })
        
        return recommendations
    
    async def _assess_assistive_technology_support(self, test_results: List[AccessibilityTestResult]) -> Dict[str, Any]:
        """
        Assess support for assistive technologies.
        
        Args:
            test_results: List of test results
            
        Returns:
            Assistive technology support assessment
        """
        screen_reader_support = 90  # Default high support
        keyboard_support = 90
        voice_control_support = 85
        
        # Adjust scores based on violations
        for result in test_results:
            if "screen reader" in result.test_name.lower():
                screen_reader_support = result.score
            elif "keyboard" in result.test_name.lower():
                keyboard_support = result.score
        
        return {
            "screen_reader_support": screen_reader_support,
            "keyboard_navigation_support": keyboard_support,
            "voice_control_support": voice_control_support,
            "overall_assistive_tech_support": round((screen_reader_support + keyboard_support + voice_control_support) / 3, 1)
        }
    
    def _determine_certification_status(self, compliance_summary: Dict[str, Any], wcag_level: str) -> Dict[str, Any]:
        """
        Determine certification status based on compliance results.
        
        Args:
            compliance_summary: Compliance summary
            wcag_level: Target WCAG level
            
        Returns:
            Certification status
        """
        overall_score = compliance_summary.get("overall_score", 0)
        compliance_percentage = compliance_summary.get("compliance_percentage", 0)
        
        if overall_score >= 95 and compliance_percentage >= 95:
            status = "certified"
            message = f"Meets WCAG {wcag_level} certification requirements"
        elif overall_score >= 90 and compliance_percentage >= 90:
            status = "compliant"
            message = f"Compliant with WCAG {wcag_level} standards"
        elif overall_score >= 75:
            status = "partial_compliance"
            message = f"Partially compliant with WCAG {wcag_level}, improvements needed"
        else:
            status = "non_compliant"
            message = f"Does not meet WCAG {wcag_level} standards, significant improvements required"
        
        return {
            "status": status,
            "message": message,
            "wcag_level": wcag_level,
            "certification_date": datetime.now().isoformat() if status == "certified" else None
        }
    
    # Placeholder methods for additional WCAG checks (would be implemented based on specific needs)
    
    async def _check_meaningful_sequence(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 1.3.2 - Meaningful Sequence."""
        return []  # Placeholder
    
    async def _check_color_usage(self, ui_components: List[Dict[str, Any]], css_styles: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 1.4.1 - Use of Color."""
        return []  # Placeholder
    
    async def _check_keyboard_accessibility(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 2.1.1 - Keyboard."""
        return []  # Placeholder
    
    async def _check_keyboard_trap(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 2.1.2 - No Keyboard Trap."""
        return []  # Placeholder
    
    async def _check_bypass_blocks(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.1 - Bypass Blocks."""
        return []  # Placeholder
    
    async def _check_page_titles(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.2 - Page Titled."""
        return []  # Placeholder
    
    async def _check_focus_order(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.3 - Focus Order."""
        return []  # Placeholder
    
    async def _check_link_purpose(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.4 - Link Purpose."""
        return []  # Placeholder
    
    async def _check_headings_labels(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.6 - Headings and Labels."""
        return []  # Placeholder
    
    async def _check_focus_visible(self, css_styles: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 2.4.7 - Focus Visible."""
        return []  # Placeholder
    
    async def _check_page_language(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 3.1.1 - Language of Page."""
        return []  # Placeholder
    
    async def _check_error_identification(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 3.3.1 - Error Identification."""
        return []  # Placeholder
    
    async def _check_labels_instructions(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 3.3.2 - Labels or Instructions."""
        return []  # Placeholder
    
    async def _check_html_parsing(self, html_structure: Dict[str, Any]) -> List[AccessibilityViolation]:
        """Check WCAG 4.1.1 - Parsing."""
        return []  # Placeholder
    
    async def _check_name_role_value(self, ui_components: List[Dict[str, Any]]) -> List[AccessibilityViolation]:
        """Check WCAG 4.1.2 - Name, Role, Value."""
        return []  # Placeholder