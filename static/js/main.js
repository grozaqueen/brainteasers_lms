function getCookie(name) {
  const cookies = document.cookie.split(';').map(cookie => cookie.trim());
  const targetCookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
  return targetCookie ? decodeURIComponent(targetCookie.substring(name.length + 1)) : null;
}


// Кнопки удаления комментария
const deleteCommentButtons = document.querySelectorAll('.delete-comment');
deleteCommentButtons.forEach((button) => {
  button.addEventListener('click', (e) => {
    const commentId = button.dataset.commentId;
    const bodyReq = new FormData();
    bodyReq.append('comment_id', commentId);
    const request = new Request('/delete-comment/' + commentId, {
      method: 'DELETE',
      body: bodyReq,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    });

    fetch(request)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          location.reload();
        } else {
          alert('Ошибка удаления комментария!');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  });
});

// Кнопки редактирования комментария
const updateCommentButtons = document.querySelectorAll('.update-comment');
updateCommentButtons.forEach((button) => {
  button.addEventListener('click', (e) => {
    const commentId = button.dataset.commentId;
    const commentText = document.getElementById(`comment-text-${commentId}`);
    const editText = document.getElementById(`edit-text-${commentId}`);
    const changeButton = document.getElementById(`change-comment-${commentId}`);

    // Показать текстовое поле и кнопку изменения, скрыть оригинальный текст комментария
    editText.style.display = 'block';
    changeButton.style.display = 'block';
    commentText.style.display = 'none';

    // Установить значение текстового поля равным оригинальному тексту комментария
    editText.value = commentText.textContent;
  });
});

// Кнопки изменения комментария
const changeCommentButtons = document.querySelectorAll('[id^="change-comment-"]');
changeCommentButtons.forEach((button) => {
  button.addEventListener('click', (e) => {
    const commentId = button.id.replace('change-comment-', '');
    const editText = document.getElementById(`edit-text-${commentId}`);
    const newText = editText.value;

    // Отправить запрос PUT для обновления текста комментария
    fetch(`/update-comment/${commentId}`, {
      method: 'PUT',
      body: JSON.stringify({ text: newText }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then(response => response.json())
      .then(data => {
        // Обновить оригинальный текст комментария новым текстом
        const commentText = document.getElementById(`comment-text-${commentId}`);
        commentText.textContent = newText;
        editText.style.display = 'none';
        button.style.display = 'none';
        commentText.style.display = 'block';
      })
      .catch(error => console.error(error));
  });
});
