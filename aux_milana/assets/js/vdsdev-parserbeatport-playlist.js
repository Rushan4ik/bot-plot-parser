( function( blocks, element ) {
// (function(blocks,editor,i18n,element){

	// jQuery(window).load(function(){
	// 	jQuery("input.vdsdev-btprtprs-select-playlist").change(function(){
	// 		alert("test");
	// 	});
	// });

	const el = element.createElement;
	// var el=element.createElement,__=i18n.__,RichText=editor.RichText;
	const { registerBlockType } = blocks;

	// const RichText = editor.RichText;

	var vdsdev_prsbtprt_playlists;
	// const registerBlockType = blocks.registerBlockType; // the same

	jQuery.ajax({
		url: ajaxurl,
		type: "POST",
		dataType : "json",
		contentType: "application/x-www-form-urlencoded; charset=UTF-8",
		data: {
			action: "vdsdev-parsebeatport_update-data-parse"
		},
		success: function(playlists) {

			registerBlockType( 'vdsdev-parse-beatport/vdsdev-parserbeatport-playlist', {
		    title: 'Парсер beatport',
		    icon: 'playlist-audio',
		    category: 'embed',
		    keywords: [ 'парсер', 'плейлист', 'beatport' ],
		    attributes: {
		      playlist:
					{
						type: 'string',
						// source: 'attribute',
						selector: 'select.vdsdev-btprtprs-select-playlist',
						attribute: 'value'
					}
		    },
		    edit: function( props ) {
					var slct_pllsts = new Array();
					slct_pllsts.push( el( 'option', { value: "" }, "Не выбран") );
					for(key in playlists)
					{
						slct_pllsts.push( el( 'option', { value: key }, key) );
					}

					function changePlaylist(){
						//jQuery("input.vdsdev-btprtprs-input-playlist").val(jQuery("select.vdsdev-btprtprs-select-playlist").val());
						props.setAttributes({playlist: jQuery("select.vdsdev-btprtprs-select-playlist").val()});
					};

					var outputselect = el( 'select', {onChange:changePlaylist, className:"vdsdev-btprtprs-select-playlist", value: props.attributes.playlist}, slct_pllsts);

					var outputhtml = (
		        el( 'div', { className: props.className },
					  	//el( 'input', { 'type': 'text', className: "vdsdev-btprtprs-input-playlist", value: props.attributes.playlist } ),
							outputselect
						)
	        );

		      return outputhtml;
		    },
		    save: function( props ){
		      return (
		        el( 'div', { className: props.className, playlist: props.attributes.playlist })
		      );
		    }
		  });

		}
	});

} )(
	window.wp.blocks, // wp.blocks becomes just "block" variable
	window.wp.element
	// window.wp.blocks,window.wp.editor,window.wp.i18n,window.wp.element
);
