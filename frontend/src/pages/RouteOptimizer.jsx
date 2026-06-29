import { useState } from "react";
import { Route, Truck, MapPin, Package } from "lucide-react";
import { optimizeApi } from "../api/orders";

const DTC_OPTIONS = [
  { id:"DTC001", name:"Kho Hà Nội"    },
  { id:"DTC002", name:"Kho Đà Nẵng"   },
  { id:"DTC003", name:"Kho TP. HCM"   },
  { id:"DTC004", name:"Kho Hải Phòng" },
  { id:"DTC005", name:"Kho Cần Thơ"   },
  { id:"DTC006", name:"Kho Vinh"      },
  { id:"DTC007", name:"Kho Vũng Tàu"  },
  { id:"DTC008", name:"Kho Thái Nguyên"},
  { id:"DTC009", name:"Kho Hội An"    },
];

const fmt    = (n) => new Intl.NumberFormat("vi-VN").format(n) + " đ";
const fmtNum = (n) => new Intl.NumberFormat("vi-VN").format(n);

export default function RouteOptimizer() {
  const [from,   setFrom]   = useState("");
  const [to,     setTo]     = useState("");
  const [weight, setWeight] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,  setError]  = useState("");

  const search = () => {
    if (!from || !to || !weight) { setError("Vui lòng điền đầy đủ thông tin"); return; }
    if (from === to) { setError("Điểm xuất phát và điểm đích không được trùng nhau"); return; }
    setError(""); setResult(null); setLoading(true);
    optimizeApi.route(from, to, parseFloat(weight))
      .then(r => setResult(r.data))
      .catch(e => setError(e.response?.data?.detail || "Không tìm thấy lộ trình phù hợp"))
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <h1 style={{ fontSize:22, fontWeight:700, color:"#1a1f2e", marginBottom:"1.5rem" }}>
        Tối ưu lộ trình
      </h1>

      {/* Input form */}
      <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
        boxShadow:"0 1px 4px rgba(0,0,0,0.07)", marginBottom:"1.5rem" }}>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr auto", gap:14, alignItems:"end" }}>

          <div>
            <label style={{ fontSize:12, color:"#6b7280", display:"block", marginBottom:6 }}>
              Điểm xuất phát
            </label>
            <select value={from} onChange={e => setFrom(e.target.value)} style={{
              width:"100%", padding:"9px 12px", borderRadius:8, fontSize:14,
              border:"1px solid #e5e7eb", outline:"none", background:"#fff", color:"#1a1f2e",
            }}>
              <option value="">-- Chọn kho --</option>
              {DTC_OPTIONS.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ fontSize:12, color:"#6b7280", display:"block", marginBottom:6 }}>
              Điểm đích
            </label>
            <select value={to} onChange={e => setTo(e.target.value)} style={{
              width:"100%", padding:"9px 12px", borderRadius:8, fontSize:14,
              border:"1px solid #e5e7eb", outline:"none", background:"#fff", color:"#1a1f2e",
            }}>
              <option value="">-- Chọn kho --</option>
              {DTC_OPTIONS.filter(d => d.id !== from).map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ fontSize:12, color:"#6b7280", display:"block", marginBottom:6 }}>
              Khối lượng (kg)
            </label>
            <input type="number" min="0.1" step="0.1" value={weight}
              onChange={e => setWeight(e.target.value)}
              placeholder="VD: 5.0"
              style={{
                width:"100%", padding:"9px 12px", borderRadius:8, fontSize:14,
                border:"1px solid #e5e7eb", outline:"none", boxSizing:"border-box",
              }} />
          </div>

          <button onClick={search} disabled={loading} style={{
            display:"flex", alignItems:"center", gap:8,
            background:"#4f9cf9", color:"#fff", border:"none",
            borderRadius:8, padding:"9px 20px", fontSize:14,
            fontWeight:600, cursor:"pointer", whiteSpace:"nowrap",
          }}>
            <Route size={16} />
            {loading ? "Đang tính..." : "Tìm lộ trình"}
          </button>
        </div>

        {error && (
          <div style={{ marginTop:12, color:"#ef4444", fontSize:13,
            background:"#fee2e2", borderRadius:8, padding:"8px 12px" }}>
            {error}
          </div>
        )}
      </div>

      {/* Result */}
      {result && (
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>

          {/* Path visualization */}
          <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
            boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
            <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1.25rem" }}>
              Lộ trình đề xuất
            </h2>

            {/* Stats row */}
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10, marginBottom:"1.25rem" }}>
              <div style={{ background:"#eff6ff", borderRadius:8, padding:"10px 14px" }}>
                <div style={{ fontSize:11, color:"#6b7280" }}>Tổng khoảng cách</div>
                <div style={{ fontSize:18, fontWeight:700, color:"#2563eb" }}>
                  {fmtNum(result.total_km)} km
                </div>
              </div>
              <div style={{ background:"#f0fdf4", borderRadius:8, padding:"10px 14px" }}>
                <div style={{ fontSize:11, color:"#6b7280" }}>COD ước tính</div>
                <div style={{ fontSize:18, fontWeight:700, color:"#16a34a" }}>
                  {fmt(result.estimated_cod)}
                </div>
              </div>
            </div>

            {/* Timeline path */}
            <div style={{ display:"flex", flexDirection:"column", gap:0 }}>
              {result.path_names.map((name, i) => (
                <div key={i} style={{ display:"flex", gap:14, alignItems:"flex-start" }}>
                  <div style={{ display:"flex", flexDirection:"column", alignItems:"center" }}>
                    <div style={{
                      width:32, height:32, borderRadius:"50%",
                      background: i === 0 ? "#4f9cf9"
                        : i === result.path_names.length - 1 ? "#22c55e" : "#e5e7eb",
                      display:"flex", alignItems:"center", justifyContent:"center",
                      flexShrink:0, color:"#fff", fontWeight:700, fontSize:13,
                    }}>
                      {i === 0 ? "A" : i === result.path_names.length - 1 ? "B" : i}
                    </div>
                    {i < result.path_names.length - 1 && (
                      <div style={{ width:2, height:32, background:"#e5e7eb" }} />
                    )}
                  </div>
                  <div style={{ paddingTop:6, paddingBottom: i < result.path_names.length - 1 ? 0 : 0 }}>
                    <div style={{ fontSize:14, fontWeight:600, color:"#1a1f2e" }}>{name}</div>
                    <div style={{ fontSize:12, color:"#8892a4" }}>{result.path[i]}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Available vehicles */}
          <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
            boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
            <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1.25rem" }}>
              Phương tiện khả dụng
              <span style={{ fontSize:13, color:"#8892a4", fontWeight:400, marginLeft:8 }}>
                (đủ tải trọng ≥ {weight} kg)
              </span>
            </h2>

            {result.available_vehicles.length === 0 ? (
              <div style={{ textAlign:"center", color:"#8892a4", padding:"2rem" }}>
                Không có phương tiện phù hợp
              </div>
            ) : (
              <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
                {result.available_vehicles.map(v => (
                  <div key={v.bien_so} style={{
                    display:"flex", alignItems:"center", gap:12,
                    padding:"10px 14px", borderRadius:8, border:"1px solid #e5e7eb",
                  }}>
                    <div style={{
                      width:36, height:36, borderRadius:8, background:"#eff6ff",
                      display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0,
                    }}>
                      <Truck size={18} color="#4f9cf9" />
                    </div>
                    <div style={{ flex:1 }}>
                      <div style={{ fontWeight:600, fontSize:14, color:"#1a1f2e" }}>{v.bien_so}</div>
                      <div style={{ fontSize:12, color:"#8892a4" }}>{v.loai_pt}</div>
                    </div>
                    <div style={{ textAlign:"right" }}>
                      <div style={{ fontSize:12, color:"#6b7280" }}>Tải trọng</div>
                      <div style={{ fontWeight:600, color:"#22c55e", fontSize:14 }}>
                        {fmtNum(v.trong_tai)} kg
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
