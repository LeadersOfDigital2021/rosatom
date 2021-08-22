$(document).ready(function () {
    $('.goTostr').on('click', function () {
        var block_text = $(this).attr('data-name');
        $('a[name=' + block_text + ']').delay(100).fadeOut().fadeIn('slow').fadeOut().fadeIn('slow')

    });
    $('.play-audio-btn').on('click', function () {
        const start_time = $(this).data('start-time')
        const end_time = $(this).data('end-time')

        let player = $("#audio_player")
        console.log(player)
        player[0].play();
    });
});
