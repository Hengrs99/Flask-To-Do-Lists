function deleteList(listId) {
  fetch("/delete_list", {
    method: "POST",
    body: JSON.stringify({ listId: listId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function getListId(listId) {
  fetch("/get_list_id", {
    method: "POST",
    body: JSON.stringify({ listId: listId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function updateTaskState(taskId) {
  fetch("/update_task_state", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/open_list";
  });
}

function addTask() {
  fetch("/add_task", {
    method: "POST",
    body: JSON.stringify({ taskText: document.getElementById('addTaskBox').value }),
  }).then((_res) => {
    window.location.href = "/open_list";
  });
}

function deleteTask(taskId) {
  fetch("/delete_task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/open_list";
  });
}

function returnToLists() {
  fetch("/return_to_lists", {method: "GET"}).then((_res) => {window.location.href = "/return_to_lists";});
}