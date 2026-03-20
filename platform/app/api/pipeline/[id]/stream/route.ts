type Params = { params: { id: string } };

export async function GET(_: Request, { params }: Params) {
	const encoder = new TextEncoder();

	const stream = new ReadableStream({
		start(controller) {
			const events = [
				{ stage: "pm", status: "complete" },
				{ stage: "architect", status: "complete" },
				{ stage: "build", status: "running" },
				{ stage: "hitl", status: "pending" },
			];

			controller.enqueue(
				encoder.encode(
					`event: metadata\ndata: ${JSON.stringify({ projectId: params.id })}\n\n`,
				),
			);

			events.forEach((event, index) => {
				setTimeout(() => {
					controller.enqueue(
						encoder.encode(`event: status\ndata: ${JSON.stringify(event)}\n\n`),
					);
					if (index === events.length - 1) {
						controller.close();
					}
				}, index * 150);
			});
		},
	});

	return new Response(stream, {
		headers: {
			"Content-Type": "text/event-stream",
			"Cache-Control": "no-cache, no-transform",
			Connection: "keep-alive",
		},
	});
}
