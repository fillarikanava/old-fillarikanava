/*global $ */

$.fn.extend({
	values: function() {
		var data = {};
		this.not(':radio:not(:checked), :checkbox:not(:checked)').each(function() {
			var value = $(this).val();
			if (value.length > 0) { data[this.name] = value; }
		});
		return data;
	},

	jsonsubmit: function(opts) {
		opts = $.extend({
			url: this.get(0).action,
			type: this.get(0).method,
			dataType: 'json',
			data: $(':input', this).values()
		}, opts);
		$.ajax(opts);
	}
});
