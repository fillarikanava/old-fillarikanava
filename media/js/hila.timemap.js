/*global Hila */

Hila.timemap = {
	/**
	 * See http://code.google.com/p/timemap/source/browse/trunk/timemap.js:1135
	 */
	openIssueWindowFn: function (template) {
		return function() {
			this.opts._MODIFIERS = Hila.jst.jstCustomModifiers;
			this.map.openInfoWindowHtml(this.getInfoPoint(),
					template.process(this.opts), {maxWidth: 350});
			this.selected = true;
		};
	}
};
