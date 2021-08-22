$(document).ready(function () {
    $('.protocol_item').on('click', function () {
        $('.protocol_item').removeClass('protocol_selected');
        $(this).toggleClass('protocol_selected');

        $('.info_block_message').addClass('d-none');
        id = $(this).attr('data-id')

        //Прописываем ссылки
        $('a#view').attr('href', '/meeting_detail/' + id);
        $('a#print').attr('href', '/meeting_print/' + id);
        $('a#sendProtocolLink').attr('href', '/meeting_send/' + id);
        $('#sendEmailMeeting_id').attr('value', id);
        $('.info_block_message#info_' + id).removeClass('d-none');
        $('#control-protocol').removeClass('d-none');
        $('#pick_protocol').addClass('d-none');
    });
});


function fullScreenProtocol() {
    event.preventDefault();
    if ($('#protocol-body').hasClass('full-screen')) {
        $("#protocol-body").addClass('col-md-12').addClass('half-screen').removeClass('col-md-5').removeClass('full-screen');
    } else {
        $("#protocol-body").addClass('col-md-5').addClass('full-screen').removeClass('col-md-12').removeClass('half-screen');
    }
}

function editElm(id) {
    event.preventDefault();
    $(id).toggleClass('edit-now');
    if ($(id).attr('disabled')) {
        $(id).removeAttr('disabled');
    } else {
        $(id).attr('disabled', '');
    }
}


