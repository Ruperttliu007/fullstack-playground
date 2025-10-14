const BASE = (import.meta.env.VITE_API_URL as string) || "http://localhost:8000";

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "content-type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) throw new Error(await res.text());
  return (res.status === 204 ? (undefined as unknown as T) : await res.json());
}
