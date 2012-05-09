(function() {
	$(function() {
		return $('#tinymceEditor').tinymce({
			script_url: STATIC_URL + 'js/tiny_mce/tiny_mce.js',
			theme: "advanced",
			theme_advanced_buttons1: "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,cut,copy,paste,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,print",
			theme_advanced_buttons2: "",
			theme_advanced_buttons3: "",
			theme_advanced_toolbar_location: "top",
			theme_advanced_toolbar_align: "left",
			theme_advanced_statusbar_location: "bottom",
		});
	});
}).call(this);
