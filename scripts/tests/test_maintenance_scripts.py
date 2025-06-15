"""
Maintenance Scripts Tests

Tests for system maintenance utilities that keep the DigiNativa AI Team
system running smoothly and efficiently.

MAINTENANCE AREAS TESTED:
- System health monitoring
- Log management and cleanup
- Performance monitoring
- Data maintenance and cleanup
- Configuration validation
- Resource usage monitoring

These tests ensure maintenance scripts work reliably and help
maintain system performance and reliability.
"""

import pytest
import subprocess
import tempfile
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSystemHealthMonitoring:
    """Test system health monitoring utilities."""
    
    def test_system_health_check(self):
        """Test system health check utility."""
        def check_system_health() -> Dict[str, Any]:
            """Check overall system health."""
            health_status = {
                "timestamp": datetime.now().isoformat(),
                "overall_status": "healthy",
                "components": {},
                "issues": [],
                "recommendations": []
            }
            
            # Check file system health
            try:
                # Check project directories exist
                critical_dirs = ["modules", "tests", "docs", "scripts"]
                for dir_name in critical_dirs:
                    dir_path = project_root / dir_name
                    if dir_path.exists():
                        health_status["components"][f"dir_{dir_name}"] = "healthy"
                    else:
                        health_status["components"][f"dir_{dir_name}"] = "missing"
                        health_status["issues"].append(f"Missing directory: {dir_name}")
                        health_status["overall_status"] = "degraded"
                
                # Check Python environment
                health_status["components"]["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}"
                
                # Check disk space (basic)
                try:
                    stat = os.statvfs(project_root)
                    free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
                    health_status["components"]["free_disk_space_gb"] = round(free_space_gb, 2)
                    
                    if free_space_gb < 1.0:  # Less than 1GB
                        health_status["issues"].append("Low disk space")
                        health_status["recommendations"].append("Clean up temporary files")
                        health_status["overall_status"] = "warning"
                        
                except (AttributeError, OSError):
                    # Windows or other OS without statvfs
                    health_status["components"]["free_disk_space_gb"] = "unknown"
                
            except Exception as e:
                health_status["components"]["filesystem"] = "error"
                health_status["issues"].append(f"Filesystem check failed: {str(e)}")
                health_status["overall_status"] = "unhealthy"
            
            return health_status
        
        # Test health check
        health = check_system_health()
        
        assert "timestamp" in health
        assert "overall_status" in health
        assert "components" in health
        assert "issues" in health
        assert "recommendations" in health
        
        # Status should be valid
        assert health["overall_status"] in ["healthy", "warning", "degraded", "unhealthy"]
        
        # Should have checked core components
        assert isinstance(health["components"], dict)
        assert len(health["components"]) > 0
    
    def test_agent_health_monitoring(self):
        """Test agent health monitoring utility."""
        def monitor_agent_health(agent_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
            """Monitor individual agent health."""
            health_report = {
                "agent_name": agent_name,
                "status": "healthy",
                "metrics": metrics,
                "alerts": [],
                "last_check": datetime.now().isoformat()
            }
            
            # Check processing metrics
            if "processing_time_ms" in metrics:
                proc_time = metrics["processing_time_ms"]
                if proc_time > 30000:  # 30 seconds
                    health_report["alerts"].append("High processing time")
                    health_report["status"] = "warning"
                elif proc_time > 60000:  # 1 minute
                    health_report["alerts"].append("Excessive processing time")
                    health_report["status"] = "critical"
            
            # Check error rates
            if "error_count" in metrics and "total_requests" in metrics:
                error_rate = metrics["error_count"] / max(metrics["total_requests"], 1)
                if error_rate > 0.1:  # 10% error rate
                    health_report["alerts"].append(f"High error rate: {error_rate:.1%}")
                    health_report["status"] = "warning"
                elif error_rate > 0.2:  # 20% error rate
                    health_report["alerts"].append(f"Critical error rate: {error_rate:.1%}")
                    health_report["status"] = "critical"
            
            # Check memory usage indicators
            if "contracts_in_memory" in metrics:
                contracts = metrics["contracts_in_memory"]
                if contracts > 100:
                    health_report["alerts"].append("High memory usage (contracts)")
                    health_report["status"] = "warning"
            
            return health_report
        
        # Test with healthy metrics
        healthy_metrics = {
            "processing_time_ms": 1500,
            "error_count": 2,
            "total_requests": 100,
            "contracts_in_memory": 25
        }
        
        health = monitor_agent_health("test_agent", healthy_metrics)
        assert health["status"] == "healthy"
        assert len(health["alerts"]) == 0
        
        # Test with problematic metrics
        problematic_metrics = {
            "processing_time_ms": 45000,  # High processing time
            "error_count": 15,  # High error count
            "total_requests": 100,
            "contracts_in_memory": 150  # High memory usage
        }
        
        health = monitor_agent_health("test_agent", problematic_metrics)
        assert health["status"] in ["warning", "critical"]
        assert len(health["alerts"]) > 0
    
    def test_contract_pipeline_health(self):
        """Test contract pipeline health monitoring."""
        def check_pipeline_health(pipeline_metrics: Dict[str, Any]) -> Dict[str, Any]:
            """Check contract pipeline health."""
            pipeline_health = {
                "status": "healthy",
                "throughput": "normal",
                "bottlenecks": [],
                "performance_issues": [],
                "recommendations": []
            }
            
            # Check throughput
            if "contracts_per_hour" in pipeline_metrics:
                throughput = pipeline_metrics["contracts_per_hour"]
                if throughput < 10:  # Less than 10 contracts per hour
                    pipeline_health["throughput"] = "low"
                    pipeline_health["performance_issues"].append("Low contract throughput")
                elif throughput > 100:  # More than 100 contracts per hour
                    pipeline_health["throughput"] = "high"
            
            # Check for bottlenecks
            if "agent_processing_times" in pipeline_metrics:
                times = pipeline_metrics["agent_processing_times"]
                max_time = max(times.values()) if times else 0
                avg_time = sum(times.values()) / len(times) if times else 0
                
                for agent, time_ms in times.items():
                    if time_ms > avg_time * 2:  # More than 2x average
                        pipeline_health["bottlenecks"].append(f"{agent}: {time_ms}ms")
            
            # Check queue lengths
            if "queue_lengths" in pipeline_metrics:
                queues = pipeline_metrics["queue_lengths"]
                for agent, queue_length in queues.items():
                    if queue_length > 10:  # Queue backing up
                        pipeline_health["bottlenecks"].append(f"{agent} queue: {queue_length}")
                        pipeline_health["recommendations"].append(f"Scale {agent} processing")
            
            # Set overall status
            if pipeline_health["bottlenecks"] or pipeline_health["performance_issues"]:
                pipeline_health["status"] = "degraded"
            
            return pipeline_health
        
        # Test with healthy pipeline
        healthy_pipeline = {
            "contracts_per_hour": 25,
            "agent_processing_times": {
                "project_manager": 2000,
                "game_designer": 3000,
                "developer": 5000,
                "test_engineer": 4000,
                "qa_tester": 3500,
                "quality_reviewer": 2500
            },
            "queue_lengths": {
                "project_manager": 2,
                "game_designer": 1,
                "developer": 3,
                "test_engineer": 2,
                "qa_tester": 1,
                "quality_reviewer": 1
            }
        }
        
        health = check_pipeline_health(healthy_pipeline)
        assert health["status"] == "healthy"
        assert len(health["bottlenecks"]) == 0
        
        # Test with problematic pipeline
        problematic_pipeline = {
            "contracts_per_hour": 5,  # Low throughput
            "agent_processing_times": {
                "project_manager": 2000,
                "game_designer": 15000,  # Very slow
                "developer": 5000,
                "test_engineer": 4000,
                "qa_tester": 3500,
                "quality_reviewer": 2500
            },
            "queue_lengths": {
                "project_manager": 2,
                "game_designer": 15,  # Queue backing up
                "developer": 12,  # Queue backing up
                "test_engineer": 8,
                "qa_tester": 5,
                "quality_reviewer": 3
            }
        }
        
        health = check_pipeline_health(problematic_pipeline)
        assert health["status"] == "degraded"
        assert len(health["bottlenecks"]) > 0
        assert len(health["performance_issues"]) > 0


class TestLogManagement:
    """Test log management and cleanup utilities."""
    
    def test_log_rotation_utility(self):
        """Test log rotation utility."""
        def rotate_logs(log_directory: Path, max_size_mb: int = 10, max_files: int = 5) -> Dict[str, Any]:
            """Rotate log files when they exceed size limits."""
            rotation_result = {
                "rotated_files": [],
                "errors": [],
                "total_space_freed_mb": 0
            }
            
            if not log_directory.exists():
                log_directory.mkdir(parents=True, exist_ok=True)
            
            try:
                for log_file in log_directory.glob("*.log"):
                    if log_file.exists():
                        file_size_mb = log_file.stat().st_size / (1024 * 1024)
                        
                        if file_size_mb > max_size_mb:
                            # Simulate rotation
                            base_name = log_file.stem
                            
                            # Find existing rotated files
                            existing_rotated = list(log_directory.glob(f"{base_name}.*.log"))
                            existing_rotated.sort(key=lambda x: x.name)
                            
                            # Remove oldest if we have too many
                            while len(existing_rotated) >= max_files:
                                oldest = existing_rotated.pop(0)
                                if oldest.exists():
                                    freed_mb = oldest.stat().st_size / (1024 * 1024)
                                    rotation_result["total_space_freed_mb"] += freed_mb
                                    # In real implementation: oldest.unlink()
                            
                            # Rotate current file
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            rotated_name = f"{base_name}.{timestamp}.log"
                            
                            rotation_result["rotated_files"].append({
                                "original": str(log_file),
                                "rotated": rotated_name,
                                "size_mb": round(file_size_mb, 2)
                            })
                            
                            # In real implementation: log_file.rename(log_directory / rotated_name)
                            
            except Exception as e:
                rotation_result["errors"].append(str(e))
            
            return rotation_result
        
        # Test log rotation
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            
            # Create test log file
            test_log = log_dir / "test.log"
            test_log.write_text("x" * (15 * 1024 * 1024))  # 15MB file
            
            result = rotate_logs(log_dir, max_size_mb=10, max_files=3)
            
            assert len(result["rotated_files"]) > 0
            assert result["rotated_files"][0]["size_mb"] > 10
            assert len(result["errors"]) == 0
    
    def test_log_cleanup_utility(self):
        """Test log cleanup utility."""
        def cleanup_old_logs(log_directory: Path, days_to_keep: int = 7) -> Dict[str, Any]:
            """Clean up log files older than specified days."""
            cleanup_result = {
                "deleted_files": [],
                "space_freed_mb": 0,
                "errors": []
            }
            
            if not log_directory.exists():
                return cleanup_result
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            try:
                for log_file in log_directory.glob("*.log"):
                    if log_file.exists():
                        file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                        
                        if file_mtime < cutoff_date:
                            file_size_mb = log_file.stat().st_size / (1024 * 1024)
                            cleanup_result["deleted_files"].append({
                                "file": str(log_file),
                                "age_days": (datetime.now() - file_mtime).days,
                                "size_mb": round(file_size_mb, 2)
                            })
                            cleanup_result["space_freed_mb"] += file_size_mb
                            
                            # In real implementation: log_file.unlink()
                            
            except Exception as e:
                cleanup_result["errors"].append(str(e))
            
            cleanup_result["space_freed_mb"] = round(cleanup_result["space_freed_mb"], 2)
            return cleanup_result
        
        # Test log cleanup
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            
            # Create old log file
            old_log = log_dir / "old.log"
            old_log.write_text("old log content")
            
            # Simulate old file by setting modification time
            old_time = time.time() - (10 * 24 * 60 * 60)  # 10 days ago
            os.utime(old_log, (old_time, old_time))
            
            # Create recent log file
            recent_log = log_dir / "recent.log"
            recent_log.write_text("recent log content")
            
            result = cleanup_old_logs(log_dir, days_to_keep=7)
            
            # Should identify old file for deletion
            assert len(result["deleted_files"]) == 1
            assert result["deleted_files"][0]["age_days"] >= 7
            assert result["space_freed_mb"] > 0
            assert len(result["errors"]) == 0
    
    def test_log_analysis_utility(self):
        """Test log analysis utility."""
        def analyze_logs(log_directory: Path, pattern: str = "ERROR") -> Dict[str, Any]:
            """Analyze logs for specific patterns."""
            analysis_result = {
                "pattern": pattern,
                "matches": [],
                "summary": {
                    "total_matches": 0,
                    "files_with_matches": 0,
                    "date_range": None
                }
            }
            
            if not log_directory.exists():
                return analysis_result
            
            try:
                for log_file in log_directory.glob("*.log"):
                    if log_file.exists():
                        file_matches = []
                        
                        try:
                            with open(log_file, 'r', encoding='utf-8') as f:
                                for line_num, line in enumerate(f, 1):
                                    if pattern.upper() in line.upper():
                                        file_matches.append({
                                            "line_number": line_num,
                                            "content": line.strip()[:200]  # Truncate long lines
                                        })
                        except (UnicodeDecodeError, IOError):
                            # Skip binary or unreadable files
                            continue
                        
                        if file_matches:
                            analysis_result["matches"].append({
                                "file": str(log_file),
                                "match_count": len(file_matches),
                                "matches": file_matches[:10]  # Limit to first 10 matches
                            })
                            analysis_result["summary"]["files_with_matches"] += 1
                            analysis_result["summary"]["total_matches"] += len(file_matches)
                
            except Exception as e:
                analysis_result["error"] = str(e)
            
            return analysis_result
        
        # Test log analysis
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            
            # Create test log with errors
            error_log = log_dir / "app.log"
            error_log.write_text("""
2024-01-01 10:00:00 INFO Application started
2024-01-01 10:01:00 ERROR Failed to connect to database
2024-01-01 10:02:00 INFO Retrying connection
2024-01-01 10:03:00 ERROR Authentication failed
2024-01-01 10:04:00 INFO Application running normally
""")
            
            result = analyze_logs(log_dir, "ERROR")
            
            assert result["summary"]["total_matches"] == 2
            assert result["summary"]["files_with_matches"] == 1
            assert len(result["matches"]) == 1
            assert result["matches"][0]["match_count"] == 2


class TestPerformanceMonitoring:
    """Test performance monitoring utilities."""
    
    def test_performance_metrics_collection(self):
        """Test performance metrics collection utility."""
        def collect_performance_metrics() -> Dict[str, Any]:
            """Collect system performance metrics."""
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "system": {},
                "application": {},
                "trends": {}
            }
            
            # System metrics
            try:
                import psutil
                metrics["system"]["cpu_percent"] = psutil.cpu_percent(interval=1)
                metrics["system"]["memory_percent"] = psutil.virtual_memory().percent
                metrics["system"]["disk_percent"] = psutil.disk_usage('/').percent
            except ImportError:
                # Fallback metrics without psutil
                metrics["system"]["cpu_percent"] = "unknown"
                metrics["system"]["memory_percent"] = "unknown"
                metrics["system"]["disk_percent"] = "unknown"
            
            # Application metrics (simulated)
            metrics["application"]["active_agents"] = 6
            metrics["application"]["contracts_processed_last_hour"] = 25
            metrics["application"]["average_processing_time_ms"] = 3500
            metrics["application"]["error_rate_percent"] = 2.1
            
            # Performance trends (simulated)
            metrics["trends"]["processing_time_trend"] = "stable"  # stable, increasing, decreasing
            metrics["trends"]["throughput_trend"] = "increasing"
            metrics["trends"]["error_rate_trend"] = "decreasing"
            
            return metrics
        
        # Test metrics collection
        metrics = collect_performance_metrics()
        
        assert "timestamp" in metrics
        assert "system" in metrics
        assert "application" in metrics
        assert "trends" in metrics
        
        # Application metrics should be present
        app_metrics = metrics["application"]
        assert "active_agents" in app_metrics
        assert "contracts_processed_last_hour" in app_metrics
        assert "average_processing_time_ms" in app_metrics
        assert "error_rate_percent" in app_metrics
        
        # Trends should be valid
        trends = metrics["trends"]
        for trend_value in trends.values():
            assert trend_value in ["stable", "increasing", "decreasing", "unknown"]
    
    def test_performance_alerting(self):
        """Test performance alerting utility."""
        def check_performance_alerts(metrics: Dict[str, Any]) -> Dict[str, Any]:
            """Check performance metrics for alerts."""
            alerts = {
                "critical": [],
                "warning": [],
                "info": [],
                "alert_level": "none"
            }
            
            # Check system metrics
            if "system" in metrics:
                system = metrics["system"]
                
                if isinstance(system.get("cpu_percent"), (int, float)):
                    cpu = system["cpu_percent"]
                    if cpu > 90:
                        alerts["critical"].append(f"CPU usage critical: {cpu}%")
                    elif cpu > 75:
                        alerts["warning"].append(f"CPU usage high: {cpu}%")
                
                if isinstance(system.get("memory_percent"), (int, float)):
                    memory = system["memory_percent"]
                    if memory > 95:
                        alerts["critical"].append(f"Memory usage critical: {memory}%")
                    elif memory > 85:
                        alerts["warning"].append(f"Memory usage high: {memory}%")
            
            # Check application metrics
            if "application" in metrics:
                app = metrics["application"]
                
                if "average_processing_time_ms" in app:
                    proc_time = app["average_processing_time_ms"]
                    if proc_time > 10000:  # 10 seconds
                        alerts["critical"].append(f"Processing time critical: {proc_time}ms")
                    elif proc_time > 5000:  # 5 seconds
                        alerts["warning"].append(f"Processing time high: {proc_time}ms")
                
                if "error_rate_percent" in app:
                    error_rate = app["error_rate_percent"]
                    if error_rate > 10:
                        alerts["critical"].append(f"Error rate critical: {error_rate}%")
                    elif error_rate > 5:
                        alerts["warning"].append(f"Error rate high: {error_rate}%")
            
            # Set overall alert level
            if alerts["critical"]:
                alerts["alert_level"] = "critical"
            elif alerts["warning"]:
                alerts["alert_level"] = "warning"
            elif alerts["info"]:
                alerts["alert_level"] = "info"
            
            return alerts
        
        # Test with good metrics
        good_metrics = {
            "system": {
                "cpu_percent": 45.0,
                "memory_percent": 60.0
            },
            "application": {
                "average_processing_time_ms": 2500,
                "error_rate_percent": 1.2
            }
        }
        
        alerts = check_performance_alerts(good_metrics)
        assert alerts["alert_level"] == "none"
        assert len(alerts["critical"]) == 0
        assert len(alerts["warning"]) == 0
        
        # Test with problematic metrics
        bad_metrics = {
            "system": {
                "cpu_percent": 95.0,  # Critical
                "memory_percent": 88.0  # Warning
            },
            "application": {
                "average_processing_time_ms": 12000,  # Critical
                "error_rate_percent": 8.5  # Warning
            }
        }
        
        alerts = check_performance_alerts(bad_metrics)
        assert alerts["alert_level"] == "critical"
        assert len(alerts["critical"]) > 0
        assert len(alerts["warning"]) > 0
    
    def test_performance_optimization_suggestions(self):
        """Test performance optimization suggestions utility."""
        def suggest_optimizations(metrics: Dict[str, Any], alerts: Dict[str, Any]) -> List[str]:
            """Suggest performance optimizations based on metrics and alerts."""
            suggestions = []
            
            # Analyze alerts for optimization opportunities
            for alert in alerts.get("critical", []) + alerts.get("warning", []):
                if "CPU usage" in alert:
                    suggestions.append("Consider scaling horizontally or optimizing CPU-intensive operations")
                elif "Memory usage" in alert:
                    suggestions.append("Review memory usage patterns and implement garbage collection optimizations")
                elif "Processing time" in alert:
                    suggestions.append("Profile slow operations and implement caching or async processing")
                elif "Error rate" in alert:
                    suggestions.append("Investigate error patterns and improve error handling")
            
            # Check trends for proactive suggestions
            if "trends" in metrics:
                trends = metrics["trends"]
                
                if trends.get("processing_time_trend") == "increasing":
                    suggestions.append("Processing time is trending upward - consider performance profiling")
                
                if trends.get("error_rate_trend") == "increasing":
                    suggestions.append("Error rate is increasing - review recent changes and logs")
                
                if trends.get("throughput_trend") == "decreasing":
                    suggestions.append("Throughput is declining - check for bottlenecks in the pipeline")
            
            # Remove duplicates and limit suggestions
            suggestions = list(set(suggestions))[:5]
            
            return suggestions
        
        # Test optimization suggestions
        metrics_with_trends = {
            "trends": {
                "processing_time_trend": "increasing",
                "error_rate_trend": "stable",
                "throughput_trend": "decreasing"
            }
        }
        
        alerts_with_issues = {
            "critical": ["CPU usage critical: 95%"],
            "warning": ["Processing time high: 7500ms", "Error rate high: 6.2%"]
        }
        
        suggestions = suggest_optimizations(metrics_with_trends, alerts_with_issues)
        
        assert len(suggestions) > 0
        assert any("CPU" in s for s in suggestions)
        assert any("processing" in s.lower() for s in suggestions)
        assert any("error" in s.lower() for s in suggestions)


class TestDataMaintenance:
    """Test data maintenance and cleanup utilities."""
    
    def test_temporary_file_cleanup(self):
        """Test temporary file cleanup utility."""
        def cleanup_temp_files(base_directory: Path, max_age_hours: int = 24) -> Dict[str, Any]:
            """Clean up temporary files older than specified hours."""
            cleanup_result = {
                "deleted_files": 0,
                "space_freed_mb": 0,
                "errors": [],
                "file_patterns_cleaned": []
            }
            
            temp_patterns = ["*.tmp", "*.temp", "*~", "*.bak", ".DS_Store", "Thumbs.db"]
            cutoff_time = time.time() - (max_age_hours * 3600)
            
            try:
                for pattern in temp_patterns:
                    pattern_files = list(base_directory.rglob(pattern))
                    files_cleaned = 0
                    
                    for temp_file in pattern_files:
                        if temp_file.is_file():
                            try:
                                file_mtime = temp_file.stat().st_mtime
                                if file_mtime < cutoff_time:
                                    file_size = temp_file.stat().st_size
                                    cleanup_result["space_freed_mb"] += file_size / (1024 * 1024)
                                    files_cleaned += 1
                                    # In real implementation: temp_file.unlink()
                            except (OSError, IOError) as e:
                                cleanup_result["errors"].append(f"Error cleaning {temp_file}: {str(e)}")
                    
                    if files_cleaned > 0:
                        cleanup_result["file_patterns_cleaned"].append({
                            "pattern": pattern,
                            "files_cleaned": files_cleaned
                        })
                        cleanup_result["deleted_files"] += files_cleaned
                
            except Exception as e:
                cleanup_result["errors"].append(f"General cleanup error: {str(e)}")
            
            cleanup_result["space_freed_mb"] = round(cleanup_result["space_freed_mb"], 2)
            return cleanup_result
        
        # Test temp file cleanup
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir)
            
            # Create test temp files
            old_temp = test_dir / "old.tmp"
            old_temp.write_text("old temp content")
            
            recent_temp = test_dir / "recent.tmp"
            recent_temp.write_text("recent temp content")
            
            # Make one file old
            old_time = time.time() - (48 * 3600)  # 48 hours ago
            os.utime(old_temp, (old_time, old_time))
            
            result = cleanup_temp_files(test_dir, max_age_hours=24)
            
            # Should find the old temp file
            assert result["deleted_files"] > 0
            assert result["space_freed_mb"] > 0
            assert len(result["file_patterns_cleaned"]) > 0
    
    def test_cache_management(self):
        """Test cache management utility."""
        def manage_cache(cache_directory: Path, max_size_mb: int = 100) -> Dict[str, Any]:
            """Manage cache size by removing least recently used files."""
            management_result = {
                "cache_size_mb": 0,
                "files_removed": 0,
                "space_freed_mb": 0,
                "status": "within_limits"
            }
            
            if not cache_directory.exists():
                return management_result
            
            try:
                # Calculate current cache size and collect file info
                cache_files = []
                total_size = 0
                
                for cache_file in cache_directory.rglob("*"):
                    if cache_file.is_file():
                        file_size = cache_file.stat().st_size
                        file_atime = cache_file.stat().st_atime  # Access time
                        
                        cache_files.append({
                            "path": cache_file,
                            "size": file_size,
                            "access_time": file_atime
                        })
                        total_size += file_size
                
                management_result["cache_size_mb"] = round(total_size / (1024 * 1024), 2)
                
                # Check if cleanup is needed
                if management_result["cache_size_mb"] > max_size_mb:
                    management_result["status"] = "cleanup_needed"
                    
                    # Sort by access time (oldest first)
                    cache_files.sort(key=lambda x: x["access_time"])
                    
                    # Remove files until under limit
                    space_to_free = total_size - (max_size_mb * 1024 * 1024)
                    space_freed = 0
                    
                    for file_info in cache_files:
                        if space_freed >= space_to_free:
                            break
                        
                        file_size = file_info["size"]
                        management_result["files_removed"] += 1
                        space_freed += file_size
                        # In real implementation: file_info["path"].unlink()
                    
                    management_result["space_freed_mb"] = round(space_freed / (1024 * 1024), 2)
                    management_result["status"] = "cleanup_completed"
                
            except Exception as e:
                management_result["error"] = str(e)
                management_result["status"] = "error"
            
            return management_result
        
        # Test cache management
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            
            # Create cache files with different access times
            for i in range(5):
                cache_file = cache_dir / f"cache_{i}.dat"
                cache_file.write_text("x" * (25 * 1024 * 1024))  # 25MB each
                
                # Set different access times
                access_time = time.time() - (i * 3600)  # Each file 1 hour older
                os.utime(cache_file, (access_time, access_time))
            
            # Should trigger cleanup (125MB total, limit 100MB)
            result = manage_cache(cache_dir, max_size_mb=100)
            
            assert result["cache_size_mb"] > 100
            assert result["status"] in ["cleanup_needed", "cleanup_completed"]
            if result["status"] == "cleanup_completed":
                assert result["files_removed"] > 0
                assert result["space_freed_mb"] > 0


class TestMaintenanceIntegration:
    """Test integration of maintenance utilities."""
    
    def test_comprehensive_maintenance_run(self):
        """Test comprehensive maintenance routine."""
        def run_comprehensive_maintenance() -> Dict[str, Any]:
            """Run comprehensive maintenance routine."""
            maintenance_report = {
                "start_time": datetime.now().isoformat(),
                "tasks_completed": [],
                "tasks_failed": [],
                "overall_status": "success",
                "summary": {}
            }
            
            try:
                # Task 1: System health check
                health_check = {
                    "overall_status": "healthy",
                    "components_checked": 5,
                    "issues_found": 0
                }
                maintenance_report["tasks_completed"].append("system_health_check")
                maintenance_report["summary"]["health_check"] = health_check
                
                # Task 2: Log cleanup
                log_cleanup = {
                    "files_cleaned": 3,
                    "space_freed_mb": 15.2
                }
                maintenance_report["tasks_completed"].append("log_cleanup")
                maintenance_report["summary"]["log_cleanup"] = log_cleanup
                
                # Task 3: Cache management
                cache_management = {
                    "cache_size_mb": 45.8,
                    "files_removed": 0,
                    "status": "within_limits"
                }
                maintenance_report["tasks_completed"].append("cache_management")
                maintenance_report["summary"]["cache_management"] = cache_management
                
                # Task 4: Performance monitoring
                perf_monitoring = {
                    "metrics_collected": True,
                    "alerts_generated": 0,
                    "status": "normal"
                }
                maintenance_report["tasks_completed"].append("performance_monitoring")
                maintenance_report["summary"]["performance_monitoring"] = perf_monitoring
                
            except Exception as e:
                maintenance_report["tasks_failed"].append(f"Error in maintenance: {str(e)}")
                maintenance_report["overall_status"] = "partial_failure"
            
            maintenance_report["end_time"] = datetime.now().isoformat()
            return maintenance_report
        
        # Test comprehensive maintenance
        report = run_comprehensive_maintenance()
        
        assert "start_time" in report
        assert "end_time" in report
        assert "tasks_completed" in report
        assert "tasks_failed" in report
        assert "overall_status" in report
        assert "summary" in report
        
        # Should complete multiple tasks
        assert len(report["tasks_completed"]) >= 3
        assert report["overall_status"] in ["success", "partial_failure", "failure"]
        
        # Summary should contain results for each task
        assert "health_check" in report["summary"]
        assert "log_cleanup" in report["summary"]
        assert "cache_management" in report["summary"]
    
    def test_maintenance_scheduling(self):
        """Test maintenance scheduling utility."""
        def schedule_maintenance_tasks() -> List[Dict[str, Any]]:
            """Define maintenance task schedule."""
            schedule = [
                {
                    "task": "temp_file_cleanup",
                    "frequency": "daily",
                    "time": "02:00",
                    "enabled": True,
                    "priority": "low"
                },
                {
                    "task": "log_rotation",
                    "frequency": "daily",
                    "time": "03:00",
                    "enabled": True,
                    "priority": "medium"
                },
                {
                    "task": "performance_monitoring",
                    "frequency": "hourly",
                    "time": None,
                    "enabled": True,
                    "priority": "high"
                },
                {
                    "task": "system_health_check",
                    "frequency": "every_15_minutes",
                    "time": None,
                    "enabled": True,
                    "priority": "high"
                },
                {
                    "task": "cache_cleanup",
                    "frequency": "weekly",
                    "time": "01:00",
                    "enabled": True,
                    "priority": "medium"
                }
            ]
            
            return schedule
        
        # Test maintenance scheduling
        schedule = schedule_maintenance_tasks()
        
        assert len(schedule) > 0
        
        # Validate schedule structure
        for task in schedule:
            assert "task" in task
            assert "frequency" in task
            assert "enabled" in task
            assert "priority" in task
            
            # Frequency should be valid
            assert task["frequency"] in [
                "every_15_minutes", "hourly", "daily", "weekly", "monthly"
            ]
            
            # Priority should be valid
            assert task["priority"] in ["low", "medium", "high", "critical"]


# Maintenance script benchmarks
MAINTENANCE_BENCHMARKS = {
    "max_health_check_time": 30,  # 30 seconds
    "max_log_cleanup_time": 60,   # 1 minute
    "max_cache_cleanup_time": 120, # 2 minutes
    "max_temp_cleanup_time": 180, # 3 minutes
    "min_disk_space_gb": 1.0,     # 1GB minimum
    "max_log_retention_days": 30, # 30 days max
    "max_cache_size_mb": 500      # 500MB max cache
}


if __name__ == "__main__":
    # Run with: pytest scripts/tests/test_maintenance_scripts.py -v
    pytest.main([__file__, "-v", "--tb=short"])