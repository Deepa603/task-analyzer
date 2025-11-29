from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task
from .scoring import calculate_priority
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')


@csrf_exempt
def analyze_tasks(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    try:
        data = json.loads(request.body)
        if not isinstance(data, list):
            raise ValueError("Input must be a JSON array")
        tasks_with_scores = []
        for task in data:
            score, explanation = calculate_priority(task, all_tasks=data)
            task['score'] = score
            task['explanation'] = explanation
            tasks_with_scores.append(task)
        sorted_tasks = sorted(tasks_with_scores, key=lambda x: x['score'], reverse=True)
        return JsonResponse(sorted_tasks, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def suggest_tasks(request):
    """
    GET: Fetch tasks from DB or fallback mock tasks
    POST: Use submitted JSON tasks
    Returns top 3 tasks with explanations
    """
    try:
        if request.method == "GET":
            tasks = Task.objects.all()
            if not tasks.exists():
                tasks = [
                    {"title": "Sample Task 1", "due_date": "2025-12-02", "importance": 9, "estimated_hours": 2, "dependencies": []},
                    {"title": "Sample Task 2", "due_date": "2025-12-06", "importance": 6, "estimated_hours": 3, "dependencies": []},
                    {"title": "Sample Task 3", "due_date": "2025-12-09", "importance": 4, "estimated_hours": 4, "dependencies": []},
                ]
            task_list = []
            for t in tasks:
                if isinstance(t, Task):
                    t_dict = {
                        "title": t.title,
                        "due_date": str(t.due_date),
                        "importance": t.importance,
                        "estimated_hours": t.estimated_hours,
                        "dependencies": t.dependencies
                    }
                else:
                    t_dict = t
                score, explanation = calculate_priority(t_dict, all_tasks=task_list)
                t_dict['score'] = score
                t_dict['explanation'] = explanation
                task_list.append(t_dict)

        elif request.method == "POST":
            data = json.loads(request.body)
            if not isinstance(data, list):
                raise ValueError("Input must be a JSON array")
            task_list = []
            for task in data:
                score, explanation = calculate_priority(task, all_tasks=data)
                task['score'] = score
                task['explanation'] = explanation
                task_list.append(task)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

        top_tasks = sorted(task_list, key=lambda x: x['score'], reverse=True)[:3]
        return JsonResponse(top_tasks, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
