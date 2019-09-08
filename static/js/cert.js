function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function setAjaxCSRFToken() {
    var csrftoken = getCookie('csrftoken');
    var sessionid = getCookie('sessionid');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}


function APIUpdateAttr(props) {
    // props = {url: .., body: , success: , error: , method: ,}
    props = props || {};
    var success_message = props.success_message || '更新成功!';
    var fail_message = props.fail_message || '更新时发生未知错误.';
    var flash_message = props.flash_message || true;
    if (props.flash_message === false) {
        flash_message = false;
    }

    $.ajax({
        url: props.url,
        type: props.method || "PATCH",
        data: props.body,
        contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json",
        async: props.async || true
    }).done(function (data, textStatue, jqXHR) {
        if (flash_message) {
            toastr.success(success_message);
        }
        if (typeof props.success === 'function') {
            return props.success(data);
        }
        if (props.async == false) {
            location.reload();
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (flash_message) {
            toastr.error(fail_message);
        }
        if (typeof props.error === 'function') {
            return props.error(jqXHR.responseText);
        }
    });
    // return true;
}

function objectDeletePost(obj, name, url, method, body, redirectTo) {
    function doDelete() {
        // var body={};
        var success = function (data) {
            // swal('Deleted!', "[ "+name+"]"+" has been deleted ", "success");
            window.location.href = redirectTo;
        };
        var fail = function () {
            swal("错误", "删除" + "[ " + name + " ]" + "遇到错误", "error");
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: method,
            success_message: "删除成功",
            success: success,
            error: fail
        });
    }

    swal({
        title: '你确定删除吗 ?',
        text: " [" + name + "] ",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: '取消',
        confirmButtonColor: "#ed5565",
        confirmButtonText: '确认',
    }).then(function (action) {
        if (action.value == true) {
            doDelete()
        }
    });
}


var cert = {};
cert.checked = false;
cert.selected = {};
cert.initDataTable = function (options) {
    // options = {
    //    ele *: $('#dataTable_id'),
    //    ajax_url *: '{% url 'users:user-list-api' %}',
    //    columns *: [{data: ''}, ....],
    //    dom: 'fltip',
    //    i18n_url: '{% static "js/...../en-us.json" %}',
    //    order: [[1, 'asc'], [2, 'asc'], ...],
    //    buttons: ['excel', 'pdf', 'print'],
    //    columnDefs: [{target: 0, createdCell: ()=>{}}, ...],
    //    uc_html: '<a>header button</a>',
    //    op_html: 'div.btn-group?',
    //    paging: true
    // }
    var ele = options.ele || $('.dataTable');
    var columnDefs = [
        {
            targets: 0,
            orderable: false,
            createdCell: function (td, cellData) {
                $(td).html('<input type="checkbox" class="text-center ipt_check" id=99991937>'.replace('99991937', cellData));
            }
        },
        {className: 'text-center', targets: '_all'}
    ];
    columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
    var select = {
        style: 'multi',
        selector: 'td:first-child'
    };
    var table = ele.DataTable({
        pageLength: options.pageLength || 15,
        dom: options.dom || '<"#uc.pull-left">flt<"row m-t"<"col-md-8"<"#op.col-md-6"><"col-md-6 text-center"i>><"col-md-4"p>>',
        order: options.order || [],
        // select: options.select || 'multi',
        buttons: [],
        columnDefs: columnDefs,
        serverSide: true,
        processing: true,
        ajax: {
            url: options.ajax_url,
            data: function (data) {
                delete data.columns;
                if (data.length !== null) {
                    data.limit = data.length;
                    delete data.length;
                }
                if (data.start !== null) {
                    data.offset = data.start;
                    delete data.start;
                }

                if (data.search !== null) {
                    var search_val = data.search.value;
                    var search_list = search_val.split(" ");
                    var search_attr = {};
                    var search_raw = [];

                    search_list.map(function (val, index) {
                        var kv = val.split(":");
                        if (kv.length === 2) {
                            search_attr[kv[0]] = kv[1]
                        } else {
                            search_raw.push(kv)
                        }
                    });
                    data.search = search_raw.join("");
                    $.each(search_attr, function (k, v) {
                        data[k] = v
                    })
                }

                if (data.order !== null && data.order.length === 1) {
                    var col = data.order[0].column;
                    var order = options.columns[col].data;
                    if (data.order[0].dir == "desc") {
                        order = "-" + order;
                    }
                    data.order = order;
                }
            },
            dataFilter: function (data) {
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.count;
                json.recordsFiltered = json.count;
                return JSON.stringify(json); // return JSON string
            },
            dataSrc: "results"
        },
        columns: options.columns || [],
        select: options.select || select,
        language: {
            search: "搜索",
            lengthMenu: "每页  _MENU_",
            info: "显示第 _START_ 至 _END_ 项结果; 总共 _TOTAL_ 项",
            infoFiltered: "",
            infoEmpty: "",
            zeroRecords: "没有匹配项",
            emptyTable: "没有记录",
            paginate: {
                first: "«",
                previous: "‹",
                next: "›",
                last: "»"
            }
        },
        lengthMenu: [[10, 15, 25, 50, 100, 200, 300, 500], [10, 15, 25, 50, 100, 200, 300, 500]]
    });
    table.selected = [];
    table.on('select', function (e, dt, type, indexes) {
        var $node = table[type](indexes).nodes().to$();
        $node.find('input.ipt_check').prop('checked', true);
        cmdb.selected[$node.find('input.ipt_check').prop('id')] = true;
        if (type === 'row') {
            var rows = table.rows(indexes).data();
            $.each(rows, function (id, row) {
                if (row.id) {
                    table.selected.push(row.id)
                }
            })
        }
    }).on('deselect', function (e, dt, type, indexes) {
        var $node = table[type](indexes).nodes().to$();
        $node.find('input.ipt_check').prop('checked', false);
        cmdb.selected[$node.find('input.ipt_check').prop('id')] = false;
        if (type === 'row') {
            var rows = table.rows(indexes).data();
            $.each(rows, function (id, row) {
                if (row.id) {
                    var index = table.selected.indexOf(row.id);
                    if (index > -1) {
                        table.selected.splice(index, 1)
                    }
                }
            })
        }
    }).on('draw', function () {
        $('#op').html(options.op_html || '');
        $('#uc').html(options.uc_html || '');
        var table_data = [];
        $.each(table.rows().data(), function (id, row) {
            if (row.id) {
                table_data.push(row.id)
            }
        });

        $.each(table.selected, function (id, data) {
            var index = table_data.indexOf(data);
            if (index > -1) {
                table.rows(index).select()
            }
        });
    });
    var table_id = table.settings()[0].sTableId;
    $('#' + table_id + ' .ipt_check_all').on('click', function () {
        if ($(this).prop("checked")) {
            $(this).closest('table').find('.ipt_check').prop('checked', true);
            table.rows({search: 'applied', page: 'current'}).select();
        } else {
            $(this).closest('table').find('.ipt_check').prop('checked', false);
            table.rows({search: 'applied', page: 'current'}).deselect();
        }
    });

    // cmdb.table = table;
    return table;
};

// Sweet Alert for Delete
function objectDelete(obj, name, url, redirectTo) {
    function doDelete() {
        var body = {};
        var success = function () {
            // swal('Deleted!', "[ "+name+"]"+" has been deleted ", "success");
            if (!redirectTo) {
                $(obj).parent().parent().remove();
            } else {
                window.location.href = redirectTo;
            }
        };
        var fail = function () {
            swal("错误", "删除" + "[ " + name + " ]" + "遇到错误", "error");
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: "DELETE",
            success_message: "删除成功",
            success: success,
            error: fail
        });
    }

    swal({
        title: '你确定删除吗 ?',
        text: " [" + name + "] ",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: '取消',
        confirmButtonColor: "#ed5565",
        confirmButtonText: '确认',
    }).then(function (action) {
        if (action.value == true) {
            doDelete()
        }
    });
}