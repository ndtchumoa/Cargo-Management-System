import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, PieChart, Pie, Legend,
} from "recharts";
import { analyticsApi } from "../api/orders";

const fmt = (n) => new Intl.NumberFormat("vi-VN").format(n) + " đ";
const COLORS = ["#4f9cf9","#22c55e","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#ec4899","#84cc16"];

export default function Analytics() {
  const [returnRate,   setReturnRate]   = useState([]);
  const [topCustomers, setTopCustomers] = useState([]);
  const [vehicleStatus,setVehicleStatus]= useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      analyticsApi.returnRate(),
      analyticsApi.topCustomers(),
      analyticsApi.vehicleStatus(),
    ]).then(([r, c, v]) => {
      setReturnRate(r.data);
      setTopCustomers(c.data);
      setVehicleStatus(v.data);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ display:"flex", alignItems:"center", justifyContent:"center", height:"60vh", color:"#8892a4" }}>
      Đang tải dữ liệu...
    </div>
  );

  // Gộp vehicle status theo loại
  const vehicleByType = vehicleStatus.reduce((acc, v) => {
    const existing = acc.find(a => a.loai_pt === v.loai_pt);
    if (existing) existing.so_luong += v.so_luong;
    else acc.push({ loai_pt: v.loai_pt, so_luong: v.so_luong });
    return acc;
  }, []);

  const activeCount  = vehicleStatus.filter(v => v.trang_thai === "Hoat dong").reduce((a,b) => a+b.so_luong,0);
  const maintenCount = vehicleStatus.filter(v => v.trang_thai === "Bao tri").reduce((a,b) => a+b.so_luong,0);

  return (
    <div>
      <h1 style={{ fontSize:22, fontWeight:700, color:"#1a1f2e", marginBottom:"1.5rem" }}>
        Phân tích
      </h1>

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:16 }}>
        {/* Return rate bar chart */}
        <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
          boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
          <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
            Tỉ lệ hoàn trả theo lộ trình (%)
          </h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={returnRate} margin={{ right:8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="id_lt" tick={{ fontSize:12 }} />
              <YAxis tick={{ fontSize:12 }} unit="%" />
              <Tooltip
                formatter={(v, n, p) => [`${v}% (${p.payload.so_hoan_tra}/${p.payload.tong_don} đơn)`]}
                labelFormatter={(l) => returnRate.find(r => r.id_lt===l)?.ten_lt || l}
              />
              <Bar dataKey="ti_le_pct" radius={[6,6,0,0]} name="Tỉ lệ hoàn trả">
                {returnRate.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top customers */}
        <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
          boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
          <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
            Top khách hàng gửi hàng nhiều nhất
          </h2>
          <table style={{ width:"100%", borderCollapse:"collapse", fontSize:14 }}>
            <thead>
              <tr style={{ background:"#f8f9fb" }}>
                {["#","Tên KH","Số đơn","Tổng giá trị"].map(h => (
                  <th key={h} style={{ padding:"7px 10px", textAlign:"left",
                    color:"#8892a4", fontWeight:600, fontSize:12 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {topCustomers.map((c, i) => (
                <tr key={c.id_kh} style={{ borderTop:"1px solid #f0f2f5" }}>
                  <td style={{ padding:"9px 10px", color:"#8892a4", fontSize:12 }}>
                    {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i+1}
                  </td>
                  <td style={{ padding:"9px 10px", fontWeight:500, color:"#1a1f2e" }}>{c.ten_kh}</td>
                  <td style={{ padding:"9px 10px" }}>
                    <span style={{
                      background:"#eff6ff", color:"#2563eb",
                      borderRadius:6, padding:"2px 8px", fontSize:12, fontWeight:600,
                    }}>{c.so_don}</span>
                  </td>
                  <td style={{ padding:"9px 10px", color:"#22c55e", fontWeight:500, fontSize:13 }}>
                    {fmt(c.tong_gia_tri)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Vehicle status */}
      <div style={{ background:"#fff", borderRadius:12, padding:"1.5rem",
        boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
        <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
          Trạng thái phương tiện
        </h2>
        <div style={{ display:"grid", gridTemplateColumns:"auto 1fr", gap:32, alignItems:"center" }}>
          {/* Donut */}
          <ResponsiveContainer width={220} height={180}>
            <PieChart>
              <Pie
                data={[
                  { name:"Hoạt động", value: activeCount  },
                  { name:"Bảo trì",   value: maintenCount },
                ]}
                cx="50%" cy="50%" innerRadius={50} outerRadius={75}
                dataKey="value" paddingAngle={4}
              >
                <Cell fill="#22c55e" />
                <Cell fill="#f59e0b" />
              </Pie>
              <Tooltip />
              <Legend iconType="circle" iconSize={10} />
            </PieChart>
          </ResponsiveContainer>

          {/* Table by type */}
          <table style={{ width:"100%", borderCollapse:"collapse", fontSize:14 }}>
            <thead>
              <tr style={{ background:"#f8f9fb" }}>
                {["Loại phương tiện","Số lượng","Hoạt động","Bảo trì"].map(h => (
                  <th key={h} style={{ padding:"7px 12px", textAlign:"left",
                    color:"#8892a4", fontWeight:600, fontSize:12 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {vehicleByType.map(v => {
                const active  = vehicleStatus.find(s => s.loai_pt===v.loai_pt && s.trang_thai==="Hoat dong")?.so_luong || 0;
                const maint   = vehicleStatus.find(s => s.loai_pt===v.loai_pt && s.trang_thai==="Bao tri")?.so_luong  || 0;
                return (
                  <tr key={v.loai_pt} style={{ borderTop:"1px solid #f0f2f5" }}>
                    <td style={{ padding:"9px 12px", fontWeight:500, color:"#1a1f2e" }}>{v.loai_pt}</td>
                    <td style={{ padding:"9px 12px", fontWeight:700 }}>{v.so_luong}</td>
                    <td style={{ padding:"9px 12px", color:"#16a34a" }}>{active}</td>
                    <td style={{ padding:"9px 12px", color:"#ca8a04" }}>{maint}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
