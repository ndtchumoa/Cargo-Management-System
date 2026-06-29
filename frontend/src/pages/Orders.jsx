import { useEffect, useState } from "react";
import { Search, Plus, Eye, RefreshCw } from "lucide-react";
import { ordersApi } from "../api/orders";

const STATUS_COLOR = {
  "Da giao":         { bg: "#dcfce7", text: "#16a34a" },
  "Dang van chuyen": { bg: "#dbeafe", text: "#2563eb" },
  "Cho xu ly":       { bg: "#fef9c3", text: "#ca8a04" },
  "Hoan tra":        { bg: "#fee2e2", text: "#dc2626" },
};

const STATUS_LIST = ["Da giao", "Dang van chuyen", "Cho xu ly", "Hoan tra"];

const fmt = (n) => new Intl.NumberFormat("vi-VN").format(n) + " đ";

function Badge({ status }) {
  const c = STATUS_COLOR[status] || { bg: "#f3f4f6", text: "#6b7280" };
  return (
    <span style={{
      background: c.bg, color: c.text,
      borderRadius: 6, padding: "2px 8px", fontSize: 12, fontWeight: 600,
    }}>{status}</span>
  );
}

export default function Orders() {
  const [orders, setOrders]         = useState([]);
  const [total, setTotal]           = useState(0);
  const [filter, setFilter]         = useState("");
  const [search, setSearch]         = useState("");
  const [loading, setLoading]       = useState(true);
  const [selected, setSelected]     = useState(null);   // tracking modal
  const [tracking, setTracking]     = useState(null);
  const [showCreate, setShowCreate] = useState(false);

  const load = (status = filter) => {
    setLoading(true);
    ordersApi.getAll(status || null)
      .then(r => { setOrders(r.data.data); setTotal(r.data.total); })
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [filter]);

  const openTracking = (id) => {
    setSelected(id);
    setTracking(null);
    ordersApi.getTracking(id).then(r => setTracking(r.data));
  };

  const filtered = orders.filter(o =>
    o.ID_DH.toLowerCase().includes(search.toLowerCase()) ||
    o.ten_nguoi_gui.toLowerCase().includes(search.toLowerCase()) ||
    o.ten_nguoi_nhan.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:"1.5rem" }}>
        <h1 style={{ fontSize:22, fontWeight:700, color:"#1a1f2e" }}>
          Đơn hàng <span style={{ fontSize:14, color:"#8892a4", fontWeight:400 }}>({total})</span>
        </h1>
        <button onClick={() => setShowCreate(true)} style={{
          display:"flex", alignItems:"center", gap:6,
          background:"#4f9cf9", color:"#fff", border:"none",
          borderRadius:8, padding:"8px 14px", fontSize:14,
          fontWeight:600, cursor:"pointer",
        }}>
          <Plus size={16} /> Tạo đơn
        </button>
      </div>

      {/* Filter + Search */}
      <div style={{ display:"flex", gap:12, marginBottom:"1rem", flexWrap:"wrap" }}>
        {/* Status filter */}
        <div style={{ display:"flex", gap:6 }}>
          <button onClick={() => setFilter("")} style={{
            padding:"5px 12px", borderRadius:6, fontSize:13, cursor:"pointer",
            border: !filter ? "none" : "1px solid #e5e7eb",
            background: !filter ? "#4f9cf9" : "#fff",
            color: !filter ? "#fff" : "#6b7280", fontWeight: !filter ? 600 : 400,
          }}>Tất cả</button>
          {STATUS_LIST.map(s => (
            <button key={s} onClick={() => setFilter(s)} style={{
              padding:"5px 12px", borderRadius:6, fontSize:13, cursor:"pointer",
              border: filter === s ? "none" : "1px solid #e5e7eb",
              background: filter === s ? STATUS_COLOR[s]?.bg : "#fff",
              color: filter === s ? STATUS_COLOR[s]?.text : "#6b7280",
              fontWeight: filter === s ? 600 : 400,
            }}>{s}</button>
          ))}
        </div>

        {/* Search */}
        <div style={{ display:"flex", alignItems:"center", gap:8, background:"#fff",
          border:"1px solid #e5e7eb", borderRadius:8, padding:"6px 12px", flex:1, minWidth:200 }}>
          <Search size={15} color="#8892a4" />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Tìm mã đơn, tên khách..."
            style={{ border:"none", outline:"none", fontSize:14, color:"#1a1f2e", width:"100%", background:"transparent" }} />
        </div>

        <button onClick={() => load()} style={{
          display:"flex", alignItems:"center", gap:6,
          background:"#fff", border:"1px solid #e5e7eb",
          borderRadius:8, padding:"6px 12px", fontSize:13, cursor:"pointer", color:"#6b7280",
        }}>
          <RefreshCw size={14} /> Làm mới
        </button>
      </div>

      {/* Table */}
      <div style={{ background:"#fff", borderRadius:12, boxShadow:"0 1px 4px rgba(0,0,0,0.07)", overflow:"hidden" }}>
        <table style={{ width:"100%", borderCollapse:"collapse", fontSize:14 }}>
          <thead>
            <tr style={{ background:"#f8f9fb" }}>
              {["Mã đơn","Người gửi","Người nhận","Lộ trình","KL (kg)","COD","Trạng thái",""].map(h => (
                <th key={h} style={{ padding:"10px 14px", textAlign:"left",
                  color:"#8892a4", fontWeight:600, fontSize:12, whiteSpace:"nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={8} style={{ padding:32, textAlign:"center", color:"#8892a4" }}>Đang tải...</td></tr>
            ) : filtered.length === 0 ? (
              <tr><td colSpan={8} style={{ padding:32, textAlign:"center", color:"#8892a4" }}>Không có đơn hàng</td></tr>
            ) : filtered.map(o => (
              <tr key={o.ID_DH} style={{ borderTop:"1px solid #f0f2f5" }}
                onMouseEnter={e => e.currentTarget.style.background="#f8f9fb"}
                onMouseLeave={e => e.currentTarget.style.background="transparent"}>
                <td style={{ padding:"10px 14px", fontWeight:600, color:"#4f9cf9" }}>{o.ID_DH}</td>
                <td style={{ padding:"10px 14px", color:"#1a1f2e" }}>{o.ten_nguoi_gui}</td>
                <td style={{ padding:"10px 14px", color:"#1a1f2e" }}>{o.ten_nguoi_nhan}</td>
                <td style={{ padding:"10px 14px", color:"#6b7280", fontSize:13 }}>{o.ten_lo_trinh}</td>
                <td style={{ padding:"10px 14px" }}>{o.KHOI_LUONG}</td>
                <td style={{ padding:"10px 14px", color:"#22c55e", fontWeight:500 }}>
                  {fmt(o.cod || 0)}
                </td>
                <td style={{ padding:"10px 14px" }}><Badge status={o.TRANG_THAI} /></td>
                <td style={{ padding:"10px 14px" }}>
                  <button onClick={() => openTracking(o.ID_DH)} style={{
                    display:"flex", alignItems:"center", gap:4,
                    background:"none", border:"1px solid #e5e7eb",
                    borderRadius:6, padding:"4px 8px", fontSize:12,
                    cursor:"pointer", color:"#6b7280",
                  }}>
                    <Eye size={13} /> Tracking
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Tracking Modal */}
      {selected && (
        <div style={{
          position:"fixed", inset:0, background:"rgba(0,0,0,0.4)",
          display:"flex", alignItems:"center", justifyContent:"center", zIndex:100,
        }} onClick={() => setSelected(null)}>
          <div style={{
            background:"#fff", borderRadius:14, padding:"1.5rem",
            width:520, maxWidth:"90vw", maxHeight:"80vh", overflow:"auto",
          }} onClick={e => e.stopPropagation()}>
            <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:"1rem" }}>
              <h2 style={{ fontSize:17, fontWeight:700, color:"#1a1f2e" }}>
                Tracking — {selected}
              </h2>
              <button onClick={() => setSelected(null)} style={{
                background:"none", border:"none", cursor:"pointer", color:"#8892a4", fontSize:20,
              }}>×</button>
            </div>

            {!tracking ? (
              <div style={{ textAlign:"center", color:"#8892a4", padding:"2rem" }}>Đang tải...</div>
            ) : (
              <>
                <div style={{ marginBottom:"1rem", padding:"10px 14px", background:"#f8f9fb", borderRadius:8 }}>
                  <div style={{ fontSize:13, color:"#8892a4" }}>Lộ trình</div>
                  <div style={{ fontWeight:600, color:"#1a1f2e" }}>{tracking.lo_trinh}</div>
                </div>
                <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
                  {tracking.history.map((h, i) => (
                    <div key={h.id_vd} style={{
                      display:"flex", gap:12, alignItems:"flex-start",
                    }}>
                      {/* Timeline dot */}
                      <div style={{ display:"flex", flexDirection:"column", alignItems:"center" }}>
                        <div style={{
                          width:12, height:12, borderRadius:"50%", marginTop:4, flexShrink:0,
                          background: h.trang_thai === "Da giao" ? "#22c55e"
                            : h.trang_thai === "Hoan tra" ? "#ef4444" : "#f59e0b",
                        }} />
                        {i < tracking.history.length - 1 && (
                          <div style={{ width:2, flex:1, background:"#e5e7eb", minHeight:24 }} />
                        )}
                      </div>
                      <div style={{ flex:1, paddingBottom:8 }}>
                        <div style={{ fontWeight:600, fontSize:14, color:"#1a1f2e" }}>
                          {h.chang_duong || "—"}
                        </div>
                        <div style={{ fontSize:12, color:"#8892a4", marginTop:2 }}>
                          NV: {h.nhan_vien || "—"} · Xe: {h.phuong_tien || "—"}
                        </div>
                        <div style={{ fontSize:12, color:"#8892a4" }}>
                          Nhận: {h.thoi_gian_nhan ? new Date(h.thoi_gian_nhan).toLocaleString("vi-VN") : "—"}
                        </div>
                        {h.thoi_gian_giao && (
                          <div style={{ fontSize:12, color:"#22c55e" }}>
                            Giao: {new Date(h.thoi_gian_giao).toLocaleString("vi-VN")}
                          </div>
                        )}
                        <Badge status={h.trang_thai} />
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Create Order Modal */}
      {showCreate && <CreateOrderModal onClose={() => setShowCreate(false)} onCreated={() => { setShowCreate(false); load(); }} />}
    </div>
  );
}

function CreateOrderModal({ onClose, onCreated }) {
  const [form, setForm] = useState({
    KHOI_LUONG: "", QUANG_DUONG: "", THANH_TIEN: "",
    ID_KH_GUI: "", ID_KH_NHAN: "", ID_LT: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const submit = () => {
    setLoading(true); setError("");
    ordersApi.create({
      ...form,
      KHOI_LUONG:  parseFloat(form.KHOI_LUONG),
      QUANG_DUONG: parseFloat(form.QUANG_DUONG),
      THANH_TIEN:  parseFloat(form.THANH_TIEN),
    })
      .then(onCreated)
      .catch(e => setError(e.response?.data?.detail || "Lỗi tạo đơn hàng"))
      .finally(() => setLoading(false));
  };

  const fields = [
    { key:"ID_KH_GUI",   label:"Mã KH gửi",     placeholder:"VD: KH001" },
    { key:"ID_KH_NHAN",  label:"Mã KH nhận",     placeholder:"VD: KH002" },
    { key:"ID_LT",       label:"Mã lộ trình",    placeholder:"VD: LT001" },
    { key:"KHOI_LUONG",  label:"Khối lượng (kg)",placeholder:"VD: 5.0" },
    { key:"QUANG_DUONG", label:"Khoảng cách (km)",placeholder:"VD: 760" },
    { key:"THANH_TIEN",  label:"Giá trị hàng (đ)",placeholder:"VD: 2000000" },
  ];

  return (
    <div style={{
      position:"fixed", inset:0, background:"rgba(0,0,0,0.4)",
      display:"flex", alignItems:"center", justifyContent:"center", zIndex:100,
    }} onClick={onClose}>
      <div style={{
        background:"#fff", borderRadius:14, padding:"1.5rem",
        width:440, maxWidth:"90vw",
      }} onClick={e => e.stopPropagation()}>
        <div style={{ display:"flex", justifyContent:"space-between", marginBottom:"1.25rem" }}>
          <h2 style={{ fontSize:17, fontWeight:700, color:"#1a1f2e" }}>Tạo đơn hàng mới</h2>
          <button onClick={onClose} style={{ background:"none", border:"none", cursor:"pointer", color:"#8892a4", fontSize:20 }}>×</button>
        </div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
          {fields.map(f => (
            <div key={f.key}>
              <label style={{ fontSize:12, color:"#6b7280", display:"block", marginBottom:4 }}>{f.label}</label>
              <input value={form[f.key]} onChange={e => set(f.key, e.target.value)}
                placeholder={f.placeholder}
                style={{
                  width:"100%", padding:"8px 10px", borderRadius:8, fontSize:14,
                  border:"1px solid #e5e7eb", outline:"none", boxSizing:"border-box",
                }} />
            </div>
          ))}
        </div>
        {error && <div style={{ marginTop:10, color:"#ef4444", fontSize:13 }}>{error}</div>}
        <button onClick={submit} disabled={loading} style={{
          marginTop:"1.25rem", width:"100%", padding:"10px",
          background:"#4f9cf9", color:"#fff", border:"none",
          borderRadius:8, fontSize:15, fontWeight:600, cursor:"pointer",
        }}>
          {loading ? "Đang tạo..." : "Tạo đơn"}
        </button>
      </div>
    </div>
  );
}
