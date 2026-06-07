"""
CertifyIQ Mock Engine — Pre-written realistic responses for EMP-001 through EMP-004.
Used when MOCK_MODE=true. No Azure API calls. Completes in <500ms.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.synthetic_employees import get_employee


MOCK_RESPONSES = {
    "EMP-001": {
        "employee": {
            "id": "EMP-001",
            "name": "Alex Chen",
            "role": "Cloud Engineer",
            "certification_target": "AZ-204",
            "current_practice_score": 62,
        },
        "learner_profile": {
            "learner_type": "ON_SCHEDULE",
            "learner_type_description": "Score improving week-over-week at steady pace",
            "skill_gap": ["Azure Security", "Azure SDK", "REST APIs"],
            "skills_known": ["Azure App Service", "Azure Functions", "Azure Storage"],
            "experience_score": 0.20,
            "risk_score": 0.52,
            "score_velocity": 3.5,
            "recommended_approach": "Maintain steady pace. Weekly practice exams. Focus on weak areas.",
            "citations": ["[Source: Role Skills Matrix]", "[Source: Engineering Certification Guide]"],
            "summary": "Learner type: ON_SCHEDULE | Risk: 52% | Gap: 3 skills",
        },
        "learning_path": {
            "certification": "AZ-204",
            "learning_path": [
                {"topic": "Azure App Service & Compute", "hours": 8, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Azure Storage Solutions", "hours": 6, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Azure Security & Key Vault", "hours": 7, "priority": "HIGH", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Azure Functions & Serverless", "hours": 5, "priority": "MED", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Practice Exams & Gap Review", "hours": 6, "priority": "HIGH", "citation": "[Source: AZ-204 Question Bank]"},
            ],
            "total_hours": 32,
            "prerequisites": ["AZ-900 (recommended)", "Basic Python or C# knowledge", "REST API familiarity"],
            "citations": ["[Source: Engineering Certification Guide]", "[Source: Role Skills Matrix]"],
            "summary": "5-topic learning path, 32hrs total",
        },
        "study_plan": {
            "weekly_plan": [
                {"week": 1, "topics": ["Azure App Service & Compute"], "hours": 8, "milestone": "Complete foundational concepts", "target_score": 60},
                {"week": 2, "topics": ["Azure Storage Solutions", "Azure Security & Key Vault"], "hours": 8, "milestone": "Complete Azure Storage Solutions module", "target_score": 68},
                {"week": 3, "topics": ["Azure Functions & Serverless"], "hours": 8, "milestone": "Complete Azure Functions & Serverless module", "target_score": 71},
                {"week": 4, "topics": ["Practice Exams & Gap Review"], "hours": 8, "milestone": "Final practice exam — target 80%+ score", "target_score": 80},
            ],
            "total_weeks": 4,
            "available_hours_per_week": 8,
            "exam_ready_date": "2026-07-07",
            "citations": ["[Source: Study Schedule Templates]", "[Source: Workload Insights Report]"],
            "summary": "4-week plan, 8hrs/week available",
        },
        "engagement": {
            "study_slots": [
                {"day": "Monday", "time": "6:30 AM", "duration_minutes": 90},
                {"day": "Wednesday", "time": "6:30 AM", "duration_minutes": 90},
                {"day": "Friday", "time": "6:30 AM", "duration_minutes": 90},
            ],
            "weekly_study_hours": 4.5,
            "capacity_flag": "MODERATE_CAPACITY",
            "capacity_message": "Monitor workload weekly — at risk of study drop-off",
            "reminder_messages": [
                "Alex Chen, your morning study block starts soon — 25 mins to go. Topic: AZ-204 core concepts. [Source: Workload Insights Report]",
                "Weekly check-in: You've completed 3/5 planned study hours this week. Keep it up! [Source: Workload Insights Report]",
                "Exam milestone reminder: AZ-204 practice exam target is 80%+. Schedule a mock exam this weekend. [Source: Study Schedule Templates]",
            ],
            "citations": ["[Source: Workload Insights Report]", "[Source: Study Schedule Templates]"],
            "summary": "3 study slots/week · 4.5hrs · MODERATE_CAPACITY",
        },
        "assessment": {
            "practice_score": 62,
            "pass_threshold": 75,
            "gap": 13,
            "verdict": "APPROACHING",
            "colour": "YELLOW",
            "recommended_action": "3-4 week focused sprint needed",
            "days_to_exam_ready": 26,
            "sample_questions": [
                {"question": "Which Azure service enables serverless event-driven compute?", "answer": "Azure Functions", "topic": "Compute"},
                {"question": "What authentication protocol does Azure AD use for modern apps?", "answer": "OAuth 2.0 / OpenID Connect", "topic": "Security"},
            ],
            "weak_areas": ["Azure Key Vault integration", "Azure Service Bus vs Event Hubs", "RBAC role assignments"],
            "trigger_loop_back": False,
            "citations": ["[Source: AZ-204 Question Bank]", "[Source: Engineering Certification Guide]"],
            "summary": "Score: 62% | Threshold: 75% | Verdict: APPROACHING",
        },
        "peer_benchmark": {
            "percentile": 46.0,
            "cohort_size": 50,
            "cohort_avg_score": 64.2,
            "cohort_avg_hours": 21.3,
            "employee_score": 62,
            "employee_hours": 8,
            "pace_comparison": "Your study pace is 62% slower than the cohort average — consider increasing study hours",
            "benchmark_insight": "You're scoring higher than 46% of Cloud Engineers attempting AZ-204 at the same stage of preparation. Your study pace is 62% slower than the cohort average — consider increasing study hours. [Source: Peer Cohort Benchmarks]",
            "motivation_message": "You're below the cohort median — but 27 peers scored lower. Targeted practice on weak areas will move you up quickly. [Source: Peer Cohort Benchmarks]",
            "citations": ["[Source: Peer Cohort Benchmarks]"],
            "summary": "Percentile: 46% | Cohort avg: 64.2% | Cohort size: 50",
        },
        "roi": {
            "exam_cost_usd": 165,
            "unguided_pass_rate": 0.58,
            "guided_pass_rate": 0.89,
            "unguided_expected_attempts": 1.72,
            "guided_expected_attempts": 1.12,
            "unguided_total_cost_usd": 283.62,
            "guided_total_cost_usd": 185.39,
            "cost_savings_usd": 98.23,
            "productivity_savings_usd": 72.0,
            "total_roi_usd": 170.23,
            "roi_message": "CertifyIQ saves $170 per employee vs unguided exam prep. This includes $98 in reduced retake costs (guided pass rate: 89% vs unguided: 58%) and $72 in productivity recovery. [Source: Certification ROI & Cost Analysis]",
            "citations": ["[Source: Certification ROI & Cost Analysis]"],
            "summary": "ROI: $170 savings | 89% guided pass rate",
        },
        "intervention": None,
        "manager_insights": {
            "team_id": "TEAM-A",
            "team_name": "Cloud Platform & Infrastructure",
            "total_members": 2,
            "ready_count": 1,
            "team_readiness_score": 50.0,
            "executive_summary": "Team TEAM-A has 1/2 members exam-ready (50.0% readiness). 0 members are HIGH RISK. Immediate manager action required for at-risk members. [Source: Manager Readiness Guide]",
            "member_status": [
                {"employee_id": "EMP-001", "name": "Alex Chen", "certification": "AZ-204", "practice_score": 62, "hours_studied": 8, "risk_level": "APPROACHING_READY", "concern": "Score 62% — 13 points below pass threshold", "recommended_action": "Focus on weak areas for 1-2 weeks"},
                {"employee_id": "EMP-002", "name": "Jordan Smith", "certification": "AZ-400", "practice_score": 78, "hours_studied": 18, "risk_level": "ON_TRACK", "concern": "Strong study progress and score trajectory", "recommended_action": "Maintain current pace — on track for pass"},
            ],
            "top_recommendations": [
                "Block calendar time for the 0 high-risk member(s) immediately. [Source: Manager Readiness Guide]",
                "Team readiness is 50.0% — target is 80% before end of quarter. [Source: Team Learning Report]",
                "Schedule weekly 15-min check-ins to review practice scores and study hours. [Source: Manager Readiness Guide]",
            ],
            "citations": ["[Source: Manager Readiness Guide]", "[Source: Team Learning Report]"],
            "summary": "Team score: 50.0% | 1/2 ready",
        },
        "readiness_forecast": {
            "current_score": 62,
            "score_velocity": 3.5,
            "weeks_to_ready": 3.7,
            "forecast_date": "July 2026",
            "confidence": "HIGH",
            "trend": "ACCELERATING",
            "forecast_message": "Forecast: exam-ready in 4 weeks. Velocity: +3.5 pts/week. Confidence: HIGH. [Source: Team Learning Report]",
            "citations": ["[Source: Team Learning Report]"],
            "summary": "Ready in 4 weeks | Velocity: +3.5 pts/wk | HIGH confidence",
        },
    },
    "EMP-002": {
        "employee": {
            "id": "EMP-002",
            "name": "Jordan Smith",
            "role": "DevOps Engineer",
            "certification_target": "AZ-400",
            "current_practice_score": 78,
        },
        "learner_profile": {
            "learner_type": "FAST_TRACKER",
            "learner_type_description": "Practice score >70 and hours <15 — aggressive learner",
            "skill_gap": ["DORA Metrics"],
            "skills_known": ["CI/CD Pipelines", "Infrastructure as Code", "Azure Monitor", "GitHub Actions", "Release Management"],
            "experience_score": 0.45,
            "risk_score": 0.0,
            "score_velocity": 5.2,
            "recommended_approach": "Compressed 2-week sprint — you're efficient. Go aggressive.",
            "citations": ["[Source: Role Skills Matrix]", "[Source: Engineering Certification Guide]"],
            "summary": "Learner type: FAST_TRACKER | Risk: 0% | Gap: 1 skills",
        },
        "learning_path": {
            "certification": "AZ-400",
            "learning_path": [
                {"topic": "Azure Pipelines & CI/CD", "hours": 8, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Infrastructure as Code (Bicep/Terraform)", "hours": 6, "priority": "HIGH", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Release Management & Gates", "hours": 5, "priority": "HIGH", "citation": "[Source: AZ-400 Question Bank]"},
                {"topic": "Practice Exams & Gap Review", "hours": 5, "priority": "HIGH", "citation": "[Source: AZ-400 Question Bank]"},
            ],
            "total_hours": 24,
            "prerequisites": ["AZ-204 or equivalent", "Git proficiency", "CI/CD pipeline experience"],
            "citations": ["[Source: Engineering Certification Guide]", "[Source: Role Skills Matrix]"],
            "summary": "4-topic learning path, 24hrs total",
        },
        "study_plan": {
            "weekly_plan": [
                {"week": 1, "topics": ["Azure Pipelines & CI/CD", "Infrastructure as Code"], "hours": 14, "milestone": "Complete foundational concepts", "target_score": 75},
                {"week": 2, "topics": ["Release Management & Gates", "Practice Exams & Gap Review"], "hours": 10, "milestone": "Final practice exam — target 80%+ score", "target_score": 80},
            ],
            "total_weeks": 2,
            "available_hours_per_week": 14,
            "exam_ready_date": "2026-06-21",
            "citations": ["[Source: Study Schedule Templates]"],
            "summary": "2-week plan, 14hrs/week available",
        },
        "engagement": {
            "study_slots": [
                {"day": "Monday", "time": "7:00 PM", "duration_minutes": 90},
                {"day": "Wednesday", "time": "7:00 PM", "duration_minutes": 90},
                {"day": "Friday", "time": "7:00 PM", "duration_minutes": 90},
            ],
            "weekly_study_hours": 4.5,
            "capacity_flag": "HEALTHY_CAPACITY",
            "capacity_message": "Good conditions for consistent study",
            "reminder_messages": [
                "Jordan Smith, your evening study block starts soon — 25 mins to go. Topic: AZ-400 core concepts. [Source: Workload Insights Report]",
                "Weekly check-in: You've completed 3/5 planned study hours this week. Keep it up! [Source: Workload Insights Report]",
                "Exam milestone reminder: AZ-400 practice exam target is 80%+. Schedule a mock exam this weekend. [Source: Study Schedule Templates]",
            ],
            "citations": ["[Source: Workload Insights Report]", "[Source: Study Schedule Templates]"],
            "summary": "3 study slots/week · 4.5hrs · HEALTHY_CAPACITY",
        },
        "assessment": {
            "practice_score": 78,
            "pass_threshold": 75,
            "gap": 0,
            "verdict": "GO",
            "colour": "GREEN",
            "recommended_action": "Schedule exam within 14 days",
            "days_to_exam_ready": 7,
            "sample_questions": [
                {"question": "What does a deployment gate in Azure Pipelines do?", "answer": "Validates pre/post-deployment conditions before proceeding", "topic": "Release Management"},
                {"question": "What DORA metric measures how quickly you recover from failure?", "answer": "Mean Time to Restore (MTTR)", "topic": "DevOps Metrics"},
            ],
            "weak_areas": ["Release gates configuration", "Infrastructure as Code (Bicep)", "DORA metrics interpretation"],
            "trigger_loop_back": False,
            "citations": ["[Source: AZ-400 Question Bank]", "[Source: Engineering Certification Guide]"],
            "summary": "Score: 78% | Threshold: 75% | Verdict: GO",
        },
        "peer_benchmark": {
            "percentile": 72.0,
            "cohort_size": 50,
            "cohort_avg_score": 71.8,
            "cohort_avg_hours": 24.1,
            "employee_score": 78,
            "employee_hours": 18,
            "pace_comparison": "Your study pace is 25% slower than the cohort average — consider increasing study hours",
            "benchmark_insight": "You're scoring higher than 72% of DevOps Engineers attempting AZ-400 at the same stage of preparation. Your study pace is 25% slower than the cohort average — consider increasing study hours. [Source: Peer Cohort Benchmarks]",
            "motivation_message": "Outstanding! You're in the top 25% of your peer cohort. Keep this momentum to the exam. [Source: Peer Cohort Benchmarks]",
            "citations": ["[Source: Peer Cohort Benchmarks]"],
            "summary": "Percentile: 72% | Cohort avg: 71.8% | Cohort size: 50",
        },
        "roi": {
            "exam_cost_usd": 165,
            "unguided_pass_rate": 0.58,
            "guided_pass_rate": 0.89,
            "unguided_expected_attempts": 1.72,
            "guided_expected_attempts": 1.12,
            "unguided_total_cost_usd": 283.62,
            "guided_total_cost_usd": 185.39,
            "cost_savings_usd": 98.23,
            "productivity_savings_usd": 48.0,
            "total_roi_usd": 146.23,
            "roi_message": "CertifyIQ saves $146 per employee vs unguided exam prep. This includes $98 in reduced retake costs (guided pass rate: 89% vs unguided: 58%) and $48 in productivity recovery. [Source: Certification ROI & Cost Analysis]",
            "citations": ["[Source: Certification ROI & Cost Analysis]"],
            "summary": "ROI: $146 savings | 89% guided pass rate",
        },
        "intervention": None,
        "manager_insights": {
            "team_id": "TEAM-A",
            "team_name": "Cloud Platform & Infrastructure",
            "total_members": 2,
            "ready_count": 1,
            "team_readiness_score": 50.0,
            "executive_summary": "Team TEAM-A has 1/2 members exam-ready (50.0% readiness). 0 members are HIGH RISK. [Source: Manager Readiness Guide]",
            "member_status": [],
            "top_recommendations": [
                "Team readiness is 50.0% — target is 80% before end of quarter. [Source: Team Learning Report]",
            ],
            "citations": ["[Source: Manager Readiness Guide]"],
            "summary": "Team score: 50.0% | 1/2 ready",
        },
        "readiness_forecast": {
            "current_score": 78,
            "score_velocity": 5.2,
            "weeks_to_ready": 0.0,
            "forecast_date": "June 07, 2026",
            "confidence": "HIGH",
            "trend": "ACCELERATING",
            "forecast_message": "You are exam-ready NOW. Score 78% exceeds the 75% threshold. Schedule your AZ-400 exam immediately. [Source: Team Learning Report]",
            "citations": ["[Source: Team Learning Report]"],
            "summary": "Ready in 0 weeks | Velocity: +5.2 pts/wk | HIGH confidence",
        },
    },
    "EMP-003": {
        "employee": {
            "id": "EMP-003",
            "name": "Morgan Lee",
            "role": "Data Engineer",
            "certification_target": "DP-203",
            "current_practice_score": 45,
        },
        "learner_profile": {
            "learner_type": "CAPACITY_LIMITED",
            "learner_type_description": "Meeting hours >22 — time-constrained learner",
            "skill_gap": ["Azure Synapse", "Azure Stream Analytics", "Data Lake", "Spark", "SQL"],
            "skills_known": ["Azure Data Factory"],
            "experience_score": 0.125,
            "risk_score": 1.0,
            "score_velocity": 1.75,
            "recommended_approach": "Micro-sessions of 30 min. Block calendar. Consistency over volume.",
            "citations": ["[Source: Role Skills Matrix]", "[Source: Engineering Certification Guide]"],
            "summary": "Learner type: CAPACITY_LIMITED | Risk: 100% | Gap: 5 skills",
        },
        "learning_path": {
            "certification": "DP-203",
            "learning_path": [
                {"topic": "Azure Data Factory Pipelines", "hours": 10, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Azure Synapse Analytics", "hours": 10, "priority": "HIGH", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Azure Stream Analytics", "hours": 7, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Data Lake Storage Gen2", "hours": 6, "priority": "MED", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Apache Spark in Synapse", "hours": 6, "priority": "MED", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Practice Exams & Gap Review", "hours": 8, "priority": "HIGH", "citation": "[Source: AZ-204 Question Bank]"},
            ],
            "total_hours": 47,
            "prerequisites": ["Basic SQL knowledge", "Azure fundamentals", "Data pipeline concepts"],
            "citations": ["[Source: Engineering Certification Guide]", "[Source: Role Skills Matrix]"],
            "summary": "6-topic learning path, 47hrs total",
        },
        "study_plan": {
            "weekly_plan": [
                {"week": 1, "topics": ["Azure Data Factory Pipelines"], "hours": 4, "milestone": "Complete foundational concepts", "target_score": 48},
                {"week": 2, "topics": ["Azure Synapse Analytics"], "hours": 4, "milestone": "Complete Azure Synapse Analytics module", "target_score": 52},
                {"week": 3, "topics": ["Azure Stream Analytics"], "hours": 4, "milestone": "Complete Azure Stream Analytics module", "target_score": 57},
                {"week": 4, "topics": ["Data Lake Storage Gen2"], "hours": 4, "milestone": "Complete Data Lake Storage Gen2 module", "target_score": 62},
                {"week": 5, "topics": ["Apache Spark in Synapse", "Practice Exams & Gap Review"], "hours": 4, "milestone": "Final practice exam — target 80%+ score", "target_score": 75},
            ],
            "total_weeks": 5,
            "available_hours_per_week": 4,
            "exam_ready_date": "2026-07-12",
            "citations": ["[Source: Study Schedule Templates]", "[Source: Workload Insights Report]"],
            "summary": "5-week plan, 4hrs/week available",
        },
        "engagement": {
            "study_slots": [
                {"day": "Tuesday", "time": "6:30 AM", "duration_minutes": 30},
                {"day": "Thursday", "time": "6:30 AM", "duration_minutes": 30},
                {"day": "Saturday", "time": "9:00 AM", "duration_minutes": 60},
            ],
            "weekly_study_hours": 2.0,
            "capacity_flag": "HIGH_CAPACITY_RISK",
            "capacity_message": "Recommend blocking 2hrs/week from calendar for study",
            "reminder_messages": [
                "Morgan Lee, your morning study block starts soon — 25 mins to go. Topic: DP-203 core concepts. [Source: Workload Insights Report]",
                "Weekly check-in: You've completed 1/3 planned study hours this week. Meeting load is high — try 30-min blocks. [Source: Workload Insights Report]",
                "Exam milestone reminder: DP-203 practice exam target is 80%+. Schedule a mock exam this weekend. [Source: Study Schedule Templates]",
            ],
            "citations": ["[Source: Workload Insights Report]", "[Source: Study Schedule Templates]"],
            "summary": "3 study slots/week · 2.0hrs · HIGH_CAPACITY_RISK",
        },
        "assessment": {
            "practice_score": 45,
            "pass_threshold": 75,
            "gap": 30,
            "verdict": "NOT YET",
            "colour": "RED",
            "recommended_action": "Intensive remediation required — 30 point gap to threshold",
            "days_to_exam_ready": 60,
            "sample_questions": [
                {"question": "Which Azure service is used for orchestrating data pipelines?", "answer": "Azure Data Factory", "topic": "Data Integration"},
                {"question": "What is the purpose of Azure Synapse Analytics?", "answer": "Unified analytics combining data warehousing and big data", "topic": "Analytics"},
            ],
            "weak_areas": ["Synapse vs Databricks distinction", "Partition strategies in Data Lake", "Stream Analytics windowing functions"],
            "trigger_loop_back": True,
            "citations": ["[Source: AZ-204 Question Bank]", "[Source: Engineering Certification Guide]"],
            "summary": "Score: 45% | Threshold: 75% | Verdict: NOT YET",
        },
        "peer_benchmark": {
            "percentile": 22.0,
            "cohort_size": 50,
            "cohort_avg_score": 58.4,
            "cohort_avg_hours": 27.8,
            "employee_score": 45,
            "employee_hours": 5,
            "pace_comparison": "Your study pace is 82% slower than the cohort average — consider increasing study hours",
            "benchmark_insight": "You're scoring higher than 22% of Data Engineers attempting DP-203 at the same stage of preparation. Your study pace is 82% slower than the cohort average — consider increasing study hours. [Source: Peer Cohort Benchmarks]",
            "motivation_message": "You're in the bottom quartile of your cohort right now — this is your signal to intensify. The cohort average (58%) is within reach with 2-3 focused weeks. [Source: Peer Cohort Benchmarks]",
            "citations": ["[Source: Peer Cohort Benchmarks]"],
            "summary": "Percentile: 22% | Cohort avg: 58.4% | Cohort size: 50",
        },
        "roi": {
            "exam_cost_usd": 165,
            "unguided_pass_rate": 0.58,
            "guided_pass_rate": 0.89,
            "unguided_expected_attempts": 1.72,
            "guided_expected_attempts": 1.12,
            "unguided_total_cost_usd": 283.62,
            "guided_total_cost_usd": 185.39,
            "cost_savings_usd": 98.23,
            "productivity_savings_usd": 90.0,
            "total_roi_usd": 188.23,
            "roi_message": "CertifyIQ saves $188 per employee vs unguided exam prep. This includes $98 in reduced retake costs (guided pass rate: 89% vs unguided: 58%) and $90 in productivity recovery. [Source: Certification ROI & Cost Analysis]",
            "citations": ["[Source: Certification ROI & Cost Analysis]"],
            "summary": "ROI: $188 savings | 89% guided pass rate",
        },
        "intervention": {
            "intervention_level": "MEDIUM",
            "manager_email_draft": "Subject: [CertifyIQ Alert] Morgan Lee needs support — DP-203 exam in 5 weeks\n\nHi,\n\nCertifyIQ's AI pipeline has flagged Morgan Lee as requiring immediate support for their upcoming DP-203 certification exam.\n\nCurrent Status:\n• Practice Score: 45% (threshold: 75%)\n• Weeks Until Exam: 5\n• Meeting Load: 24hrs/week (above recommended 16hrs)\n• Key Weak Areas: Synapse vs Databricks distinction, Partition strategies in Data Lake, Stream Analytics windowing functions\n\nRecommended Actions:\n1. Schedule a 30-minute 1:1 with Morgan Lee this week to discuss study challenges\n2. Block 2hrs on Morgan Lee's calendar every Tuesday and Thursday for the next 5 weeks\n3. Consider whether any meetings can be delegated to reduce Morgan Lee's 24hr/week meeting load\n\nFinancial Context:\nWithout intervention, this represents $188 at risk (exam fee + productivity cost).\nWith CertifyIQ-guided prep, pass rates increase from 58% to 89%.\n\nThis is an automated alert from CertifyIQ. Human review required before any action.\n[Source: Intervention Best Practices]",
            "employee_message": "Hi Morgan Lee, we've noticed you're working hard on DP-203 with 5 weeks to go. Your current score of 45% shows real progress, but we want to make sure you have everything you need. Let's focus on Synapse vs Databricks distinction, Partition strategies in Data Lake, Stream Analytics windowing functions — these are your biggest opportunities for score improvement. Small, consistent 30-minute sessions will move the needle more than sporadic long study blocks. Your manager has been notified to help clear some calendar space. You've got this. [Source: Intervention Best Practices]",
            "calendar_recommendation": "Block Tuesday 2-4 PM and Thursday 12-2 PM for the next 5 weeks. Mark as 'Study — DP-203 Prep' and set as 'Busy'. This creates 20 protected study hours before exam date. [Source: Intervention Best Practices]",
            "escalation_triggered": True,
            "roi_at_risk_usd": 188.23,
            "citations": ["[Source: Intervention Best Practices]"],
            "summary": "Intervention: MEDIUM | ROI at risk: $188",
        },
        "manager_insights": {
            "team_id": "TEAM-B",
            "team_name": "Analytics & AI",
            "total_members": 2,
            "ready_count": 0,
            "team_readiness_score": 0.0,
            "executive_summary": "Team TEAM-B has 0/2 members exam-ready (0.0% readiness). 1 members are HIGH RISK. Immediate manager action required for at-risk members. [Source: Manager Readiness Guide]",
            "member_status": [
                {"employee_id": "EMP-003", "name": "Morgan Lee", "certification": "DP-203", "practice_score": 45, "hours_studied": 5, "risk_level": "HIGH_RISK", "concern": "Only 5hrs studied with 5 weeks to exam", "recommended_action": "Urgent 1:1 — consider deferring exam date"},
                {"employee_id": "EMP-004", "name": "Riley Park", "certification": "AI-102", "practice_score": 71, "hours_studied": 14, "risk_level": "APPROACHING_READY", "concern": "Score 71% — 4 points below pass threshold", "recommended_action": "Focus on weak areas for 1-2 weeks"},
            ],
            "top_recommendations": [
                "Block calendar time for the 1 high-risk member(s) immediately. [Source: Manager Readiness Guide]",
                "Team readiness is 0.0% — target is 80% before end of quarter. [Source: Team Learning Report]",
                "Schedule weekly 15-min check-ins to review practice scores and study hours. [Source: Manager Readiness Guide]",
            ],
            "citations": ["[Source: Manager Readiness Guide]", "[Source: Team Learning Report]"],
            "summary": "Team score: 0.0% | 0/2 ready",
        },
        "readiness_forecast": {
            "current_score": 45,
            "score_velocity": 1.75,
            "weeks_to_ready": 17.1,
            "forecast_date": "September 2026",
            "confidence": "MEDIUM",
            "trend": "STEADY",
            "forecast_message": "At current pace, you won't reach 75% threshold before your exam. Score velocity is only +1.75 pts/week. Intervention recommended to accelerate progress. [Source: Team Learning Report]",
            "citations": ["[Source: Team Learning Report]"],
            "summary": "Ready in 17 weeks | Velocity: +1.75 pts/wk | MEDIUM confidence",
        },
    },
    "EMP-004": {
        "employee": {
            "id": "EMP-004",
            "name": "Riley Park",
            "role": "AI Engineer",
            "certification_target": "AI-102",
            "current_practice_score": 71,
        },
        "learner_profile": {
            "learner_type": "ON_SCHEDULE",
            "learner_type_description": "Score improving week-over-week at steady pace",
            "skill_gap": ["NLP", "Bot Framework", "Azure Cognitive Search"],
            "skills_known": ["Azure AI Services", "Azure OpenAI", "Computer Vision"],
            "experience_score": 0.35,
            "risk_score": 0.12,
            "score_velocity": 3.25,
            "recommended_approach": "Maintain steady pace. Weekly practice exams. Focus on weak areas.",
            "citations": ["[Source: Role Skills Matrix]", "[Source: Engineering Certification Guide]"],
            "summary": "Learner type: ON_SCHEDULE | Risk: 12% | Gap: 3 skills",
        },
        "learning_path": {
            "certification": "AI-102",
            "learning_path": [
                {"topic": "Azure AI Services Overview", "hours": 6, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Azure OpenAI Service", "hours": 8, "priority": "HIGH", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Computer Vision & Custom Vision", "hours": 6, "priority": "HIGH", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "NLP & Language Understanding", "hours": 6, "priority": "HIGH", "citation": "[Source: Role Skills Matrix]"},
                {"topic": "Bot Framework & Conversational AI", "hours": 5, "priority": "MED", "citation": "[Source: Engineering Certification Guide]"},
                {"topic": "Practice Exams & Gap Review", "hours": 6, "priority": "HIGH", "citation": "[Source: AZ-204 Question Bank]"},
            ],
            "total_hours": 37,
            "prerequisites": ["Python basics", "REST API familiarity", "Basic ML concepts"],
            "citations": ["[Source: Engineering Certification Guide]", "[Source: Role Skills Matrix]"],
            "summary": "6-topic learning path, 37hrs total",
        },
        "study_plan": {
            "weekly_plan": [
                {"week": 1, "topics": ["Azure AI Services Overview", "Azure OpenAI Service"], "hours": 12, "milestone": "Complete foundational concepts", "target_score": 68},
                {"week": 2, "topics": ["Computer Vision", "NLP & Language Understanding"], "hours": 12, "milestone": "Complete Computer Vision module", "target_score": 74},
                {"week": 3, "topics": ["Bot Framework", "Practice Exams & Gap Review"], "hours": 12, "milestone": "Final practice exam — target 80%+ score", "target_score": 80},
            ],
            "total_weeks": 3,
            "available_hours_per_week": 12,
            "exam_ready_date": "2026-06-28",
            "citations": ["[Source: Study Schedule Templates]"],
            "summary": "3-week plan, 12hrs/week available",
        },
        "engagement": {
            "study_slots": [
                {"day": "Tuesday", "time": "12:00 PM", "duration_minutes": 60},
                {"day": "Thursday", "time": "12:00 PM", "duration_minutes": 60},
                {"day": "Saturday", "time": "10:00 AM", "duration_minutes": 120},
            ],
            "weekly_study_hours": 4.0,
            "capacity_flag": "HEALTHY_CAPACITY",
            "capacity_message": "Good conditions for consistent study",
            "reminder_messages": [
                "Riley Park, your afternoon study block starts soon — 25 mins to go. Topic: AI-102 core concepts. [Source: Workload Insights Report]",
                "Weekly check-in: You've completed 3/5 planned study hours this week. Keep it up! [Source: Workload Insights Report]",
                "Exam milestone reminder: AI-102 practice exam target is 80%+. Schedule a mock exam this weekend. [Source: Study Schedule Templates]",
            ],
            "citations": ["[Source: Workload Insights Report]", "[Source: Study Schedule Templates]"],
            "summary": "3 study slots/week · 4.0hrs · HEALTHY_CAPACITY",
        },
        "assessment": {
            "practice_score": 71,
            "pass_threshold": 75,
            "gap": 4,
            "verdict": "APPROACHING",
            "colour": "YELLOW",
            "recommended_action": "3-4 week focused sprint needed",
            "days_to_exam_ready": 8,
            "sample_questions": [
                {"question": "Which Azure service provides pre-built AI models via REST API?", "answer": "Azure AI Services (Cognitive Services)", "topic": "AI Services"},
                {"question": "What is grounding in Azure OpenAI?", "answer": "Connecting LLM outputs to verified knowledge sources", "topic": "Azure OpenAI"},
            ],
            "weak_areas": ["Azure OpenAI deployment configuration", "Responsible AI principles in practice", "Custom vision model training"],
            "trigger_loop_back": False,
            "citations": ["[Source: AZ-204 Question Bank]", "[Source: Engineering Certification Guide]"],
            "summary": "Score: 71% | Threshold: 75% | Verdict: APPROACHING",
        },
        "peer_benchmark": {
            "percentile": 58.0,
            "cohort_size": 50,
            "cohort_avg_score": 67.1,
            "cohort_avg_hours": 22.6,
            "employee_score": 71,
            "employee_hours": 14,
            "pace_comparison": "Your study pace is 38% slower than the cohort average — consider increasing study hours",
            "benchmark_insight": "You're scoring higher than 58% of AI Engineers attempting AI-102 at the same stage of preparation. Your study pace is 38% slower than the cohort average — consider increasing study hours. [Source: Peer Cohort Benchmarks]",
            "motivation_message": "You're above average in your cohort. A focused final push will put you in the top quarter. [Source: Peer Cohort Benchmarks]",
            "citations": ["[Source: Peer Cohort Benchmarks]"],
            "summary": "Percentile: 58% | Cohort avg: 67.1% | Cohort size: 50",
        },
        "roi": {
            "exam_cost_usd": 165,
            "unguided_pass_rate": 0.58,
            "guided_pass_rate": 0.89,
            "unguided_expected_attempts": 1.72,
            "guided_expected_attempts": 1.12,
            "unguided_total_cost_usd": 283.62,
            "guided_total_cost_usd": 185.39,
            "cost_savings_usd": 98.23,
            "productivity_savings_usd": 60.0,
            "total_roi_usd": 158.23,
            "roi_message": "CertifyIQ saves $158 per employee vs unguided exam prep. This includes $98 in reduced retake costs (guided pass rate: 89% vs unguided: 58%) and $60 in productivity recovery. [Source: Certification ROI & Cost Analysis]",
            "citations": ["[Source: Certification ROI & Cost Analysis]"],
            "summary": "ROI: $158 savings | 89% guided pass rate",
        },
        "intervention": None,
        "manager_insights": {
            "team_id": "TEAM-B",
            "team_name": "Analytics & AI",
            "total_members": 2,
            "ready_count": 0,
            "team_readiness_score": 0.0,
            "executive_summary": "Team TEAM-B has 0/2 members exam-ready (0.0% readiness). [Source: Manager Readiness Guide]",
            "member_status": [],
            "top_recommendations": [
                "Team readiness is 0.0% — target is 80% before end of quarter. [Source: Team Learning Report]",
            ],
            "citations": ["[Source: Manager Readiness Guide]"],
            "summary": "Team score: 0.0% | 0/2 ready",
        },
        "readiness_forecast": {
            "current_score": 71,
            "score_velocity": 3.25,
            "weeks_to_ready": 1.2,
            "forecast_date": "June 14, 2026",
            "confidence": "HIGH",
            "trend": "ACCELERATING",
            "forecast_message": "At your current velocity of +3.25 pts/week, you'll be exam-ready by June 14, 2026. Keep this pace — the finish line is close. [Source: Team Learning Report]",
            "citations": ["[Source: Team Learning Report]"],
            "summary": "Ready in 1 weeks | Velocity: +3.25 pts/wk | HIGH confidence",
        },
    },
}

AGENT_ORDER = [
    (1, "Learner Profiler", "learner_profile"),
    (2, "Learning Path Curator", "learning_path"),
    (3, "Study Plan Generator", "study_plan"),
    (4, "Engagement Agent", "engagement"),
    (5, "Assessment Agent", "assessment"),
    (6, "Peer Benchmarking Agent", "peer_benchmark"),
    (7, "ROI Calculator", "roi"),
    (8, "Intervention Agent", "intervention"),
    (9, "Manager Insights Agent", "manager_insights"),
    (10, "Readiness Forecaster", "readiness_forecast"),
]


class MockEngine:
    def run_pipeline(self, employee_id: str) -> dict:
        """Return complete pipeline results for an employee."""
        mock = MOCK_RESPONSES.get(employee_id)
        if not mock:
            emp = get_employee(employee_id)
            if not emp:
                return {"error": f"Employee {employee_id} not found"}
            mock = MOCK_RESPONSES["EMP-001"]

        results = {}
        for _, _, key in AGENT_ORDER:
            results[key] = mock.get(key)

        verdict = mock["assessment"]["verdict"]
        return {
            "employee_id": employee_id,
            "agents_completed": 10 if mock.get("intervention") else 9,
            "avg_eval_score": 0.87,
            "loop_iterations": 2 if mock["assessment"].get("trigger_loop_back") else 1,
            "intervention_triggered": mock.get("intervention") is not None,
            "verdict": verdict,
            "results": results,
        }

    def stream_pipeline(self, employee_id: str):
        """Generator that yields SSE events for the pipeline."""
        import json
        from datetime import datetime, timezone

        mock = MOCK_RESPONSES.get(employee_id)
        if not mock:
            emp = get_employee(employee_id)
            if not emp:
                yield f"data: {json.dumps({'event': 'error', 'message': f'Employee {employee_id} not found'})}\n\n"
                return
            mock = MOCK_RESPONSES["EMP-001"]

        emp = get_employee(employee_id) or mock["employee"]

        def event(event_type: str, data: dict) -> str:
            return f"data: {json.dumps({'event': event_type, **data})}\n\n"

        yield event("pipeline_start", {
            "employee_id": employee_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agents_count": 10,
            "guardrails": 25,
            "fallback_tiers": 4,
            "mock_mode": True,
        })

        assessment_result = mock["assessment"]
        verdict = assessment_result["verdict"]
        trigger_loop_back = assessment_result.get("trigger_loop_back", False)
        loop_iteration = 1

        # Steps 1-5
        for step, agent_name, key in AGENT_ORDER[:5]:
            result_data = mock.get(key, {})
            yield event("agent_start", {
                "step": step,
                "agent": agent_name,
                "loop_iteration": loop_iteration,
            })
            yield event("agent_complete", {
                "step": step,
                "agent": agent_name,
                "latency_ms": 80 + step * 40,
                "tier_used": 4,
                "eval_score": 0.83 + (step * 0.01),
                "eval_grade": "EXCELLENT" if step % 2 == 0 else "GOOD",
                "guardrails_passed": "25/25",
                "responsible_ai": "PASS",
                "docs_retrieved": 3,
                "citations": result_data.get("citations", ["[Source: Engineering Certification Guide]"]),
                "result_summary": result_data.get("summary", ""),
                "loop_iteration": loop_iteration,
            })

        # Loop back for EMP-003
        if trigger_loop_back:
            loop_iteration = 2
            yield event("loop_back_triggered", {
                "loop_iteration": loop_iteration,
                "reason": "Assessment verdict: NOT YET — re-running study plan with intensive remediation",
                "previous_score": emp.get("current_practice_score", 45),
            })
            # Re-run steps 1-5
            for step, agent_name, key in AGENT_ORDER[:5]:
                result_data = mock.get(key, {})
                yield event("agent_start", {
                    "step": step,
                    "agent": agent_name,
                    "loop_iteration": loop_iteration,
                })
                yield event("agent_complete", {
                    "step": step,
                    "agent": agent_name,
                    "latency_ms": 70 + step * 35,
                    "tier_used": 4,
                    "eval_score": 0.85 + (step * 0.01),
                    "eval_grade": "EXCELLENT",
                    "guardrails_passed": "25/25",
                    "responsible_ai": "PASS",
                    "docs_retrieved": 3,
                    "citations": result_data.get("citations", ["[Source: Engineering Certification Guide]"]),
                    "result_summary": result_data.get("summary", "") + " (remediation iteration)",
                    "loop_iteration": loop_iteration,
                })

        # Steps 6-7
        for step, agent_name, key in AGENT_ORDER[5:7]:
            result_data = mock.get(key, {})
            yield event("agent_start", {
                "step": step,
                "agent": agent_name,
                "loop_iteration": loop_iteration,
            })
            yield event("agent_complete", {
                "step": step,
                "agent": agent_name,
                "latency_ms": 90 + step * 30,
                "tier_used": 4,
                "eval_score": 0.86 + (step * 0.005),
                "eval_grade": "EXCELLENT",
                "guardrails_passed": "25/25",
                "responsible_ai": "PASS",
                "docs_retrieved": 2,
                "citations": result_data.get("citations", ["[Source: Peer Cohort Benchmarks]"]),
                "result_summary": result_data.get("summary", ""),
                "loop_iteration": loop_iteration,
            })

        # Step 8: Intervention (conditional)
        intervention_data = mock.get("intervention")
        if verdict == "NOT YET" or intervention_data:
            yield event("agent_start", {
                "step": 8,
                "agent": "Intervention Agent",
                "loop_iteration": loop_iteration,
            })
            yield event("intervention_alert", {
                "employee_id": employee_id,
                "employee_name": emp.get("name", ""),
                "score": emp.get("current_practice_score", 0),
                "weeks_until_exam": emp.get("weeks_until_exam", 0),
                "intervention_level": (intervention_data or {}).get("intervention_level", "HIGH"),
                "roi_at_risk_usd": (intervention_data or {}).get("roi_at_risk_usd", 165),
            })
            yield event("agent_complete", {
                "step": 8,
                "agent": "Intervention Agent",
                "latency_ms": 150,
                "tier_used": 4,
                "eval_score": 0.88,
                "eval_grade": "EXCELLENT",
                "guardrails_passed": "25/25",
                "responsible_ai": "PASS",
                "docs_retrieved": 2,
                "citations": (intervention_data or {}).get("citations", ["[Source: Intervention Best Practices]"]),
                "result_summary": (intervention_data or {}).get("summary", "Intervention triggered"),
                "loop_iteration": loop_iteration,
            })

        # Steps 9-10
        for step, agent_name, key in AGENT_ORDER[8:10]:
            result_data = mock.get(key, {})
            yield event("agent_start", {
                "step": step,
                "agent": agent_name,
                "loop_iteration": loop_iteration,
            })
            yield event("agent_complete", {
                "step": step,
                "agent": agent_name,
                "latency_ms": 100 + step * 25,
                "tier_used": 4,
                "eval_score": 0.87 + (step * 0.004),
                "eval_grade": "EXCELLENT",
                "guardrails_passed": "25/25",
                "responsible_ai": "PASS",
                "docs_retrieved": 2,
                "citations": result_data.get("citations", ["[Source: Team Learning Report]"]),
                "result_summary": result_data.get("summary", ""),
                "loop_iteration": loop_iteration,
            })

        total_agents = 10 if (verdict == "NOT YET" or intervention_data) else 9
        yield event("pipeline_complete", {
            "employee_id": employee_id,
            "agents_completed": total_agents,
            "avg_eval_score": 0.87,
            "loop_iterations": loop_iteration,
            "intervention_triggered": verdict == "NOT YET" or intervention_data is not None,
            "verdict": verdict,
            "results": {
                "learner_profile": mock.get("learner_profile", {}),
                "learning_path": mock.get("learning_path", {}),
                "study_plan": mock.get("study_plan", {}),
                "engagement": mock.get("engagement", {}),
                "assessment": mock.get("assessment", {}),
                "peer_benchmark": mock.get("peer_benchmark", {}),
                "roi": mock.get("roi", {}),
                "intervention": mock.get("intervention"),
                "manager_insights": mock.get("manager_insights", {}),
                "readiness_forecast": mock.get("readiness_forecast", {}),
            },
        })