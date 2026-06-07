from __future__ import annotations
from datetime import date
from typing import Optional

EMPLOYEES = {
    "EMP-001": {
        "id": "EMP-001",
        "name": "Alex Chen",
        "role": "Cloud Engineer",
        "department": "Cloud Platform",
        "team_id": "TEAM-A",
        "certification_target": "AZ-204",
        "current_practice_score": 62,
        "hours_studied": 8,
        "focus_hours_per_week": 14,
        "meeting_hours_per_week": 18,
        "weeks_until_exam": 4,
        "starting_score": 48,
        "preferred_study_time": "Morning",
        "manager_id": "MGR-001",
    },
    "EMP-002": {
        "id": "EMP-002",
        "name": "Jordan Smith",
        "role": "DevOps Engineer",
        "department": "Infrastructure",
        "team_id": "TEAM-A",
        "certification_target": "AZ-400",
        "current_practice_score": 78,
        "hours_studied": 18,
        "focus_hours_per_week": 20,
        "meeting_hours_per_week": 12,
        "weeks_until_exam": 3,
        "starting_score": 55,
        "preferred_study_time": "Evening",
        "manager_id": "MGR-001",
    },
    "EMP-003": {
        "id": "EMP-003",
        "name": "Morgan Lee",
        "role": "Data Engineer",
        "department": "Analytics",
        "team_id": "TEAM-B",
        "certification_target": "DP-203",
        "current_practice_score": 45,
        "hours_studied": 5,
        "focus_hours_per_week": 8,
        "meeting_hours_per_week": 24,
        "weeks_until_exam": 5,
        "starting_score": 38,
        "preferred_study_time": "Morning",
        "manager_id": "MGR-002",
    },
    "EMP-004": {
        "id": "EMP-004",
        "name": "Riley Park",
        "role": "AI Engineer",
        "department": "AI & Cognitive",
        "team_id": "TEAM-B",
        "certification_target": "AI-102",
        "current_practice_score": 71,
        "hours_studied": 14,
        "focus_hours_per_week": 18,
        "meeting_hours_per_week": 15,
        "weeks_until_exam": 3,
        "starting_score": 58,
        "preferred_study_time": "Afternoon",
        "manager_id": "MGR-002",
    },
}

TEAMS = {
    "TEAM-A": {
        "team_id": "TEAM-A",
        "name": "Cloud Platform & Infrastructure",
        "manager": "Ananya Patel",
        "manager_id": "MGR-001",
        "members": ["EMP-001", "EMP-002"],
    },
    "TEAM-B": {
        "team_id": "TEAM-B",
        "name": "Analytics & AI",
        "manager": "David Kim",
        "manager_id": "MGR-002",
        "members": ["EMP-003", "EMP-004"],
    },
}


def get_employee(employee_id: str) -> Optional[dict]:
    return EMPLOYEES.get(employee_id)


def get_all_employees() -> list:
    return list(EMPLOYEES.values())


def get_team(team_id: str) -> Optional[dict]:
    return TEAMS.get(team_id)