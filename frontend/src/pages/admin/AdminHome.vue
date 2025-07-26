<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  localStorage.clear()
  router.push('/login')
}
</script>

<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">🚗 Admin Home</h2>

    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="list-group shadow">

          <router-link to="/admin/users" class="list-group-item list-group-item-action">
            View All Users
          </router-link>

          <router-link to="/admin/parking_lots" class="list-group-item list-group-item-action">
            Manage Parking Lots
          </router-link>

          <router-link to="/admin/parking_spots" class="list-group-item list-group-item-action">
            Manage Parking Spots
          </router-link>

          <router-link to="/admin/reservations" class="list-group-item list-group-item-action">
            View Reservations
          </router-link>

          <button class="list-group-item list-group-item-action text-danger" @click="logout">
            Logout
          </button>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-group-item {
  font-size: 1.1rem;
}
</style>
