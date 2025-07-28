// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import AdminHome from '../pages/admin/AdminHome.vue'
import UserHome from '../pages/user/UserHome.vue'
import AllUsers from '../pages/admin/AllUsers.vue'
import ParkingSpots from '../pages/admin/ParkingSpots.vue'
import AvailableParkingLots from '../pages/user/AvailableParkingLots.vue'
import AdminCreateLot from '../pages/admin/AdminCreateLot.vue'
import AllReservations from '../pages/admin/AllReservations.vue'
import MyReservations from '../pages/user/MyReservations.vue'
import AdminStats from '../pages/admin/AdminStats.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'signup', component: Register },
  { path: '/home', name: 'home', component: Home },
  { path: '/admin/home', component: AdminHome },
  { path: '/user/home', component: UserHome },
  { path: '/admin/users', component: AllUsers },
  { path: '/admin/parking_spots', component: ParkingSpots },
  { path: '/user/available-lots', component: AvailableParkingLots },
  { path: '/admin/parking_lots', component: AdminCreateLot },
  { path: '/admin/reservations', component: AllReservations },
  { path: '/user/reservations', component: MyReservations },
  { path: '/admin/analytics', component: AdminStats }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

