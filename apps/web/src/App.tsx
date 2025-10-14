import { useEffect, useState } from "react";
import { api } from "./lib/api";

type Task = { id: number; title: string; done: boolean; note?: string | null };

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api<Task[]>("/tasks");
      setTasks(data);
    } finally {
      setLoading(false);
    }
  };

  const add = async () => {
    if (!title.trim()) return;
    await api<Task>("/tasks", {
      method: "POST",
      body: JSON.stringify({ title }),
    });
    setTitle("");
    load();
  };

  const toggle = async (t: Task) => {
    await api<Task>(`/tasks/${t.id}`, {
      method: "PATCH",
      body: JSON.stringify({ done: !t.done }),
    });
    load();
  };

  const remove = async (id: number) => {
    await api<void>(`/tasks/${id}`, { method: "DELETE" });
    load();
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">Tasks</h1>

      <div className="flex gap-2 mb-6">
        <input
          className="bg-gray-800 p-2 rounded w-80 outline-none"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task..."
        />
        <button onClick={add} className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded">
          Add
        </button>
      </div>

      {loading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <ul className="space-y-2">
          {tasks.map((t) => (
            <li key={t.id} className="bg-gray-800 rounded p-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={t.done}
                  onChange={() => toggle(t)}
                  className="w-5 h-5"
                />
                <span className={t.done ? "line-through text-gray-400" : ""}>{t.title}</span>
              </div>
              <button
                onClick={() => remove(t.id)}
                className="text-red-400 hover:text-red-300"
                title="Delete"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
