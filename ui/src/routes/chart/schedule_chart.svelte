<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';
	import ChartDataLabels from "chartjs-plugin-dragdata";
	import { Chart as ChartJS, registerables } from 'chart.js';
	import TailwindColors from '$lib/color_utils';
	import { TimeInterval } from '$lib/time_intervals';

	ChartJS.register(...registerables, ChartDataLabels);
	let ctx: any;
	let power_setpoints = Array(24).fill(0);
	let chart: any;
	let labels: string[];
	let propagate_drag_forward_flag = true;
	
	export let step_size = 5;
	export let propagate_drag_forward = true;
	export let smart_propagation = true;
	export let intervals:TimeInterval = TimeInterval.FIFTEEN_MINUTES;

	function hourly_labels() {
		const labels = [];
        for (let i = 0; i < 24; i++) {
            labels.push(i.toString().padStart(2, '0') + ':00');
        }
        return labels;
	}

    function five_minute_labels() {
        const labels = [];
        for (let i = 0; i < 24 * 12; i++) {
            const hours = Math.floor(i * 5 / 60).toString().padStart(2, '0');
            const minutes = (i * 5 % 60).toString().padStart(2, '0');
            labels.push(`${hours}:${minutes}`);
        }
        return labels;
    }

    function fifteen_minute_labels() {
        const labels = [];
        for (let i = 0; i < 24 * 4; i++) {
            const hours = Math.floor(i * 15 / 60).toString().padStart(2, '0');
            const minutes = (i * 15 % 60).toString().padStart(2, '0');
            labels.push(`${hours}:${minutes}`);
        }
        return labels;
    }

	function get_labels(inv: TimeInterval) {
		switch (inv) {
			case TimeInterval.FIVE_MINUTES:
				return five_minute_labels();
			case TimeInterval.FIFTEEN_MINUTES:
				return fifteen_minute_labels();
			default:
				return hourly_labels();
		}
	}

	$: labels = get_labels(intervals);
	$: power_setpoints = Array(labels.length).fill(0);
	$: create_chart(intervals);

	function create_chart(interval: TimeInterval) {
		if (chart) chart.destroy();
		if (!ctx) return;
		chart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: labels,
				datasets: [
					{
						data: power_setpoints,
						backgroundColor: TailwindColors['amber-700'],
						borderColor: TailwindColors['amber-700'],
						borderWidth: 1,
						pointHoverRadius: 10,
						pointRadius: 4,
						stepped: true,
						pointHoverBackgroundColor: TailwindColors['amber-700'], 
						pointHoverBorderColor: TailwindColors['amber-700'],
					}
				]
			},
			options: {
				interaction: {
					intersect: true
				},
				scales: {
					x: {
						title: {
							display: true,
							text: 'Local Time',
							color: TailwindColors['white']
						},
						ticks: {
							color: TailwindColors['white'],
						},
						grid: {
							color: TailwindColors['gray-800'],
						}
					},
                    y: {
						title: {
							display: true,
							text: 'Power Setpoint (kW)',
							color: TailwindColors['white']
						},
						ticks: {
							color: TailwindColors['white'],
						},
						grid: {
							color: TailwindColors['gray-800'],
						},
                        min: -100,
                        max: 100
                    }
                },
				plugins: {
					dragData: {
						showTooltip: true,
						snap: false,
						round: 0,
						magnet: {
							to: (value: number) => Math.round(value / step_size) * step_size,
						},
						onDragStart: (event: any, element: any, index: any, value: any) => {
							console.log(propagate_drag_forward, smart_propagation)
							if (!propagate_drag_forward) {
								propagate_drag_forward_flag = false;
								return;
							}
							if (!smart_propagation) {
								propagate_drag_forward_flag = true;
								return;
							}
							for (let i = index + 1; i < power_setpoints.length; i++) {
								if (power_setpoints[index] != power_setpoints[i]) {
									propagate_drag_forward_flag = false;
									return;
								}
							}
							propagate_drag_forward_flag = true;
						},
                        onDrag: (event: any, datasetIndex: any, index: any, value: any) => {
							if (!propagate_drag_forward_flag) return;
                            for (let i = index; i < power_setpoints.length; i++) {
                                power_setpoints[i] = value;
                            }
                        },
                        onDragEnd: (event: any, datasetIndex: any, index: any, value: any) => {
							if (!propagate_drag_forward_flag) {
								return;
							}
                            for (let i = index; i < power_setpoints.length; i++) {
                                power_setpoints[i] = value
                            }
							chart.update();
                        },
					},
					tooltip: {
						displayColors: false,
						callbacks: {
                            label: (context) => context.raw + ' kW',
                        }
					},
					legend: {
						display: false
					},
				}
			}
		});
	}

	onMount(() => create_chart(intervals));
</script>

<canvas bind:this={ctx}></canvas>