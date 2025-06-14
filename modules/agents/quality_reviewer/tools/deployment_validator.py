"""
Deployment Validator - Validates production readiness for DigiNativa features.

Checks all requirements for safe production deployment including performance,
security, accessibility, and DNA compliance requirements.
"""

import logging
from typing import Dict, Any


class DeploymentValidator:
    """Validates production deployment readiness."""
    
    def __init__(self):
        """Initialize deployment validator."""
        self.logger = logging.getLogger(f"{__name__}.DeploymentValidator")
        
        # Production requirements thresholds
        self.production_requirements = {
            "lighthouse_score_min": 90,
            "api_response_time_max_ms": 200,
            "test_coverage_min_percent": 95,
            "wcag_compliance_min_percent": 90,
            "dna_compliance_min_percent": 85,
            "security_score_min": 95
        }
        
        self.logger.info(f"Deployment validator initialized with requirements: {self.production_requirements}")
    
    async def validate_performance_requirements(self, performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate performance requirements for production deployment."""
        try:
            issues = []
            passed = True
            
            # Check Lighthouse score
            lighthouse_score = performance_analysis.get("lighthouse_score", 0)
            if lighthouse_score < self.production_requirements["lighthouse_score_min"]:
                passed = False
                issues.append(f"Lighthouse score too low: {lighthouse_score} < {self.production_requirements['lighthouse_score_min']}")
            
            # Check API response time
            api_response_time = performance_analysis.get("api_response_time_ms", 1000)
            if api_response_time > self.production_requirements["api_response_time_max_ms"]:
                passed = False
                issues.append(f"API response time too slow: {api_response_time}ms > {self.production_requirements['api_response_time_max_ms']}ms")
            
            # Check page load time (should be under 3 seconds for production)
            page_load_time = performance_analysis.get("page_load_time_ms", 5000)
            if page_load_time > 3000:
                passed = False
                issues.append(f"Page load time too slow: {page_load_time}ms > 3000ms")
            
            return {
                "passed": passed,
                "requirement": "performance",
                "issues": issues,
                "metrics": {
                    "lighthouse_score": lighthouse_score,
                    "api_response_time_ms": api_response_time,
                    "page_load_time_ms": page_load_time
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"Performance requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "performance",
                "issues": [f"Validation failed: {e}"],
                "issue": f"Performance validation error: {e}"
            }
    
    async def validate_security_requirements(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate security requirements for production deployment."""
        try:
            issues = []
            passed = True
            
            # Check for security vulnerabilities
            security_audit = qa_data.get("security_audit", {})
            vulnerabilities = security_audit.get("vulnerabilities", [])
            
            if vulnerabilities:
                high_severity = [v for v in vulnerabilities if v.get("severity") == "high"]
                if high_severity:
                    passed = False
                    issues.append(f"{len(high_severity)} high-severity security vulnerabilities found")
                
                medium_severity = [v for v in vulnerabilities if v.get("severity") == "medium"]
                if len(medium_severity) > 5:
                    passed = False
                    issues.append(f"{len(medium_severity)} medium-severity vulnerabilities (max 5 allowed)")
            
            # Check authentication and authorization
            auth_implemented = security_audit.get("authentication_implemented", False)
            if not auth_implemented:
                passed = False
                issues.append("Authentication not properly implemented")
            
            # Check data validation
            input_validation = security_audit.get("input_validation_score", 0)
            if input_validation < self.production_requirements["security_score_min"]:
                passed = False
                issues.append(f"Input validation score too low: {input_validation} < {self.production_requirements['security_score_min']}")
            
            # Check HTTPS and secure headers
            secure_headers = security_audit.get("secure_headers_implemented", False)
            if not secure_headers:
                passed = False
                issues.append("Security headers not properly configured")
            
            return {
                "passed": passed,
                "requirement": "security",
                "issues": issues,
                "metrics": {
                    "vulnerabilities_count": len(vulnerabilities),
                    "high_severity_count": len([v for v in vulnerabilities if v.get("severity") == "high"]),
                    "input_validation_score": input_validation,
                    "secure_headers_implemented": secure_headers
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"Security requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "security",
                "issues": [f"Validation failed: {e}"],
                "issue": f"Security validation error: {e}"
            }
    
    async def validate_accessibility_requirements(self, accessibility_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate accessibility requirements for production deployment."""
        try:
            issues = []
            passed = True
            
            # Check WCAG compliance
            wcag_compliance = accessibility_analysis.get("wcag_compliance_percent", 0)
            if wcag_compliance < self.production_requirements["wcag_compliance_min_percent"]:
                passed = False
                issues.append(f"WCAG compliance too low: {wcag_compliance}% < {self.production_requirements['wcag_compliance_min_percent']}%")
            
            # Check for critical accessibility violations
            violations_count = accessibility_analysis.get("violations_count", 0)
            if violations_count > 0:
                passed = False
                issues.append(f"{violations_count} accessibility violations must be fixed")
            
            # Check keyboard accessibility
            keyboard_accessible = accessibility_analysis.get("keyboard_accessible", False)
            if not keyboard_accessible:
                passed = False
                issues.append("Keyboard navigation not fully accessible")
            
            return {
                "passed": passed,
                "requirement": "accessibility",
                "issues": issues,
                "metrics": {
                    "wcag_compliance_percent": wcag_compliance,
                    "violations_count": violations_count,
                    "keyboard_accessible": keyboard_accessible
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"Accessibility requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "accessibility",
                "issues": [f"Validation failed: {e}"],
                "issue": f"Accessibility validation error: {e}"
            }
    
    async def validate_dna_requirements(self, dna_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate DNA compliance requirements for production deployment."""
        try:
            issues = []
            passed = True
            
            # Check design principles compliance
            design_principles_avg = dna_analysis.get("design_principles_avg", 0)
            if design_principles_avg < 4.0:
                passed = False
                issues.append(f"Design principles score too low: {design_principles_avg} < 4.0")
            
            # Check architecture principles compliance
            architecture_compliance = dna_analysis.get("architecture_principles", {}).get("compliance_percent", 0)
            if architecture_compliance < self.production_requirements["dna_compliance_min_percent"]:
                passed = False
                issues.append(f"Architecture compliance too low: {architecture_compliance}% < {self.production_requirements['dna_compliance_min_percent']}%")
            
            # Check specific DNA principles
            design_principles = dna_analysis.get("design_principles", {})
            for principle, score in design_principles.items():
                if score < 3.5:
                    passed = False
                    issues.append(f"DNA principle '{principle}' score too low: {score} < 3.5")
            
            return {
                "passed": passed,
                "requirement": "dna_compliance",
                "issues": issues,
                "metrics": {
                    "design_principles_avg": design_principles_avg,
                    "architecture_compliance_percent": architecture_compliance,
                    "design_principles": design_principles
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"DNA requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "dna_compliance",
                "issues": [f"Validation failed: {e}"],
                "issue": f"DNA validation error: {e}"
            }
    
    async def validate_test_coverage_requirements(self, test_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate test coverage requirements for production deployment."""
        try:
            issues = []
            passed = True
            
            # Check test coverage
            coverage_percent = test_analysis.get("coverage_percent", 0)
            if coverage_percent < self.production_requirements["test_coverage_min_percent"]:
                passed = False
                issues.append(f"Test coverage too low: {coverage_percent}% < {self.production_requirements['test_coverage_min_percent']}%")
            
            # Check test pass rate
            pass_rate = test_analysis.get("pass_rate", 0)
            if pass_rate < 100:
                passed = False
                issues.append(f"Not all tests passing: {pass_rate}% pass rate")
            
            return {
                "passed": passed,
                "requirement": "test_coverage",
                "issues": issues,
                "metrics": {
                    "coverage_percent": coverage_percent,
                    "pass_rate": pass_rate
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"Test coverage requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "test_coverage",
                "issues": [f"Validation failed: {e}"],
                "issue": f"Test coverage validation error: {e}"
            }
    
    async def validate_compatibility_requirements(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate browser and device compatibility requirements."""
        try:
            issues = []
            passed = True
            
            # Check browser compatibility
            browser_compatibility = qa_data.get("browser_compatibility", {})
            supported_browsers = browser_compatibility.get("supported_browsers", [])
            required_browsers = ["Chrome", "Firefox", "Safari", "Edge"]
            
            for browser in required_browsers:
                if browser not in supported_browsers:
                    passed = False
                    issues.append(f"Browser {browser} not fully supported")
            
            # Check mobile compatibility
            mobile_compatibility = qa_data.get("mobile_compatibility", {})
            responsive_design = mobile_compatibility.get("responsive_design", False)
            if not responsive_design:
                passed = False
                issues.append("Responsive design not properly implemented")
            
            # Check device testing
            devices_tested = mobile_compatibility.get("devices_tested", [])
            if len(devices_tested) < 3:
                passed = False
                issues.append(f"Insufficient device testing: {len(devices_tested)} devices (minimum 3)")
            
            return {
                "passed": passed,
                "requirement": "compatibility",
                "issues": issues,
                "metrics": {
                    "supported_browsers": supported_browsers,
                    "responsive_design": responsive_design,
                    "devices_tested_count": len(devices_tested)
                },
                "issue": "; ".join(issues) if issues else None
            }
            
        except Exception as e:
            self.logger.error(f"Compatibility requirements validation failed: {e}")
            return {
                "passed": False,
                "requirement": "compatibility",
                "issues": [f"Validation failed: {e}"],
                "issue": f"Compatibility validation error: {e}"
            }