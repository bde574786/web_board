document.getElementById("post_button").addEventListener("click", function () {
    
    var titleValue = document.querySelector('.board_write .title input[type="text"]').value;
    var writerValue = document.querySelector('.board_write .writer input[type="text"]').value;
    var contentValue = document.querySelector('.board_write .content textarea').value;

    var post = {
        title: titleValue,
        writer: writerValue,
        content: contentValue
    }

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

});
