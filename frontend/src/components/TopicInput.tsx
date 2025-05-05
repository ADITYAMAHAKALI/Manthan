import { useState } from "react";
import { Button } from "./ui/button";
import { generateSession } from "../lib/api";

interface Props {
  onSessionStart: (sessionId: string, topic: string) => void;
}

export function TopicInput({ onSessionStart }: Props) {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleStart() {
    setLoading(true);
    setError(null);

    try {
      const { session_id, topic: confirmedTopic } = await generateSession(topic);
      onSessionStart(session_id, confirmedTopic);
      setTopic("");
    } catch (err:unknown) {
        console.error(err)
      setError("Failed to start session. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <input
          type="text"
          className="border px-3 py-2 rounded w-full"
          placeholder="Enter a debate topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <Button onClick={handleStart} disabled={loading || topic.length < 3}>
          {loading ? "Starting..." : "Start Debate"}
        </Button>
      </div>
      {error && <p className="text-red-600 text-sm">{error}</p>}
    </div>
  );
}
