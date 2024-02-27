document.getElementById('joinForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var userId = document.getElementById('userId').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var rePassword = document.getElementById('rePassword').value;
    var phoneNumber = document.getElementById('phoneNumber').value;
    var phoneNumberReg = /^01([0|1|6|7|8|9])-([0-9]{3,4})-([0-9]{4})$/;
    var passwordReg = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;


    if (!checkPhoneNumber(phoneNumberReg, phoneNumber, e) || !checkPassword(password, rePassword, e) || !checkValidPassword(passwordReg, password, e)) {
        return;
    } else {

        var data = {
            'userId': userId,
            'username': username,
            'phoneNumber': phoneNumber,
            'password': password
        }
        
        fetch("/register_user", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.text())
            .then(text => {
                if (text === 'success') {
                    alert('회원가입 성공');
                    window.location.href = '/login';
                } else if (text === 'duplicate_id') {
                    alert('아이디가 존재합니다.');
                } else {
                    alert('회원가입 실패');
            }
            }).catch(error => {
                alert("요청을 완료할 수 없습니다.")
            })
    }  

})

function checkPhoneNumber(phoneNumberReg, phoneNumber, e) {
    if (!phoneNumberReg.test(phoneNumber)) {
        alert("전화번호가 형식과 맞지 않습니다. ex) 010-0000-0000");
        return false;
    }
    return true;
}

function checkPassword(password, rePassword, e) {
    if (password !== rePassword) {
        alert("패스워드가 일치하지 않습니다.");
        return false;
    }
    return true;
}

function checkValidPassword(passwordReg, password, e) {
    if (!passwordReg.test(password)) {
        alert("비밀번호는 8자 이상이어야 하며, 숫자, 영어 대소문자, 특수문자를 모두 포함하여야 합니다.");
        return false;
    }
    return true;
}

