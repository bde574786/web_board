document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search_button');
    const dropdown = document.getElementById('dropdown_content');

    searchButton.addEventListener('click', function () {
        const selectedOption = dropdown.value;
        var data = {}
        var userInput = document.getElementById('search_input').value;

        switch (selectedOption) {
            case '전체(제목 + 내용)':
                data = { 'option': 'all' }
                break;
            case '제목':
                data = { 'option': 'title' }
                break;
            case '내용':
                data = { 'option': 'content' }
                break;
            default:
                alert("올바르지 않은 옵션 !")
        }

        data['userInput'] = userInput;

        $.ajax({
            type: "POST",
            url: "/search",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (response) {

            }
        })

    });
});