<script>
	import { io } from 'socket.io-client';
	import { onMount } from 'svelte';

	import { ENDPOINT } from '$lib/constants';
	import { stringify } from 'postcss';

	let socket;
	let touchData = {
		start: {
			x: null,
			y: null
		},
		end: {
			x: null,
			y: null
		}
	};
	let sensorData = {
		absolute: null,
		alpha: null,
		beta: null,
		gamma: null
	};

	let logs = '';

	let mainElement;

	const sendData = () => {
		if (socket) {
			socket.emit('data-event', {
				type: 'touch',
				data: {
					...touchData
				}
			});
		}
	};

	const handleOrientation = (e) => {
		logs += JSON.stringify(e);
		sensorData.absolute = e.absolute;
		sensorData.alpha = e.alpha;
		sensorData.beta = e.beta;
		sensorData.gamma = e.gamma;

		socket.emit('event', {
			type: 'sensor',
			data: {
				...sensorData
			}
		});
	};

	const activateSensor = () => {
		alert('activateSensor');

		socket.emit('data-event', {
			type: 'sensor',
			data: 'hello'
		});
		// DeviceMotionEvent.requestPermission()
		// 	.then((response) => {
		// 		if (response == 'granted') {
		// 			window.addEventListener('deviceorientation', handleOrientation);
		// 		}
		// 	})
		// 	.catch(alert);
	};

	onMount(() => {
		console.log('mounted');
		socket = io(ENDPOINT, { path: '/ws/socket.io' });
		socket.on('connect', () => {
			console.log('connected');
		});

		mainElement.addEventListener('touchstart', (e) => {
			// console.log(e.touches[0]);
			touchData.start.x = e.touches[0].clientX;
			touchData.start.y = e.touches[0].clientY;

			// touchData.start = e.;
		});

		mainElement.addEventListener('touchmove', (e) => {
			// console.log(e.touches[0]);
			touchData.end.x = e.touches[0].clientX;
			touchData.end.y = e.touches[0].clientY;

			// touchData.start = e.;
		});

		mainElement.addEventListener('touchend', (e) => {
			// console.log('send data');
			// alert('sentdata');

			sendData();
		});
	});
</script>

<div class="min-h-screen w-screen hover:bg-gray-100 touch-none" bind:this={mainElement}>
	<button on:click={activateSensor}> Activate Sensor </button>

	<div>
		<div>
			{JSON.stringify(touchData)}
		</div>
		<div>
			{sensorData.alpha}
		</div>
		<div>
			{sensorData.beta}
		</div>
		<div>
			{sensorData.gamma}
		</div>
	</div>

	<div>
		{logs}
	</div>
</div>
