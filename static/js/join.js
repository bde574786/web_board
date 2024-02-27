document.getElementById('joinForm').onsubmit = function (e) {
    var password = document.getElementById('password').value;
    var rePassword = document.getElementById('rePassword').value;

    if (password !== rePassword) {
        e.preventDefault();
        alert("패스워드가 일치하지 않습니다.")
    }

}