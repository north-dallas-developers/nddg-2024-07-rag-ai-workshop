
const input = document.querySelector('[name="query"]');
const outputNode = document.querySelector('.output');
console.log('input', input);

input.addEventListener('keyup', (evt) => {
    if (evt.key === 'Enter' || evt.keyCode === 13) {
        
        const url = '/send-query';

        const formData = new FormData();
        formData.append('query', input.value);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            outputNode.innerHTML = '';

            const questionNode = document.createElement('h3');
            questionNode.textContent = input.value;

            const answerNode = document.createElement('div');
            let message = data.message.replace(/(\r\n|\n|\r)/g, '<br />');
            answerNode.innerHTML = message;

            outputNode.appendChild(questionNode);
            outputNode.appendChild(answerNode);

        })
        .catch((error) => {
            console.error('Error:', error);
        });
        


    }
});


