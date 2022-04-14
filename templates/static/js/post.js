function openEditModal(categoryId, categoryName) {
    document.getElementById('categoryName').setAttribute('value', categoryName);
    document.getElementById('editCategoryForm').setAttribute('action', `/categories/edit/${categoryId}`);

    $('#editCategoryModal').modal();
}

function openRemoveModal(categoryId, categoryName) {
    document.getElementById('confirmRemoveButton').setAttribute('href', `/categories/remove/${categoryId}`);
    document.getElementById('removeText').innerText = `You really want to remove the ${categoryName} category.`;

    $('#removeCategoryModal').modal();
}

function openRemoveCommentModal(commentId, commentAuthorUsername) {
    document.getElementById('confirmRemoveButton').setAttribute('href', `/posts/comments/${commentId}`);
    document.getElementById('removeText').innerText = (`
        Do you really want to remove the comment made by ${commentAuthorUsername}?
    `);

    $('#removeCommentModal').modal();
}