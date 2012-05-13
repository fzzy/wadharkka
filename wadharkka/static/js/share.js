(function() {
	$(document).ready(function() {
		$('#conemails').EnableMultiField(
			{
				enableRemove: false,
				data: initial_conemails,
			}
		);
	});
}).call(this);
