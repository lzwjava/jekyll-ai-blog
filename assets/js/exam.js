console.log("DOM fully loaded and parsed");
const examDiv = document.querySelector('.exam');

if (examDiv) {
    console.log("Exam div found:", examDiv);
    fetchExamQuestions('exams/computer-organization-exam1-en.json')
        .then(questions => {
            console.log("Exam questions fetched successfully:", questions);
            displayQuestions(questions, examDiv);
        })
        .catch(error => {
            console.error('Error fetching or displaying exam questions:', error);
            examDiv.innerHTML = '<p>Failed to load exam questions.</p>';
        });
} else {
    console.error("Exam div not found!");
}

async function fetchExamQuestions(url) {
    console.log("Fetching exam questions from:", url);
    const response = await fetch(url);
    if (!response.ok) {
        console.error("HTTP error! status:", response.status);
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    console.log("Exam questions fetched successfully");
    return await response.json();
}

function displayQuestions(questions, examDiv) {
    console.log("Displaying questions:", questions);
    questions.forEach((questionData, index) => {
        const questionElement = document.createElement('div');
        questionElement.classList.add('question');
        questionElement.innerHTML = `<p><strong>${index + 1}. ${questionData.question}</strong></p>`;

        const choicesElement = document.createElement('ul');
        choicesElement.classList.add('choices');

        questionData.choices.forEach((choice, choiceIndex) => {
            const choiceElement = document.createElement('li');
            const inputId = `question-${index}-choice-${choiceIndex}`;
            choiceElement.innerHTML = `
                <input type="radio" id="${inputId}" name="question-${index}" value="${choiceIndex}">
                <label for="${inputId}">${choice}</label>
            `;
            choicesElement.appendChild(choiceElement);
        });

        questionElement.appendChild(choicesElement);
        examDiv.appendChild(questionElement);
    });

    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit Exam';
    submitButton.addEventListener('click', () => {
        // TODO: Add submission logic here (e.g., collect answers, grade the exam)
        alert('Exam submitted! (Submission logic not yet implemented)');
    });
    examDiv.appendChild(submitButton);
    console.log("Exam displayed successfully");
}
