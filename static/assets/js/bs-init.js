$(document).ready(function(){

	$('[data-bss-dynamic-product]').each(function(index, elem) {
		var param = $(elem).data('bss-dynamic-product-param');
		$(elem).data('reflow-product', new URL(location.href).searchParams.get(param));
	});

});