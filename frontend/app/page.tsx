"use client";
import { useState } from "react";
import { ChatResult, PurchaseOrder, sendChat } from "@/lib/api";
import { ApprovalCard } from "@/components/ApprovalCard";

export default function Dashboard() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<ChatResult | null>(null);
  const [threadId, setThreadId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const restaurantId = "5c3f04ac-b83a-4720-84e6-3e9f9561f8e3"; // swap for the real one from Supabase

  function responseToText(response: unknown): string {
    if (typeof response === "string") return response;
    if (Array.isArray(response)) {
      const text = response
        .filter((item): item is { text: string } => typeof item === "object" && item !== null && "text" in item && typeof item.text === "string")
        .map((item) => item.text)
        .join("\n");
      if (text) return text;
    }
    if (typeof response === "object" && response !== null && "text" in response && typeof response.text === "string") {
      return response.text;
    }
    return JSON.stringify(response);
  }

  function parsePurchaseOrder(response: unknown): PurchaseOrder | null {
    try {
      const parsed = typeof response === "string" ? JSON.parse(response) as PurchaseOrder : response as PurchaseOrder;
      if (!parsed.supplier_name || !Array.isArray(parsed.items) || typeof parsed.total_amount !== "number") {
        return null;
      }
      return parsed;
    } catch {
      return null;
    }
  }

  async function handleSend() {
    if (!message.trim() || isLoading) return;
    const threadId = crypto.randomUUID();
    setThreadId(threadId);
    setIsLoading(true);
    setError(null);
    try {
      setResult(await sendChat(threadId, message, restaurantId));
    } catch {
      setError("The manager could not reach the kitchen system. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="dashboard-shell">
      <header className="page-header">
        <p className="eyebrow">Operations cockpit</p>
        <h1>AI Restaurant Manager</h1>
        <p className="subtitle">Ask about stock, sales, and forecasts. The manager will surface decisions that need your sign-off.</p>
      </header>

      <form className="ask-bar" onSubmit={(event) => { event.preventDefault(); void handleSend(); }}>
        <input
          className="ask-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about inventory, sales, or forecasts..."
        />
        <button type="submit" disabled={isLoading || !message.trim()} className="send-button">
          {isLoading ? "Thinking..." : "Ask manager"}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {result && (
        <div className="results-stack">
          <section className="response-panel">
            <p className="eyebrow">Manager response</p>
            {(() => {
              const responseText = responseToText(result.response);
              const purchaseOrder = parsePurchaseOrder(responseText);

              return purchaseOrder ? (
                <div className="response-order">
                  <p className="response-intro">Purchase order prepared for <strong>{purchaseOrder.supplier_name}</strong></p>
                  <div className="response-table-wrap">
                    <table className="response-table">
                      <thead>
                        <tr>
                          <th>Item</th>
                          <th>Quantity</th>
                          <th>Unit price</th>
                          <th>Line total</th>
                        </tr>
                      </thead>
                      <tbody>
                        {purchaseOrder.items.map((item, index) => (
                          <tr key={`${item.item_name}-${index}`}>
                            <td>{item.item_name}</td>
                            <td>{item.quantity} {item.unit}</td>
                            <td>${item.unit_price.toFixed(2)}</td>
                            <td>${(item.quantity * item.unit_price).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <p className="response-total"><span>Total</span><strong>${purchaseOrder.total_amount.toFixed(2)}</strong></p>
                </div>
              ) : (
                <p className="response-text">{responseText}</p>
              );
            })()}
          </section>
          {result.approval_requested && result.draft_order && threadId && (
            <ApprovalCard threadId={threadId} draftOrder={result.draft_order} />
          )}
        </div>
      )}
    </main>
  );
}