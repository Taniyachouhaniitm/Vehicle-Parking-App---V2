<template>
  <div class="container mt-4">
    <div class="text-center mb-4">
      <h2 class="fw-bold">🚗 Welcome to Your Parking Dashboard</h2>
      <p class="text-muted">
        Easily view available parking lots, check spot availability, and manage your reservations—all in one place.
      </p>
    </div>

    <!-- Dashboard section -->
    <div class="card shadow-sm p-4 mb-4">
      <h4 class="mb-3">🔍 Quick View: Available Parking Lots</h4>

      <!-- Use the reusable component -->
      <AvailableParkingLots />

      <!-- Call-to-action buttons -->
      <router-link to="/user/available-lots" class="btn btn-primary mt-3">
        View & Book from All Parking Lots →
      </router-link>

      <router-link to="/user/reservations" class="btn btn-secondary mt-3">
        View My Reservations Details →
      </router-link>

      <!-- Report buttons -->
      <div class="mt-4">
        <button class="btn btn-primary me-2" @click="downloadMonthlyReport">
          📥 Download Monthly Report (HTML)
        </button>
        <button class="btn btn-success" @click="exportCSV">
          📤 Export CSV via Email
        </button>
      </div>

      <!-- Logout -->
      <div class="mt-4">
        <button class="btn btn-danger" @click="logout">
          🔒 Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserHome',
  methods: {
    downloadMonthlyReport() {
      fetch(import.meta.env.VITE_BASEURL + "/user/monthly-report", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to download report");
          }
          return response.blob();
        })
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "monthly_report.html";
          a.click();
          window.URL.revokeObjectURL(url);
        })
        .catch((err) => {
          alert("Download failed");
          console.error(err);
        });
    },
    exportCSV() {
      fetch(import.meta.env.VITE_BASEURL+'/user/export-csv', {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // optional, helps for clarity
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then(async (res) => {
          const data = await res.json();
          if (!res.ok) {
            throw new Error(data.error || "Server error");
          }
          alert(data.message || "CSV export request sent!");
        })
        .catch((err) => {
          console.error("CSV export failed:", err);
          alert("Failed to send CSV export request.");
        });
    },

    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 12px;
  background: #f9f9f9;
}
h2 {
  color: #2c3e50;
}
.btn-primary {
  background-color: #007bff;
  border: none;
}
.btn-primary:hover {
  background-color: #0056b3;
}
.btn-success {
  background-color: #28a745;
}
.btn-success:hover {
  background-color: #218838;
}
.btn-danger {
  background-color: #dc3545;
  border: none;
}
.btn-danger:hover {
  background-color: #c82333;
}
</style>
