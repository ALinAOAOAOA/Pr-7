// Простое приложение "To-Do List" без внешних зависимостей
const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-btn");
const list = document.getElementById("todo-list");
const counter = document.getElementById("counter");
const errorMsg = document.getElementById("error");

// Обновляет счётчик невыполненных задач
function updateCounter() {
  const left = list.querySelectorAll(".todo-item:not(.done)").length;
  counter.textContent = "Осталось задач: " + left;
}

// Добавляет задачу в список
function addTask() {
  const text = input.value.trim();
  if (text === "") {
    errorMsg.hidden = false; // пустую задачу не добавляем
    return;
  }
  errorMsg.hidden = true;

  const li = document.createElement("li");
  li.className = "todo-item";

  const span = document.createElement("span");
  span.className = "todo-text";
  span.textContent = text;
  // клик по тексту отмечает задачу выполненной / снимает отметку
  span.addEventListener("click", () => {
    li.classList.toggle("done");
    updateCounter();
  });

  const del = document.createElement("button");
  del.className = "delete-btn";
  del.type = "button";
  del.textContent = "Удалить";
  del.addEventListener("click", () => {
    li.remove();
    updateCounter();
  });

  li.append(span, del);
  list.appendChild(li);

  input.value = "";
  input.focus();
  updateCounter();
}

addBtn.addEventListener("click", addTask);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") addTask();
});

updateCounter();
