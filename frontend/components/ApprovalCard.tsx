"use client";
import { useState } from "react";
import { approveOrder, PurchaseOrder } from "@/lib/api";

export function ApprovalCard({ threadId, draftOrder }: { threadId: string; draftOrder: PurchaseOrder }) {
  const [status, setStatus] = useState<"pending" | "approved">("pending");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleApprove() {
    setIsSubmitting(true);
    setError(null);
    try {
      await approveOrder(threadId);
      setStatus("approved");
    } catch (approvalError) {
      setError(approvalError instanceof Error ? approvalError.message : "Approval could not be completed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="approval-card" aria-live="polite">
      <div className="approval-heading">
        <div>
          <p className="eyebrow">Action required</p>
          <h2>Review purchase order</h2>
        </div>
        <span className="pending-badge">Waiting for approval</span>
      </div>
      <p className="supplier">Supplier: <strong>{draftOrder.supplier_name}</strong></p>
      <ul className="order-items">
        {draftOrder.items.map((item, i) => (
          <li key={`${item.item_name}-${i}`}>
            <span>{item.item_name}</span>
            <span>{item.quantity} {item.unit} <small>${item.unit_price.toFixed(2)}/{item.unit}</small></span>
          </li>
        ))}
      </ul>
      <p className="order-total"><span>Total</span><strong>${draftOrder.total_amount.toFixed(2)}</strong></p>
      {error && <p className="error-message">{error}</p>}
      {status === "pending" ? (
        <button onClick={handleApprove} className="approve-button" disabled={isSubmitting}>
          {isSubmitting ? "Approving..." : "Approve order"}
        </button>
      ) : (
        <p className="approved-status">Order approved</p>
      )}
    </section>
  );
}