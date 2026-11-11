// 1. POBIERANIE ELEMENTÓW HTML ===============================

const taskForm = document.getElementById("task-form");
const taskTitle = document.getElementById("task-title");
const taskList = document.getElementById("task-list");
const message = document.getElementById("message");

const totalCount = document.getElementById("total-count");
const completedCount = document.getElementById("completed-count");

const filterButtons = document.querySelectorAll(".filter-btn");


// 2. ZMIENNE PRZECHOWUJĄCE STAN APLIKACJI =====================

let tasks = [];
let currentFilter = "all";


// 3. POBIERANIE TOKENU CSRF ==================================

const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;


// 4. WYŚWIETLANIE KOMUNIKATÓW ================================

function showMessage(text, type = "error") {
    message.textContent = text;
    message.className = "message " + type;
}


// 5. OBSŁUGA ODPOWIEDZI API ==================================

async function checkResponse(response) {
    if (!response.ok) {
        let errorMessage = "Wystąpił błąd API.";

        try {
            const data = await response.json();

            if (data.error) {
                errorMessage = data.error;
            }
        } catch (error) {
            errorMessage = "Nie udało się odczytać odpowiedzi serwera.";
        }

        throw new Error(errorMessage);
    }

    return response.json();
}


// 6. POBIERANIE ZADAŃ Z API ==================================

async function loadTasks() {
    try {
        const response = await fetch("/api/tasks/");

        tasks = await checkResponse(response);

        renderTasks();
        updateCounters();

        return true;

    } catch (error) {
        showMessage(error.message);
        return false;
    }
}

// 7. AKTUALIZACJA LICZNIKÓW ==================================

function updateCounters() {
    totalCount.textContent = tasks.length;

    const completedTasks = tasks.filter(
        task => task.completed
    );

    completedCount.textContent = completedTasks.length;
}


// 8. FILTROWANIE ZADAŃ =======================================

function getFilteredTasks() {
    if (currentFilter === "active") {
        return tasks.filter(task => !task.completed);
    }

    if (currentFilter === "completed") {
        return tasks.filter(task => task.completed);
    }

    return tasks;
}


// 9. WYŚWIETLANIE LISTY ZADAŃ ================================

function renderTasks() {
    taskList.replaceChildren();

    const filteredTasks = getFilteredTasks();

    if (filteredTasks.length === 0) {
        const emptyItem = document.createElement("li");

        emptyItem.textContent = "Brak zadań do wyświetlenia.";
        emptyItem.className = "task-item";

        taskList.appendChild(emptyItem);
        return;
    }

    filteredTasks.forEach(task => {
        const item = document.createElement("li");
        item.className = "task-item";

        if (task.completed) {
            item.classList.add("completed");
        }

        const title = document.createElement("span");
        title.className = "task-title";
        title.textContent = task.title;

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const statusButton = document.createElement("button");
        statusButton.type = "button";

        statusButton.textContent = task.completed
            ? "Przywróć"
            : "Ukończ";

        statusButton.addEventListener("click", () => {
            toggleTask(task);
        });

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Usuń";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });

        actions.appendChild(statusButton);
        actions.appendChild(deleteButton);

        item.appendChild(title);
        item.appendChild(actions);

        taskList.appendChild(item);
    });
}


// 10. DODAWANIE NOWEGO ZADANIA ===============================

async function addTask(event) {
    event.preventDefault();

    const title = taskTitle.value.trim();

    if (!title) {
        showMessage("Treść zadania nie może być pusta.");
        return;
    }

    if (title.length > 200) {
        showMessage("Zadanie może mieć maksymalnie 200 znaków.");
        return;
    }

    try {
        const response = await fetch("/api/tasks/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ title: title })
        });

        await checkResponse(response);

        taskForm.reset();
        showMessage("Zadanie zostało dodane.", "success");

        const loaded = await loadTasks();

        if (!loaded) {
            showMessage(
                "Operacja została zapisana, ale nie udało się odświeżyć listy."
            );
        }

    } catch (error) {
        showMessage(error.message);
    }
}


// 11. ZMIANA STATUSU ZADANIA =================================

async function toggleTask(task) {
    try {
        const response = await fetch(`/api/tasks/${task.id}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                completed: !task.completed
            })
        });

        await checkResponse(response);

        showMessage("Status zadania został zmieniony.", "success");

        const loaded = await loadTasks();

        if (!loaded) {
            showMessage(
                "Operacja została zapisana, ale nie udało się odświeżyć listy."
            );
        }

    } catch (error) {
        showMessage(error.message);
    }
}


// 12. USUWANIE ZADANIA =======================================

async function deleteTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken
            }
        });

        await checkResponse(response);

        showMessage("Zadanie zostało usunięte.", "success");

        const loaded = await loadTasks();

        if (!loaded) {
            showMessage(
                "Operacja została zapisana, ale nie udało się odświeżyć listy."
            );
        }
        
    } catch (error) {
        showMessage(error.message);
    }
}


// 13. OBSŁUGA PRZYCISKÓW FILTROWANIA =========================

filterButtons.forEach(button => {
    button.addEventListener("click", () => {
        currentFilter = button.dataset.filter;

        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        renderTasks();
    });
});


// 14. OBSŁUGA FORMULARZA =====================================

taskForm.addEventListener("submit", addTask);


// 15. POBRANIE ZADAŃ PO OTWARCIU STRONY ======================

loadTasks();