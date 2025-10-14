import { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState("unknown");

  useEffect(() => {
    const base = import.meta.env.VITE_API_URL;
    if (!base) return;
    fetch(`${base}/health`)
      .then(r => r.json())
      .then(d => setHealth(d.status))
      .catch(() => setHealth("error"));
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-indigo-900 text-white p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold">Vite + React + Tailwind</h1>
        <p className="text-slate-300">API health: {health}</p>
        <a href="#" className="inline-block rounded-xl px-4 py-2 bg-indigo-600 hover:bg-indigo-500 transition">
          Styled Button
        </a>
      </div>
    </div>
  );
}
