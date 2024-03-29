document.getElementById('delete_button').addEventListener("click", function () {

    var post_id = document.getElementById('post_id').textContent;
    data = {"id": post_id}

    $.ajax({
        type: "POST",
        url: "/delete_post/" + post_id,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            if (response === "success") {
                alert("글 삭제 성공 !!")
                window.location.href = "/index";
            } else {
                alert(response)
            }
        }
    })

})

document.getElementById('file_download').addEventListener("click", function () {
    var fileId = document.getElementById('file_id').value;
    var matches = fileId.match(/\d+/g);
    var id = matches.map(function(match) {
        return parseInt(match, 10);
    });
    window.location.href = '/download/' + id[0];
    
})