const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export type PurchaseOrder = {
  supplier_name: string;
  items: Array<{
    item_name: string;
    quantity: number;
    unit: string;
    unit_price: number;
  }>;
  total_amount: number;
};

export type ChatResult = {
  response: string;
  draft_order: PurchaseOrder | null;
  approval_requested: boolean;
};

export async function sendChat(threadId: string, message: string, restaurantId: string) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ thread_id: threadId, message, restaurant_id: restaurantId }),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return (await res.json()) as ChatResult;
}

export async function approveOrder(threadId: string) {
  const res = await fetch(`${API_BASE}/approvals/${threadId}/approve`, { method: "POST" });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Approval failed: ${res.status}`);
  }
  return res.json();
}