from datetime import date

def detect_circular_dependency(task, all_tasks, visited=None, stack=None):
    """
    Detect circular dependency using DFS.
    Returns True if a cycle exists.
    """
    if visited is None:
        visited = set()
    if stack is None:
        stack = set()

    task_title = task.get("title")
    if task_title in stack:
        return True
    if task_title in visited:
        return False

    visited.add(task_title)
    stack.add(task_title)

    for dep in task.get("dependencies", []):
        dep_task = next((t for t in all_tasks if t.get("title") == dep), None)
        if dep_task and detect_circular_dependency(dep_task, all_tasks, visited, stack):
            return True

    stack.remove(task_title)
    return False


def calculate_priority(task, all_tasks=None, weights=None):
    """
    Calculate task priority score and provide explanations.
    weights: dict like {"urgency": 0.4, "importance": 0.3, "effort": 0.2, "dependency": 0.1}
    """
    explanation = []
    all_tasks = all_tasks or []

    # Set default weights if not provided
    weights = weights or {"urgency": 0.4, "importance": 0.3, "effort": 0.2, "dependency": 0.1}

    # --- Circular dependency check ---
    if detect_circular_dependency(task, all_tasks):
        explanation.append("⚠ Circular dependency detected")
        # Assign high score to alert user
        return 10.0, explanation

    # --- Urgency Factor ---
    due_date_str = task.get("due_date")
    try:
        due_date = date.fromisoformat(due_date_str) if due_date_str else None
        days_left = (due_date - date.today()).days if due_date else None
    except Exception:
        days_left = None

    if days_left is None:
        urgency = 5
        explanation.append("No valid due date")
    elif days_left < 0:
        urgency = 10
        explanation.append("Overdue task")
    elif days_left <= 2:
        urgency = 8
        explanation.append("Due very soon")
    elif days_left <= 7:
        urgency = 5
    else:
        urgency = 2

    # --- Importance Factor ---
    importance = task.get("importance", 5)
    if not isinstance(importance, int) or not (1 <= importance <= 10):
        importance = 5
        explanation.append("Invalid importance, set to default")
    elif importance >= 8:
        explanation.append("High importance")

    # --- Effort Factor ---
    estimated_hours = task.get("estimated_hours", 5)
    try:
        effort_score = max(0, 10 - int(estimated_hours))
        if estimated_hours <= 2:
            explanation.append("Quick to complete")
    except Exception:
        effort_score = 5
        explanation.append("Invalid estimated hours, set to default")

    # --- Dependency Factor ---
    dependency_score = 0
    if all_tasks and task.get("dependencies"):
        dependency_score = sum(1 for t in all_tasks if t.get("title") in task["dependencies"]) * 2
        explanation.append(f"Blocks {len(task['dependencies'])} tasks")

    # --- Weighted sum ---
    score = (weights["urgency"] * urgency +
             weights["importance"] * importance +
             weights["effort"] * effort_score +
             weights["dependency"] * dependency_score)

    return round(score, 2), explanation or ["Regular priority"]
