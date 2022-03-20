function openEditModal(categoryId, categoryName) {
    document.getElementById('categoryName').setAttribute('value', categoryName);
    document.getElementById('editCategoryForm').setAttribute('action', `/categories/edit/${categoryId}`);

    $('#editCategoryModal').modal();
}