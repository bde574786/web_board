document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search_button');
    const dropdown = document.getElementById('dropdown_content');
    const parentDiv = document.querySelector('.board_list');
    const childDivs = parentDiv.querySelectorAll('.board_list > div:not(.top)');
    
    searchButton.addEventListener('click', function () {
        const selectedOption = dropdown.value;
        const userInput = document.getElementById('search_input').value;

        let data = {};
        switch (selectedOption) {
            case '전체(제목 + 내용)':
                data = { 'option': 'all' };
                break;
            case '제목':
                data = { 'option': 'title' };
                break;
            case '내용':
                data = { 'option': 'content' };
                break;
            default:
                alert("올바르지 않은 옵션 !");
                return;
        }
        data['userInput'] = userInput;

        $.ajax({
            type: "GET",
            url: "/search?" + $.param(data),
            contentType: "application/json",
            success: function (response) {
                const dataList = response.toString().split(",");

                parentDiv.style.display = 'none';

                for (let i = 0; i < childDivs.length; i++) {
                    const currentId = childDivs[i].querySelector('.num').innerText.trim();
                    const shouldDisplay = dataList.includes(currentId);
                    childDivs[i].style.display = shouldDisplay ? 'block' : 'none';
                }

                parentDiv.style.display = 'block';
            }
        });
    });

    document.getElementById('search_input').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            searchButton.click();
        }
    });

    document.getElementById('more_button').addEventListener('click', function () {
        var userBox = document.getElementById('user_box');

        if (userBox.style.display == 'none') {
            userBox.style.display = 'block';
        } else {
            userBox.style.display = 'none';
        }

    })

});
