import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export function useAgentStream(threadId: string, message: string, restaurantId: string) {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const url = `${API_BASE}/runs/${threadId}/stream?message=${encodeURIComponent(message)}&restaurant_id=${restaurantId}`;
    const es = new EventSource(url);
    es.onmessage = (e) => setEvents((prev) => [...prev, JSON.parse(e.data)]);
    es.onerror = () => es.close();
    return () => es.close();
  }, [threadId, message, restaurantId]);

  return events;
}