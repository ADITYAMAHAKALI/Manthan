import { useState } from "react";
import { TopicInput } from "./components/TopicInput";
import { RoleSelector } from "./components/RoleSelector";
import { DebateStream } from "./components/DebateStream";

function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [role, setRole] = useState<"in-favor" | "against" | null>(null);

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4 space-y-6">
      <h1 className="text-2xl font-bold">Gemini Debate Simulator</h1>

      <TopicInput
        onSessionStart={(id, topic) => {
          setSessionId(id);
          setTopic(topic);
          setRole(null);
        }}
      />

      {sessionId && (
        <>
          <div className="text-gray-600">Session: <code>{sessionId}</code></div>
          <div className="text-lg font-medium">Topic: {topic}</div>

          <RoleSelector onSelect={(r) => setRole(r)} />

          {role && <DebateStream sessionId={sessionId} role={role} />}
        </>
      )}
    </div>
  );
}

export default App;
