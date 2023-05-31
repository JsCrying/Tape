let user_name = '';


$('#image').change(() => {
	$('#status').html(`<i class="fas fa-check"></i>`);
});

$('#cancel').click(() => {
	$('#image').val(null);
	$('#status').html(`<i class="fa-solid fa-image"></i>`);
});

function showMessage(user_name, message, image, timestamp) { // 接收到服务端传递的信息后，在对话框显示
		let messageHTML = `
			<div class="message">
				<span class="message-sender">${user_name}</span>
				<span class="message-timestamp"> ${timestamp}</span>
		`;
		if (message !== '') {
			messageHTML += `<span class="message-content">${message}</span>`;
		}

		if (image) {
			let blob = new Blob([image]);
			messageHTML += `<span class="message-content"><img src="${URL.createObjectURL(blob)}" class="message-image"></span>`;
		}

		messageHTML += `
			</div>
		`;
		$('#message-list')[0].insertAdjacentHTML('beforeend', messageHTML);
}

function operateMessage() {
	const message = $('#message').val().trim();
	let image = $('#image')[0].files[0];
	// 1、$(“#image”)获取到的是jquery对象，他没有dom对象的方法，比如src，因此需要把对象转化为dom，然后(“#image”)[0].src获取值  
	// 2、修改src属性可以这样，
	// (“#image”)[0].src获取值  
	// 修改src属性可以这样，attr是jquery对象的方法：
	// (“#image”).attr(‘src’,path);
	// attr是jquery对象的方法：

	if (message !== '' || image) {
		const timestamp = new Date().toLocaleString(); // Get the current timestamp

		socket.emit(
					'msg',
					{
						'client_to_server': current_channel,
						'msg': message,
						'img': image,
						'timestamp': timestamp
					}
		);
		$('#message').val('');
		$('#image').val(null); // Reset the image input field
		$('#status').html(`<i class="fa-solid fa-image"></i>`);
	}
}
function sendMessage(e) {
	e.preventDefault();
	operateMessage();
}

$('#message-form').submit((e) => {
	sendMessage(e);
});