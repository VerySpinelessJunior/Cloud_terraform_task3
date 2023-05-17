// Инициализация Codemirror
var codeEditor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    tabSize: 4,
    indentWithTabs: true,
    theme: "xq-light",
    mode: "python"
});

// Функция выполнения кода
function executeCode(type) {
    var code = codeEditor.getValue();

    if(type == "back"){
        var xhr = new XMLHttpRequest();
        var url = '/run_code';
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                handleResponse(response);
            }
        };

        var requestBody = JSON.stringify({ code: code });
        xhr.send(requestBody);
    }

    if(type == "front"){
        var response = execute_python(code, "").$string_dict
        handleResponse(response);
    }
}

// Функция обработки ответа
function handleResponse(response) {
    var outputElement = document.getElementById("output");
    outputElement.innerHTML = ""; // Очистить содержимое элемента вывода

    if (response.output) {
        outputElement.classList.remove("error");
        outputElement.classList.add("success");
        outputElement.textContent = response.output;
    } else if (response.error) {
        outputElement.classList.remove("success");
        outputElement.classList.add("error");
        outputElement.textContent = response.error;
    }
}

// Обработчик события нажатия на кнопку "Выполнить код" (бек)
<!-- document.getElementById("execute-button-back").addEventListener("click", function() { -->
<!-- executeCode("back"); -->
<!-- });	 -->

// Обработчик события нажатия на кнопку "Выполнить код" (фронт)
document.getElementById("execute-button-front").addEventListener("click", function() {
    executeCode("front");
});

// Функция добавления теста
function addTest(description, output) {
    var tableBody = document.getElementById("test-table-body");
    var row = document.createElement("tr");
    var descriptionCell = document.createElement("td");
    var outputCell = document.createElement("td");
    var buttonCell = document.createElement("td");
    var checkButton = document.createElement("button");

    descriptionCell.textContent = description;
    outputCell.textContent = output;
    checkButton.textContent = "Проверить тест";
    checkButton.classList.add("btn", "btn-primary", "test-button");

    row.appendChild(descriptionCell);
    row.appendChild(outputCell);
    row.appendChild(buttonCell);
    buttonCell.appendChild(checkButton);
    tableBody.appendChild(row);
}

// Обработчик события переключения темы
document.getElementById("dark-mode-toggle").addEventListener("change", function() {
    var body = document.body;
    <!-- var executeButtonBack = document.getElementById("execute-button-back"); -->
    var executeButtonFront = document.getElementById("execute-button-front");
    var executeTests = document.getElementById("execute-tests");
    var thElements = document.querySelectorAll(".test-table th");
    var testButtons = document.querySelectorAll(".test-button");

    if (this.checked) {
        body.classList.add("dark-mode");
        codeEditor.setOption('theme', 'seti');
        <!-- executeButtonBack.classList.remove("btn-primary"); -->
        <!-- executeButtonBack.classList.add("btn-light"); -->
        executeButtonFront.classList.remove("btn-primary");
        executeButtonFront.classList.add("btn-light");
        executeTests.classList.remove("btn-primary");
        executeTests.classList.add("btn-light");

        thElements.forEach(function(element) {
            element.classList.add("dark-mode");
        });

        testButtons.forEach(function(button) {
            button.classList.add("btn-light");
        });
    } else {
        body.classList.remove("dark-mode");
        codeEditor.setOption('theme', 'xq-light');
        <!-- executeButtonBack.classList.remove("btn-light"); -->
        <!-- executeButtonBack.classList.add("btn-primary"); -->
        executeButtonFront.classList.remove("btn-light");
        executeButtonFront.classList.add("btn-primary");
        executeTests.classList.remove("btn-light");
        executeTests.classList.add("btn-primary");

        thElements.forEach(function(element) {
            element.classList.remove("dark-mode");
        });

        testButtons.forEach(function(button) {
            button.classList.remove("btn-light");
        });
    }
});

function toggleTask(event) {
    event.preventDefault();
    var taskItem = event.target.parentNode;
    var taskDescription = taskItem.querySelector('.task-description');
    taskDescription.classList.toggle('show');
}

// Добавление тестов
addTest("Тест 1", "Вывод 1");
addTest("Тест 2", "Вывод 2");