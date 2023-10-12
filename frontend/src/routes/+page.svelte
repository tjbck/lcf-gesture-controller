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

	let angle = 0;
	let heatTime = 200;

	let mainElement;

	$: if (socket) {
		socket.emit('data-event', {
			type: 'heat',
			data: heatTime
		});
	}

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

	const getAngle = (x1, y1, x2, y2) => {
		return Math.round(((Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI + 360) % 360);
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

			angle = getAngle(touchData.start.x, touchData.start.y, touchData.end.x, touchData.end.y);

			sendData();
		});
	});
</script>

<div class="min-h-screen w-screen touch-none flex flex-col justify-center">
	<div />

	<div class=" w-full h-full flex-1 flex hover:bg-gray-100" bind:this={mainElement}>
		<div class="m-auto">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				style="transform: rotate({angle - 270}deg);"
				viewBox="0 0 24 24"
				fill="currentColor"
				class=" w-20 h-20"
			>
				<path
					fill-rule="evenodd"
					d="M11.47 2.47a.75.75 0 011.06 0l3.75 3.75a.75.75 0 01-1.06 1.06l-2.47-2.47V21a.75.75 0 01-1.5 0V4.81L8.78 7.28a.75.75 0 01-1.06-1.06l3.75-3.75z"
					clip-rule="evenodd"
				/>
			</svg>

			<div class=" text-center font-semibold text-lg">
				{angle}deg
			</div>
		</div>
	</div>

	<div class=" m-3 text-center font-medium">
		<div class=" text-sm text-left font-medium mb-1">Heat Time</div>
		<div class="flex">
			<button
				class=" bg-gray-300 rounded-l p-3 px-10"
				on:click={() => {
					heatTime = Math.max(0, heatTime - 50);
				}}
			>
				-
			</button>
			<input
				class="w-full text-center outline-none bg-gray-300"
				type="number"
				min="0"
				max="500"
				disabled
				bind:value={heatTime}
			/>
			<button
				class=" bg-gray-300 rounded-r p-3 px-10"
				on:click={() => {
					heatTime = Math.min(500, heatTime + 50);
				}}
			>
				+
			</button>
		</div>
	</div>
</div>
