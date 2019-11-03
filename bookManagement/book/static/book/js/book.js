$(document).ready(function () {
    //  $('#release_date').flatpickr();
    $("#register").click(function () {
        if (confirm("Are you sure want to register?")) {
            $('#book').submit();
        }
    });

    $('#update').click(function () {
        if (confirm("Are you sure want to update?")) {
            $('#book_update').submit();
        }
    })


    $.ajax({
        url: 'test',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let rows = '';
            data.books.forEach(book => {
                var due_date = book.id + 1;
                rows += '<tr><td>' + book.id + '</td><td>' + book.book_title + '</td><td>' + book.book_author + '</td><td>' + book.book_publisher + '</td><td>' + book.book_release_date + '</td><td>' + book.book_category__category_text + '</td><td>' + book.book_status + '</td>';
                if (!book.book_status) {
                    rows += '<td> Availabe </td><td>' + book.latest_book_loan__due_date + '</td>' +
                        '<td><a href="edit/' + book.id + '" id="edit' + book.id + '"" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Edit</a>' +
                        '<button class="btn btn-info btn-sm" id="delete_book" data-id="' + book.id + '" type="button">Delete</button>' +
                        '<button id="borrow_book" class="btn btn-primary btn-sm" role="button" disabled>Borrow</button>' +
                        '</td></tr>';
                    
                }

                else if (book.status) {
                    rows += '<td> Availabe </td><td>' + book.latest_book_loan__due_date + '</td>' +
                        '<td><a href="edit/' + book.id + '" id="edit' + book.id + '"" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Edit</a>' +
                        '<button class="btn btn-info btn-sm" id="delete_book" data-id="' + book.id + '" type="button">Delete</button>' +
                        '<a href="borrow/' + book.id + '"  id="borrow_book" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Borrow</a>' +
                        '</td></tr>';
                } else {
                    rows += '<td id="' + book.id + '"> On Loan </td><td id="' + due_date + '">' + book.latest_book_loan__due_date + '</td>' +
                        '<td><button id="edit_button" class="btn btn-primary btn-sm" role="button" disabled>Edit</a>' +
                        '<button class="btn btn-danger btn-sm" id="delete_book" data-id="' + book.id + '" type="button" disabled >Delete</button>' +
                        '<button id="return_book" data-id="' + book.id + '" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Return</button>' +
                        '</td></tr>';
                }
            });
            $('#table tbody').append(rows)

            $("#table").DataTable({
                'aoColumnDefs': [{
                    'bSortable': false,
                    'aTargets': [0]
                }]
            });
            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });
            $('#table').on('click', 'button#delete_book', function () {
                if (confirm("Are you sure want to delete?")) {
                    deleteBook(this)
                }
            })

            $('#table tbody').on('click', 'button#return_book', function () {
                if (confirm("Are you sure want to return?")) {
                    returnBook(this)
                   autoRefresh();
                }

            })

        }
    });


    function deleteBook(element) {
        bookId = $(element).data("id")
        $.ajax({
            url: 'delete/' + bookId,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                $(element).parents()[1].remove()
            }
        });
    }

    function returnBook(element) {
        bookId = $(element).data("id")
        var due_date = bookId + 1;
        $.ajax({
            url: 'return/' + bookId,
            type: 'post',
            dataType: 'json',
            success: function (data) {

                $('button#return_book').replaceWith('<a href="borrow/' + bookId + '"  id="borrow_book" class="btn btn-primary btn-sm" role="button" aria-disabled="true">Borrow</a>')
                $('button#del' + bookId).replaceWith('<button class="btn btn-info btn-sm" id="del' + bookId + '" data-id="' + bookId + '" type="button">Delete</button>');
                $('button#del' + bookId).attr("disabled", false);
                $('button#edit'+ bookId).attr("disabled", false);
                $('td#' + bookId).text("Available")
                $('td#' + due_date).text("");
            }
        })
        
        
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $('#search_book').click(function () {
        var col = 1;
        var table = $('#table').DataTable()
        var value = $('#title').val();
        var release_date = $('#release_date').val();



        $.fn.dataTableExt.afnFiltering.push(
            function (settings, data, dataIndex) {
                var title = $('#title').val();
                var author = $('#author').val();
                var publisher = $('#publisher').val();
                var status = $('#release_date').val();
                var title_col = data[1];
                var author_col = data[2];
                var publisher_col = data[3];
                var status_col = data[7];

                if (title_col.includes(title) &&
                    author_col.includes(author) &&
                    publisher_col.includes(publisher) &&
                    status_col.includes(status)) {
                    return true;
                } else if (status.includes(status_col) && author.includes(author_col) && publisher.includes(publisher_col)) { return true; }
                else if (title.includes(title_col) && status.includes(status_col) && publisher.includes(publisher_col)) { return true; }
                else if (title.includes(title_col) && author.includes(author_col) && status.includes(status_col)) { return true; }
                else if (title.includes(title_col) && author.includes(author_col) && publisher.includes(publisher_col)) { return true; }
                else if (title.includes(title_col) && author.includes(author_col)) { return true; }
                else if (title.includes(title_col) && publisher.includes(publisher_col)) { return true; }
                else if (title.includes(title_col) && status.includes(status_col)) { return true; }
                else if (publisher.includes(publisher_col) && author.includes(author_col)) { return true; }
                else if (publisher.includes(publisher_col) && author.includes(author_col)) { return true; }
                else if (publisher.includes(publisher_col) && status.includes(status_col)) { return true; }
                else if (title.includes(title_col)) { return true; }
                else if (author.includes(author_col)) { return true; }
                else if (publisher.includes(publisher_col)) { return true; }
                else if (status.includes(status_col)) { return true; }

            }
        );
        table.draw();
    });



    $('input[type="checkbox"]').click(function () {
        var table = $('#table').DataTable()
        // if($(this).prop("checked") == true){

        $.fn.dataTableExt.afnFiltering.push(
            function (settings, data, dataIndex) {
                var checked = $('#toggle_switch').is(':checked');
                if (checked) {
                    var date = new Date();
                    date.setDate(date.getDate());
                    date_col = data[8];
                    date_column = new Date(date_col);
                    if (date_column < date) {
                        return true
                    }
                } else {
                    return true;
                }
            }
        );
        table.draw();

    });

    $('#borrow').click(function () {
        var userVal = $('#id_Customer').val();
        $.ajax({
            url: '/check/'+userVal,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if(data.count >= 3) {
                    alert('You already borrowed the maximum amount of book')
                } else {
                    $('#book_borrow').submit();
                }
            }
        })
    })
});

function autoRefresh() {
    setTimeout(function() {
        location.reload();
        }, 1000);
}
