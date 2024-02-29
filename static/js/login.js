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




function openFindId() {
    var popup;
    if (!popup || popup.closed) {
        popup = window.open('/find_id', 'newwindow', 'width=500,height=500');
    } else {
        popup.focus();
        return;
    }

    popup.addEventListener('DOMContentLoaded', function () {
        popup.document.getElementById('find_button').addEventListener('click', function() {
            var name = popup.document.getElementById('name').value;
            var phoneNumber = popup.document.getElementById('phoneNumber').value;

            var data = {
                'name': name,
                'phoneNumber': phoneNumber
            }

            fetch("/get_id", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    var container = popup.document.getElementById('container');
                    var customAlert = popup.document.getElementById('customAlert');
                    var alertMessage = popup.document.getElementById('alertMessage');

                    customAlert.style.display = 'block';
                    container.style.display = 'none';
                    
                    if (data) {    
                        alertMessage.textContent = "회원님의 아이디는" + data[0] + "입니다."
                    } else {
                        alertMessage.textContent = "정보를 찾을 수 없습니다."
                    }
                })
                .catch(error => {
                    console.error("요청을 완료할 수 없습니다:", error);
                });
        });
    });
}


function openFindPassword() {
    var popup;
    if (!popup || popup.closed) {
        popup = window.open('/find_password', 'newwindow', 'width=500,height=500');
    } else {
        popup.focus();
        return;
    }

    popup.addEventListener('DOMContentLoaded', function () {
        popup.document.getElementById('find_button').addEventListener('click', function () {
            var id = popup.document.getElementById('id').value;
            var name = popup.document.getElementById('name').value;
            var phoneNumber = popup.document.getElementById('phoneNumber').value;

            var data = {
                'id': id,
                'name': name,
                'phoneNumber': phoneNumber
            }

            fetch("/get_password", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    var container = popup.document.getElementById('container');
                    var customAlert = popup.document.getElementById('customAlert');
                    var alertMessage = popup.document.getElementById('alertMessage');

                    customAlert.style.display = 'block';
                    container.style.display = 'none';

                    if (data) {    
                        alertMessage.textContent = "회원님의 비밀번호는" + data[0] + "입니다."
                    } else {
                        alertMessage.textContent = "정보를 찾을 수 없습니다."
                    }
                })
                .catch(error => {
                    console.error("요청을 완료할 수 없습니다:", error);
                });
        });
    });
}