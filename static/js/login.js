document.getElementById('login_form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    var userId = document.getElementById('userId').value;
    var password = document.getElementById('password').value;

    var data = {
        'userId': userId,
        'password': password
    } 

    fetch("/user_login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.text())
        .then(text => {
            if (text === 'success') {
                alert(userId + "님 환영합니다.");
                window.location.href = '/index';
            } else {
                alert("아이디 또는 비밀번호가 일치하지 않습니다.");
        }
        }).catch(error => {
            alert("요청을 완료할 수 없습니다.")
    })

})