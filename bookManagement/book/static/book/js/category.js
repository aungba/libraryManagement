$(document).ready(function () {
    $.ajax({
        url: 'category',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            data.categoryList.forEach(category => {
                rows += '<tr><td>' +category.id+ '</td><td>' +category.category_text+ '</td>' +
                '<td><a href="edit/' + category.id + '" id="category_edit" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Edit</a></td></tr>';

                
            });
            $('#c_table tbody').append(rows)
        }
    })
});