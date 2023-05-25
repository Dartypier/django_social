// listener on page load
document.addEventListener("DOMContentLoaded", function () {
    update_likes_color();
});

// persist red color on reload fo each user that liked a post
function update_likes_color() {
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(likeButton => {
        const isLiked = likeButton.classList.contains('liked');
        if (isLiked) {
            likeButton.style.color = "red";
        }
    });
}

function handleLike(postId) {
    const likeButton = document.getElementById(`like-button-${postId}`);
    const likeCount = document.getElementById(`like-count-${postId}`);
    const url = `/like/${postId}/`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeButton.style.color = "red";
            } else {
                likeButton.style.removeProperty("color");
            }

            likeCount.innerText = data.count;
        })
}