document.getElementById("post_button").addEventListener("click", function () {
    
    var titleValue = document.querySelector('.board_write .title input[type="text"]').value;
    var writerValue = document.querySelector('.board_write .info input[type="text"]').value;
    var checkbox = document.getElementById("checkbox");
    var secretKeyValue = document.getElementById('password').value;
    var contentValue = document.querySelector('.board_write .content textarea').value;

    var post = {
            title: titleValue,
            writer: writerValue,
            secretKey: secretKeyValue,
            content: contentValue
        }
    

    if (!checkbox.checked || (checkbox.checked && secretKeyValue.length > 0)) {
        $.ajax({
            type: "POST",
            url: "/write_post",
            contentType: "application/json",
            data: JSON.stringify(post),
            success: function (response) {
                if (response === "success") {
                    alert("글 쓰기 성공 !!")
                    window.location.href = "/index";
                } else {
                    alert(response)
                }
            }
        })
    } else {
        alert("비밀번호가 입력되지 않았습니다.")
    }



});

function isChecked() {
    var checkbox = document.getElementById("checkbox");
    var secretKeyField = document.getElementById("password");

    if (checkbox.checked) {
        secretKeyField.disabled = false;
    } else {
        secretKeyField.disabled = true;
    }
}