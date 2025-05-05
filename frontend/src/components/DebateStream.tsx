import { useState } from "react";
import { streamArgument } from "../lib/api";

interface Props {
  sessionId: string;
  role: "in-favor" | "against";
}

export function DebateStream({ sessionId, role }: Props) {
  const [streamedText, setStreamedText] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleStream() {
    setStreamedText("");
    setLoading(true);
    await streamArgument(sessionId, role, (text) =>
      setStreamedText((prev) => prev + text)
    );
    setLoading(false);
  }

  return (
    <div className="space-y-3">
      <button
        onClick={handleStream}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Streaming..." : `Speak as ${role}`}
      </button>
      <pre className="p-3 bg-gray-100 rounded whitespace-pre-wrap">{streamedText}</pre>
    </div>
  );
}
