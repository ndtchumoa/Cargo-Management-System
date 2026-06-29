export default function StatCard({ title, value, sub, icon: Icon, color = "#4f9cf9" }) {
  return (
    <div style={{
      background: "#fff", borderRadius: 12, padding: "1.25rem 1.5rem",
      boxShadow: "0 1px 4px rgba(0,0,0,0.07)", display: "flex",
      alignItems: "center", gap: 16, minWidth: 0,
    }}>
      <div style={{
        width: 48, height: 48, borderRadius: 12,
        background: color + "18", display: "flex",
        alignItems: "center", justifyContent: "center", flexShrink: 0,
      }}>
        <Icon size={22} color={color} />
      </div>
      <div style={{ minWidth: 0 }}>
        <div style={{ fontSize: 13, color: "#8892a4", marginBottom: 2 }}>{title}</div>
        <div style={{ fontSize: 22, fontWeight: 700, color: "#1a1f2e" }}>{value}</div>
        {sub && <div style={{ fontSize: 12, color: "#8892a4", marginTop: 2 }}>{sub}</div>}
      </div>
    </div>
  );
}
