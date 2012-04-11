$ ->
    $('textarea.tinymce').tinymce({
        # Location of TinyMCE script
        script_url : STATIC_URL + 'js/tiny_mce/tiny_mce.js',

        # General options
        theme : "advanced",
        #plugins : "autolink,lists,pagebreak,save,print,contextmenu,paste,template",

        # Theme options
        theme_advanced_buttons1: "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,cut,copy,paste,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,print",
        theme_advanced_buttons2: "",
        theme_advanced_buttons3: "",
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: "bottom",
        theme_advanced_resizing: true,
    })

