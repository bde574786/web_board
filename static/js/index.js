var content = document.getElementById("dropdown_content")
var style = window.getComputedStyle(content);

function toggleImage() {
    var image = document.getElementById("arrow_image")
    
    if (content.style.display === "none") {
        image.src = "../static/images/arrow_up.png"
    } else {
        image.src = "../static/images/arrow_down.png"
    }
}

function showDropdownContent() {
    if (style.display == "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}

function changeDropdownCondition(element) {
    var condition = element.getAttribute("data-value");
    var search_condition = document.getElementById("search_condition");
    
    if (condition === "all") {
        search_condition.textContent = "전체(제목 + 내용)"
    } else if (condition === "title") {
        search_condition.textContent = "제목"
    } else {
        search_condition.textContent = "내용"
    }

    content.style.display = "none"
    toggleImage()
}

document.getElementById("search_button").addEventListener("click", function () {
    alert("검색 버튼 클릭");
});

document.querySelectorAll("#dropdown_content a").forEach(item => {
    item.addEventListener("click", function () {
        changeDropdownCondition(this)
    })
})

document.getElementById('condition_button').addEventListener("click", function() {
    showDropdownContent()
    toggleImage()
});


