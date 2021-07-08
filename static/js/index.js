(function ($) {
	$.extend({
		tipsBox: function (options) {

			options = $.extend({
				obj: null,  //jq object
				str: "+1",  //content or html
				startSize: "12px",  //start font size
				endSize: "30px",    //end font size
				interval: 600,  //time gap
				color: "red",    //color
				callback: function () { }    //callback function
			}, options);

			$("body").append("<span class='num'>" + options.str + "</span>");

			var box = $(".num");
			var left = options.obj.offset().left + options.obj.width() / 2;
			var top = options.obj.offset().top - options.obj.height();

			box.css({
				"position": "absolute",
				"left": left + "px",
				"top": top + "px",
				"z-index": 9999,
				"font-size": options.startSize,
				"line-height": options.endSize,
				"color": options.color
			});

			box.animate({
				"font-size": options.endSize,
				"opacity": "0",
				"top": top - parseInt(options.endSize) + "px"
			}, options.interval, function () {
				box.remove();
				options.callback();
			});
		}
	});
})(jQuery);


jQuery.cookie = function(name, value, options) {
	if (typeof value != 'undefined') { // name and value given, set cookie
		options = options || {};
		if (value === null) {
			value = '';
			options = $.extend({}, options); // clone object since it's unexpected behavior if the expired property were changed
			options.expires = -1;
		}
		var expires = '';
		if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
			var date;
			if (typeof options.expires == 'number') {
				date = new Date();
				date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
			} else {
				date = options.expires;
			}
			expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
		}
		// NOTE Needed to parenthesize options.path and options.domain
		// in the following expressions, otherwise they evaluate to undefined
		// in the packed version for some reason...
		var path = options.path ? '; path=' + (options.path) : '';
		var domain = options.domain ? '; domain=' + (options.domain) : '';
		var secure = options.secure ? '; secure' : '';
		document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
	} else { // only name given, get cookie
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};


function GetCookie(name) {
	return $.cookie(name);
};

function SetCookie(name, data) {
	$.cookie(name, data, {
		expires: 100
	});
	$.cookie(name, data, {
		path: "/"
	});
};

var i = 1;
var json = {};
$('#total').text(imgArray.length)
$('#totallink').text(num);
function propsVal() {
	var m = 0;
	for (let key in json){
		if (key == i) {
			$('#icon').show();
		}
		m++;
	}
	$('#currlink').text(m);
	$('#propsVal').css('width', (m / num) * 100 +'%');
}

function initdom() {
	$('#check').text(i);
	var currdom = imgArray[i-1];
	var html = '<a href="'+currdom.url+'?id='+currdom.id+'"><img src="images/'+currdom.name+'"/></a>'
	$('.main').html(html);
	var str = currdom.name.lastIndexOf('.');
	$('#imgName').text(currdom.name.substr(0, str));
}

$('#link').on('click', function(){
	$.tipsBox({
		obj: $(this),
		str: "+1",
		callback: function () {
		}
	});
	json[i] = true;
	$('#icon').show();
	// imgArray[i].collect = true;
	// json[i] = imgArray[i];
	propsVal();
})
propsVal();

$('#next').on('click', function(){
	$('#icon').hide();
	var link = 0;
	var arr = [];
    for (let key in json){
    	link++;
    	arr.push(key);
    }
    if (link == num) {
		alert("Please wait fot 20 sec and don't do anything");
		alert("The anime you have selected are " + arr.join(','));
    	eel.dataToPy(arr)
		eel.expose(dataToJs);
    	function dataToJs(ani) {
			var ani_name = new Array(5);
			var url_name = new Array(5);
			var content = new Array(5);
			var type = new Array(5);
			var episodes = new Array(5);
			var score = new Array(5);
			var start_date = new Array(5);
			var end_date = new Array(5);
			var rated = new Array(5);
			var members = new Array(5);


			var i = 0;
			for (var t = 0; t < 5; t++) {
				SetCookie("ani_name" + t ,ani[i]);
				SetCookie("url_name" + t, ani[i + 1]);
				SetCookie("content" + t ,ani[i + 2]);
				SetCookie("type" + t ,ani[i + 3]);
				SetCookie("episodes" + t ,ani[i + 4]);
				SetCookie("score" + t ,ani[i + 5]);
				SetCookie("start_date" + t ,ani[i + 6]);
				SetCookie("end_date" + t ,ani[i + 7]);
				SetCookie("rated" + t ,ani[i + 8]);
				SetCookie("members" + t ,ani[i + 9]);
				i += 10;
			}
			window.location.href = "result.html";
		}
		dataToJs();
    }else if (i == imgArray.length && link != num) {
    	i = 1;
		// 	json = {};
		alert('The number of anime you need to select is'+num+', now you have select '+link+' anime, please add more')
		propsVal();
		// $('#check').text(i);
		initdom();
    }else {
    	i++;
		$('#check').text(i);
		propsVal();
		initdom();
      	// $('#img').attr('src', 'images/' +imgArray[(i-1)].name)
    }
})

initdom();



