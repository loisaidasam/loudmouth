
function default_ready() {
	$(".email_td").click(function () {
		$("#" + $(this).attr('id') + "_brief").toggle();
		$("#" + $(this).attr('id') + "_summary").toggle();
	});
}