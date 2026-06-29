import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard, Package, FileText,
  TruckIcon, BarChart2, Route, Menu, X
} from "lucide-react";
import { useState } from "react";

const NAV = [
  { to: "/",           icon: LayoutDashboard, label: "Tổng quan"    },
  { to: "/orders",     icon: Package,         label: "Đơn hàng"     },
  { to: "/invoices",   icon: FileText,        label: "Hóa đơn"      },
  { to: "/operations", icon: TruckIcon,       label: "Vận hành"     },
  { to: "/analytics",  icon: BarChart2,       label: "Phân tích"    },
  { to: "/optimize",   icon: Route,           label: "Tối ưu lộ trình" },
];

export default function Layout() {
  const [open, setOpen] = useState(true);

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#f4f6f9" }}>
      {/* Sidebar */}
      <aside style={{
        width: open ? 220 : 64, transition: "width 0.2s",
        background: "#1a1f2e", color: "#fff", flexShrink: 0,
        display: "flex", flexDirection: "column",
      }}>
        {/* Logo */}
        <div style={{
          padding: "1.25rem 1rem", display: "flex",
          alignItems: "center", gap: 10, borderBottom: "1px solid #2d3548"
        }}>
          <TruckIcon size={22} color="#4f9cf9" />
          {open && <span style={{ fontWeight: 700, fontSize: 15, color: "#fff" }}>
            CargoMS
          </span>}
          <button
            onClick={() => setOpen(!open)}
            style={{
              marginLeft: "auto", background: "none", border: "none",
              color: "#8892a4", cursor: "pointer", padding: 4,
            }}
          >
            {open ? <X size={16} /> : <Menu size={16} />}
          </button>
        </div>

        {/* Nav items */}
        <nav style={{ flex: 1, padding: "0.75rem 0" }}>
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to} to={to} end={to === "/"}
              style={({ isActive }) => ({
                display: "flex", alignItems: "center", gap: 12,
                padding: "0.6rem 1rem", textDecoration: "none",
                color: isActive ? "#4f9cf9" : "#8892a4",
                background: isActive ? "#242b3d" : "transparent",
                borderLeft: isActive ? "3px solid #4f9cf9" : "3px solid transparent",
                fontSize: 14, fontWeight: isActive ? 600 : 400,
                transition: "all 0.15s", whiteSpace: "nowrap", overflow: "hidden",
              })}
            >
              <Icon size={18} style={{ flexShrink: 0 }} />
              {open && label}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        {open && (
          <div style={{
            padding: "0.75rem 1rem", fontSize: 11,
            color: "#4a5568", borderTop: "1px solid #2d3548"
          }}>
            cargo_db · MySQL 8.0
          </div>
        )}
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, padding: "1.5rem", overflow: "auto" }}>
        <Outlet />
      </main>
    </div>
  );
}
