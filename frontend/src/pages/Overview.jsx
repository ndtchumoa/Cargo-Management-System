import { useEffect, useState } from "react";
import { Package, FileText, TruckIcon, AlertCircle } from "lucide-react";
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, CartesianGrid,
} from "recharts";
import StatCard from "../components/StatCard";
import { analyticsApi } from "../api/orders";

const STATUS_COLOR = {
  "Da giao":        "#22c55e",
  "Dang van chuyen":"#4f9cf9",
  "Cho xu ly":      "#f59e0b",
  "Hoan tra":       "#ef4444",
};

const MONTH_VI = ["", "T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12"];

const fmt = (n) => new Intl.NumberFormat("vi-VN").format(n) + " đ";

export default function Overview() {
  const [summary, setSummary]   = useState([]);
  const [revenue, setRevenue]   = useState([]);
  const [topRoutes, setTopRoutes] = useState([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    Promise.all([
      analyticsApi.orderSummary(),
      analyticsApi.revenue(),
      analyticsApi.topRoutes(),
    ]).then(([s, r, t]) => {
      setSummary(s.data);
      setRevenue(r.data.map(d => ({ ...d, thang: MONTH_VI[d.thang] })));
      setTopRoutes(t.data);
    }).finally(() => setLoading(false));
  }, []);

  const total    = summary.reduce((a, b) => a + b.so_luong, 0);
  const delivered = summary.find(s => s.trang_thai === "Da giao")?.so_luong || 0;
  const inTransit = summary.find(s => s.trang_thai === "Dang van chuyen")?.so_luong || 0;
  const returned  = summary.find(s => s.trang_thai === "Hoan tra")?.so_luong || 0;

  if (loading) return (
    <div style={{ display:"flex", alignItems:"center", justifyContent:"center", height:"60vh", color:"#8892a4" }}>
      Đang tải dữ liệu...
    </div>
  );

  return (
    <div>
      <h1 style={{ fontSize: 22, fontWeight: 700, color: "#1a1f2e", marginBottom: "1.5rem" }}>
        Tổng quan
      </h1>

      {/* Stat cards */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit, minmax(200px,1fr))", gap:16, marginBottom:"1.5rem" }}>
        <StatCard title="Tổng đơn hàng"    value={total}     icon={Package}     color="#4f9cf9" />
        <StatCard title="Đã giao"           value={delivered} icon={TruckIcon}   color="#22c55e" />
        <StatCard title="Đang vận chuyển"   value={inTransit} icon={TruckIcon}   color="#f59e0b" />
        <StatCard title="Hoàn trả"          value={returned}  icon={AlertCircle} color="#ef4444" />
      </div>

      {/* Charts row */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:"1.5rem" }}>
        {/* Donut chart trạng thái */}
        <div style={{ background:"#fff", borderRadius:12, padding:"1.25rem", boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
          <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
            Đơn hàng theo trạng thái
          </h2>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={summary} dataKey="so_luong" nameKey="trang_thai"
                cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={3}>
                {summary.map((s) => (
                  <Cell key={s.trang_thai} fill={STATUS_COLOR[s.trang_thai] || "#8892a4"} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => [`${v} đơn`]} />
              <Legend iconType="circle" iconSize={10} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Line chart doanh thu */}
        <div style={{ background:"#fff", borderRadius:12, padding:"1.25rem", boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
          <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
            Doanh thu theo tháng
          </h2>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={revenue} margin={{ right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="thang" tick={{ fontSize:12 }} />
              <YAxis tick={{ fontSize:11 }} tickFormatter={(v) => (v/1e6).toFixed(0)+"M"} />
              <Tooltip formatter={(v) => [fmt(v)]} />
              <Line type="monotone" dataKey="tong_doanh_thu" stroke="#4f9cf9"
                strokeWidth={2} dot={{ r:4 }} name="Doanh thu" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top routes table */}
      <div style={{ background:"#fff", borderRadius:12, padding:"1.25rem", boxShadow:"0 1px 4px rgba(0,0,0,0.07)" }}>
        <h2 style={{ fontSize:15, fontWeight:600, color:"#1a1f2e", marginBottom:"1rem" }}>
          Top lộ trình
        </h2>
        <table style={{ width:"100%", borderCollapse:"collapse", fontSize:14 }}>
          <thead>
            <tr style={{ background:"#f8f9fb" }}>
              {["Lộ trình","Số đơn","Tổng giá trị hàng"].map(h => (
                <th key={h} style={{ padding:"8px 12px", textAlign:"left", color:"#8892a4", fontWeight:600, fontSize:12 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {topRoutes.map((r, i) => (
              <tr key={r.id_lt} style={{ borderTop:"1px solid #f0f2f5" }}>
                <td style={{ padding:"10px 12px", color:"#1a1f2e" }}>{r.ten_lt}</td>
                <td style={{ padding:"10px 12px" }}>
                  <span style={{
                    background:"#4f9cf918", color:"#4f9cf9",
                    borderRadius:6, padding:"2px 8px", fontSize:12, fontWeight:600,
                  }}>{r.so_don}</span>
                </td>
                <td style={{ padding:"10px 12px", color:"#22c55e", fontWeight:500 }}>
                  {fmt(r.tong_gia_tri)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
