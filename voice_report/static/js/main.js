$( document ).ready(function() {


    $('.protocol_item').on('click', function() {
        $('.protocol_item').removeClass('protocol_selected');
        $(this).toggleClass('protocol_selected');

        $('.info_block_message').addClass('d-none');
        id = $(this).attr('data-id')
        
        //Прописываем ссылки
        $('a#view').attr('href', '/view?meeting_id='+id);
        $('a#print').attr('href', '/print?meeting_id='+id);
        $('a#sendProtocolLink').attr('href', '/send?meeting_id='+id);
        $('#sendEmailMeeting_id').attr('value', id);
       
        console.log(id);
        $('.info_block_message#info_'+id).removeClass('d-none');
        $('#control-protocol').removeClass('d-none');
        $('#pick_protocol').addClass('d-none');

    });
/*Временный функционал для демонстрации */
    $('#protocol_2').on('click', function() {
        $('#info_1').toggleClass('d-none');
        $('#info_2').toggleClass('d-none');

    });
    $('#protocol_1').on('click', function() {
        $('#info_1').toggleClass('d-none');
        $('#info_2').toggleClass('d-none');

    });
  /*Временный функционал для демонстрации  END*/
});





function fullScreenProtocol(){
    event.preventDefault();
    console.log('fullScreen');
    if ($('#protocol-body').hasClass('full-screen')){
        $("#protocol-body").addClass('col-md-12').addClass('half-screen').removeClass('col-md-5').removeClass('full-screen');
    }
    else{
        $("#protocol-body").addClass('col-md-5').addClass('full-screen').removeClass('col-md-12').removeClass('half-screen');
    }
}
function editElm(id){
    event.preventDefault();

    $(id).toggleClass('edit-now');
    if ($(id).attr('disabled')) {
        $(id).removeAttr('disabled');
    } else {
        $(id).attr('disabled','');
    }

    console.log(elm);
}


