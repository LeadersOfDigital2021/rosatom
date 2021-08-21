
var $textArea = $(".textarea-container");

// Re-size to fit initial content.
resizeTextArea($textArea);

// Remove this binding if you don't want to re-size on typing.
$textArea.off("keyup.textarea").on("keyup.textarea", function() {
    resizeTextArea($(this));
});

function resizeTextArea($element) {
    $element.height($element[0].scrollHeight);
}