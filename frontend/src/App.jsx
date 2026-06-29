import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout      from "./components/Layout";
import Overview    from "./pages/Overview";
import Orders      from "./pages/Orders";
import Analytics   from "./pages/Analytics";
import RouteOptimizer from "./pages/RouteOptimizer";

// Placeholder pages (sẽ build sau)
const Invoices   = () => <div style={{ padding:"2rem", color:"#8892a4" }}>Hóa đơn — đang phát triển</div>;
const Operations = () => <div style={{ padding:"2rem", color:"#8892a4" }}>Vận hành — đang phát triển</div>;

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index          element={<Overview />}       />
          <Route path="orders"  element={<Orders />}         />
          <Route path="invoices"element={<Invoices />}       />
          <Route path="operations" element={<Operations />}  />
          <Route path="analytics"  element={<Analytics />}   />
          <Route path="optimize"   element={<RouteOptimizer />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
