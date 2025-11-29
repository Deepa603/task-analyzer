# Smart Task Analyzer

## Overview
The Smart Task Analyzer is a web-based tool to help users **prioritize tasks** based on multiple factors including urgency, importance, estimated effort, and dependencies. It provides **priority scores**, explanations for each score, and suggests the top tasks to focus on.

---

## Algorithm Explanation

### Factors Considered
1. **Urgency** – How close the task is to its due date.
   - Overdue tasks get the highest score.
   - Tasks due soon get moderately high scores.
2. **Importance** – User-defined priority (1-10 scale).
   - High importance tasks contribute significantly to the overall score.
3. **Effort** – Estimated hours to complete the task.
   - Tasks requiring less time get slightly higher scores to encourage quick wins.
4. **Dependencies** – Tasks that block other tasks.
   - Tasks that unlock other tasks get additional points.
5. **Circular Dependency Check**
   - If a circular dependency is detected, the task is flagged with the highest score to alert the user.

### Why Urgency is weighted more than Effort
- Urgency directly impacts deadlines. Completing overdue or soon-due tasks is critical to avoid delays.
- Effort is secondary because small tasks can be quick wins, but missing urgent tasks has a higher cost.
- Weights used:  
  - Urgency: 0.4  
  - Importance: 0.3  
  - Effort: 0.2  
  - Dependency: 0.1

The algorithm combines these factors into a **priority score** between 0 and 10 and provides a **reason/explanation** for each score.

---

## Features
- Add tasks individually or paste a JSON array for bulk input.
- Analyze tasks to calculate priority scores.
- Suggest the top 3 tasks to focus on.
- Visual priority indicators (High/Medium/Low) using color coding.
- Handles circular dependencies gracefully.
- Clean and responsive UI.

---

## Installation & Running the App

### Prerequisites
- Python 3.x
- pip

### Steps

1. Clone the repository
```bash
git clone https://github.com/Deepa603/task-analyzer.git
cd task-analyzer

2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run database migrations
python manage.py migrate

5.Start the Django development server
python manage.py runserver
