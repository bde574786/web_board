document.getElementById('post_button').addEventListener("click", function () {

    var post_id = document.getElementById('post_id').value;
    var titleValue = document.querySelector('.board_write .title input[type="text"]').value;
    var writerValue = document.querySelector('.board_write .writer input[type="text"]').value;
    var contentValue = document.querySelector('.board_write .content textarea').value;

    post = {"id": post_id, "title": titleValue, "writer": writerValue, "content": contentValue}
    
    $.ajax({
        type: "POST",
        url: "/edit_post/" + post_id,
        contentType: "application/json",
        data: JSON.stringify(post),
        success: function (response) {
            if (response === "success") {
                alert("글 수정 성공 !!")
                window.location.href = "/view_post/" + post_id
            } else {
                alert(response)
            }
    }
})

})