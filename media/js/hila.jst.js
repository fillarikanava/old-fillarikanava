/*global Hila */

Hila.jst = {
	jstCustomModifiers: {
		br: function(str) {
			return str.replace(/\n/g, '<br>');
		},
		wrap: function(str, len) {
			if (str.length < len) { return str; }
			return str.substr(0, str.lastIndexOf(' ', len)) + "...";
		},
		slice: function(arr, from, to) {
			if (to === undefined) { from = 0; to = from; }
			return arr.slice(from, to);
		}
	}
};

//$('.dyn-href').live('mouseover', function() {
//	ids = this.id.split('-');
//	this.href = this.href.replace(ids[0], ids[1]);
//});
