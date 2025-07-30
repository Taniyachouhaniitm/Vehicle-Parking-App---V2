<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">All Parking Spots</h2>
    
    <table v-if="spots.length" class="table table-bordered table-striped">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Lot ID</th>
          <th>Spot Number</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in spots" :key="spot.id">
          <td>{{ spot.id }}</td>
          <td>{{ spot.lot_id }}</td>
          <td>{{ spot.spot_number }}</td>
          <td>{{ spot.status }}</td>
          <td>
            <button class="btn btn-primary btn-sm me-2" @click="startEdit(spot)">
              Edit
            </button>
            <button class="btn btn-danger btn-sm" @click="deleteSpot(spot.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="alert alert-info text-center">
      No parking spots found.
    </div>

    <div v-if="editingSpot" class="modal fade show d-block" tabindex="-1" style="background: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Parking Spot</h5>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Spot Number</label>
              <input v-model="editForm.spot_number" class="form-control" type="text" />
            </div>
            <div class="mb-3">
              <label class="form-label">Status</label>
              <select v-model="editForm.status" class="form-select">
                <option value="A">Available</option>
                <option value="O">Occupied</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cancelEdit">Cancel</button>
            <button class="btn btn-success" @click="submitEdit">Save</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3 text-center">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const spots = ref([])
const error = ref('')
const editingSpot = ref(null)
const editForm = ref({ spot_number: '', status: '' })

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(import.meta.env.VITE_BASEURL + 'admin/parking_spots', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      }
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.msg || 'Failed to load parking spots'
      return
    }

    spots.value = data
  } catch (err) {
    console.error(err)
    error.value = 'Server error. Please try again later.'
  }
})


const deleteSpot = async (id) => {
  if (!confirm('Are you sure you want to delete this parking spot?')) return

  try {
    const token = localStorage.getItem('token')
    const res = await fetch(
      `${import.meta.env.VITE_BASEURL}admin/parking_spots/${id}`,
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      }
    )

    const data = await res.json()

    if (!res.ok) {
      error.value = data.message || 'Failed to delete parking spot'
      return
    }


    spots.value = spots.value.filter(spot => spot.id !== id)
  } catch (err) {
    console.error(err)
    error.value = 'Server error. Please try again later.'
  }
}

// Start editing
function startEdit(spot) {
  editingSpot.value = spot
  editForm.value = {
    spot_number: spot.spot_number,
    status: spot.status
  }
}

// Cancel editing
function cancelEdit() {
  editingSpot.value = null
  editForm.value = { spot_number: '', status: '' }
}

// Submit edit
async function submitEdit() {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(
      `${import.meta.env.VITE_BASEURL}admin/parking_spots/${editingSpot.value.id}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(editForm.value)
      }
    )

    const data = await res.json()

    if (!res.ok) {
      error.value = data.message || 'Failed to update parking spot'
      return
    }

    // Update local list
    const index = spots.value.findIndex(s => s.id === editingSpot.value.id)
    if (index !== -1) {
      spots.value[index] = { ...spots.value[index], ...editForm.value }
    }

    cancelEdit()
  } catch (err) {
    console.error(err)
    error.value = 'Server error. Please try again later.'
  }
}
</script>