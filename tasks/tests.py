# tests.py
from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_priority

class ScoringTests(TestCase):

    def test_normal_task(self):
        """Test a normal task with no dependencies and future due date"""
        task = {
            "title": "Normal Task",
            "due_date": (date.today() + timedelta(days=5)).isoformat(),
            "estimated_hours": 3,
            "importance": 7,
            "dependencies": []
        }
        score = calculate_priority(task)
        self.assertTrue(0 <= score <= 10)
        print(f"Normal Task Score: {score}")

    def test_past_due_task(self):
        """Test a task that is past due"""
        task = {
            "title": "Past Due Task",
            "due_date": (date.today() - timedelta(days=2)).isoformat(),
            "estimated_hours": 4,
            "importance": 6,
            "dependencies": []
        }
        score = calculate_priority(task)
        self.assertEqual(score, 0.4*10 + 0.3*6 + 0.2*(10-4))  # manual check
        print(f"Past Due Task Score: {score}")

    def test_task_with_dependencies(self):
        """Test a task that blocks other tasks"""
        all_tasks = [
            {"title": "Task A", "dependencies": []},
            {"title": "Task B", "dependencies": ["Task C"]},
            {"title": "Task C", "dependencies": []},
        ]
        task = {
            "title": "Task B",
            "due_date": (date.today() + timedelta(days=3)).isoformat(),
            "estimated_hours": 2,
            "importance": 8,
            "dependencies": ["Task C"]
        }
        score = calculate_priority(task, all_tasks=all_tasks)
        self.assertTrue(score > 0)
        print(f"Task with Dependencies Score: {score}")
