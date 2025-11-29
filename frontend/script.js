const analyzeBtn = document.getElementById("analyze-btn");
const suggestBtn = document.getElementById("suggest-btn");
const addTaskBtn = document.getElementById("add-task-btn");
const tasksInput = document.getElementById("tasks-input");
const tasksOutput = document.getElementById("tasks-output");
const sortDropdown = document.getElementById("sort-strategy");

// Store all tasks in this array
let taskList = [];

// ----------------- Priority Display -----------------
function getPriorityClass(score) {
    if (score >= 7) return "high";
    if (score >= 4) return "medium";
    return "low";
}

// ----------------- Sorting Strategies -----------------
function sortTasks(tasks) {
    const strategy = sortDropdown.value;
    return tasks.slice().sort((a, b) => {
        switch(strategy) {
            case "fastest": // low estimated hours first
                return (a.estimated_hours || 0) - (b.estimated_hours || 0);
            case "impact": // high importance first
                return (b.importance || 0) - (a.importance || 0);
            case "deadline": // earliest due date first
                const dateA = a.due_date ? new Date(a.due_date) : new Date(2100,0,1);
                const dateB = b.due_date ? new Date(b.due_date) : new Date(2100,0,1);
                return dateA - dateB;
            case "smart": // use calculated score
            default:
                return (b.score || 0) - (a.score || 0);
        }
    });
}

// ----------------- Render Tasks -----------------
function renderTasks(tasks) {
    tasksOutput.innerHTML = "";
    const sortedTasks = sortTasks(tasks);
    sortedTasks.forEach(task => {
        const div = document.createElement("div");
        div.className = `task-card ${getPriorityClass(task.score)}`;
        div.innerHTML = `
            <div class="task-title">${task.title} (Score: ${task.score})</div>
            <div class="task-details">Due: ${task.due_date || "N/A"}, Hours: ${task.estimated_hours || "N/A"}, Importance: ${task.importance || "N/A"}</div>
            <div class="task-explanation">Reason: ${task.explanation.join(", ")}</div>
        `;
        tasksOutput.appendChild(div);
    });
}

// ----------------- Add Single Task -----------------
addTaskBtn.addEventListener("click", () => {
    const title = document.getElementById("title").value.trim();
    const due_date = document.getElementById("due_date").value;
    const importance = parseInt(document.getElementById("importance").value);
    const estimated_hours = parseInt(document.getElementById("hours").value);
    const dependencies = document.getElementById("dependencies").value
                            .split(",")
                            .map(d => d.trim())
                            .filter(d => d);

    if (!title) { alert("Title is required"); return; }

    const newTask = { title, due_date, importance, estimated_hours, dependencies };

    // Add to task list
    taskList.push(newTask);

    // Update JSON textarea
    tasksInput.value = JSON.stringify(taskList, null, 2);

    // Clear form
    document.getElementById("title").value = "";
    document.getElementById("due_date").value = "";
    document.getElementById("importance").value = "";
    document.getElementById("hours").value = "";
    document.getElementById("dependencies").value = "";

    renderTasks(taskList);
});

// ----------------- Analyze / Suggest Tasks -----------------
async function postTasks(url) {
    let tasks;
    try {
        tasks = JSON.parse(tasksInput.value);
        if (!Array.isArray(tasks)) throw "Input must be a JSON array";
    } catch (err) {
        alert("Invalid JSON input: " + err);
        return;
    }

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(tasks)
        });
        const data = await res.json();
        if (res.ok) {
            // Update taskList with scores for consistent rendering
            taskList = data;
            renderTasks(taskList);
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert("Error contacting server: " + err);
    }
}

analyzeBtn.addEventListener("click", () => postTasks("/api/tasks/analyze/"));
suggestBtn.addEventListener("click", () => postTasks("/api/tasks/suggest/"));

// ----------------- Sorting Dropdown -----------------
sortDropdown.addEventListener("change", () => renderTasks(taskList));
