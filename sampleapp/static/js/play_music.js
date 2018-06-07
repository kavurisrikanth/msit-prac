function markHistory(id) {
    let chatHistory = document.querySelector(id),
        descendants = chatHistory.getElementsByTagName('p');
    for(let i = 0; i < descendants.length; i++) {
        someDiv = descendants[i];

        if(someDiv.getAttribute('class') === 'msg_text') {
            someDiv.addEventListener("click", function (event) {
                copyAndPlay(event.target.innerText);
                // console.log(event.target.innerText);
            });
        }
    }
}

function copyAndPlay(text) {
    let textArea = document.querySelector('#s1');
    s1.value = text;
    piano.recplay();
}