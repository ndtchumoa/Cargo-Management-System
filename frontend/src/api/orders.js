import client from "./client";

export const ordersApi = {
  getAll:    (status) => client.get("/api/orders", { params: status ? { status } : {} }),
  getById:   (id)     => client.get(`/api/orders/${id}`),
  create:    (data)   => client.post("/api/orders", data),
  updateStatus: (id, status) => client.patch(`/api/orders/${id}/status`, { TRANG_THAI: status }),
  getTracking:  (id)  => client.get(`/api/orders/${id}/tracking`),
};

export const invoicesApi = {
  getAll:  (trangThai) => client.get("/api/invoices", { params: trangThai ? { trang_thai: trangThai } : {} }),
  getById: (id)        => client.get(`/api/invoices/${id}`),
  create:  (orderIds)  => client.post("/api/invoices", { order_ids: orderIds }),
  pay:     (id)        => client.patch(`/api/invoices/${id}/pay`),
};

export const assignmentsApi = {
  getAll: ()     => client.get("/api/assignments"),
  create: (data) => client.post("/api/assignments", data),
};

export const analyticsApi = {
  revenue:      () => client.get("/api/analytics/revenue"),
  returnRate:   () => client.get("/api/analytics/return-rate"),
  topRoutes:    () => client.get("/api/analytics/top-routes"),
  vehicleStatus:() => client.get("/api/analytics/vehicle-status"),
  topCustomers: () => client.get("/api/analytics/top-customers"),
  orderSummary: () => client.get("/api/analytics/order-status-summary"),
};

export const optimizeApi = {
  route: (from_dtc, to_dtc, weight_kg) =>
    client.post("/api/optimize/route", { from_dtc, to_dtc, weight_kg }),
};
