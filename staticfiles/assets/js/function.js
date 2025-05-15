const monthNames = ["Jan", "Feb", "Mar", "April", "May",
	"June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

$('#blogCommentForm').submit(function (e) {
	e.preventDefault();

	let dt = new Date();
	let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

	$.ajax({
		data: $(this).serialize(),

		method: $(this).attr('method'),

		url: $(this).attr('action'),

		dataType: 'json',

		success: function (res) {
			console.log('Comment saved to DB!..');

			if (res.bool == true) {
				$('#blogCommentRes').html('Comment Added Successfully!')
				$('.hide-comment').hide()

				let _html = '<div class="card-body">'
				_html += '<div class="d-flex flex-start align-items-center">'
				_html += '<img class="rounded-circle shadow-1-strong mr-3" src="' + res.context.image + '" alt="avatar" width="60" height="60" />'
				_html += '<div>'
				_html += '<h6 class="font-weight-bold mb-1">' + res.context.user + '</h6>'
				_html += '<p class="text-muted small mb-0">' + time + '</p>'
				_html += '</div>'
				_html += '</div>'
				_html += '<p class="mt-3">' + res.context.comment + '</p>'
				_html += '</div>'
				_html += '<hr class="my-0">'

				$('.card').prepend(_html)

			}
		}
	})
})

$(document).on('submit', '#ajax-contact-form', function (e) {
	e.preventDefault()

	let name = $('#name').val()
	let email = $('#email').val()
	let message = $('#message').val()

	$.ajax({
		url: '/ajax-contact-form',
		data: {
			'name': name,
			'email': email,
			'message': message,
		},
		dataType: 'json',
		beforeSend: function () {
			console.log('Sending data to server...')
		},
		success: function (response) {
			console.log('Data send to server successfully.')
			$('#ajax-contact-form')[0].reset();
			$('#ajax-contact-form').hide()
			$('.contact__form__title').html('<h2>Message Sent Successfully!</h2>')
		}
	})
})
