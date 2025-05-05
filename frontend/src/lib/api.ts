const BASE_URL = "http://localhost:8000"; // adjust for prod

export interface SessionResponse {
  session_id: string;
  topic: string;
}

export interface GeneratedArgument {
  session_id: string;
  role: "in-favor" | "against";
  response: string;
}

/**
 * Create a new debate session with the given topic.
 */
export async function generateSession(topic: string): Promise<SessionResponse> {
  const res = await fetch(`${BASE_URL}/api/debate/generate_session`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic }),
  });

  if (!res.ok) throw new Error("Failed to generate session");

  return res.json();
}

/**
 * Stream an argument from the server for a given session ID and role.
 */
export async function streamArgument(
  sessionId: string,
  role: "in-favor" | "against",
  onData: (text: string) => void
): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/debate/stream?session_id=${sessionId}&role=${role}`);
  if (!res.ok || !res.body) {
    throw new Error("Streaming failed");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const text = decoder.decode(value, { stream: true });
    onData(text);
  }
}
