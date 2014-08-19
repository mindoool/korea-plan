var last=false;
var running =false;

$(document).ready(function(){
	var offset = 5;
	$.ajax({
		url: '/newsfeed_ajax',
		type:'POST',
		success:function(response){
			$('#newsfeed_right').append(response);
			console.log('success');
		},
		error: function(){
			console.log('error');
		},
		complete:function(){
			console.log('complete');
		}
	});
	
	$(window).scroll(function(){
		if($(window).scrollTop() == $(document).height() - $(window).height() && (! last) && (! running)) {
			running = true;
			$.ajax({
				url:'/newsfeed_ajax',
				type: 'POST',
				data:{"number": offset},
				success:function(response){
					if (response.trim()==''){
						last = true;
					}
					else {
					$('#newsfeed_right').append(response);
					console.log('success');
					offset +=5;
					}

				},
				error:function(){
					console.log('error');
				},
				complete:function(){
					console.log('complete');
					running = false;
				}

			});
		}
	});

});

