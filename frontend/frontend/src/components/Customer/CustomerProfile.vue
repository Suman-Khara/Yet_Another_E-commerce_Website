<template>
  <div class="profile-container">
    <h2>Customer Profile</h2>
    <div class="profile-wrapper">
      <!-- Left Section: Personal Details -->
      <div class="personal-details">
        <form @submit.prevent="toggleEdit">
          <label>Username</label>
          <input type="text" v-model="profile.username" disabled class="readonly" />

          <label>Email</label>
          <input type="email" v-model="profile.email" disabled class="readonly" />

          <label>Phone Number</label>
          <input
            type="text"
            v-model="profile.phone_number"
            :disabled="!isEditing"
            :class="{ editable: isEditing, readonly: !isEditing }"
          />

          <label>Address</label>
          <textarea
            v-model="profile.address"
            :disabled="!isEditing"
            :class="{ editable: isEditing, readonly: !isEditing }"
          ></textarea>

          <button type="submit">{{ isEditing ? "Save Changes" : "Update Profile" }}</button>
        </form>

        <button @click="verifyEmail" class="verify-btn">Verify Email</button>
        <p v-if="emailVerified" class="success">Verification mail has been sent.</p>
      </div>

      <!-- Right Section: History -->
      <div class="history-section">
        <h3>History</h3>
        <div class="history-content">
          <p>Order history and past actions will be displayed here.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      profile: {
        username: "",
        email: "",
        phone_number: "",
        address: ""
      },
      emailVerified: false,
      isEditing: false // Editing is disabled by default
    };
  },
  mounted() {
    console.log("Current route params:", this.$route.params);
  },
  watch: {
    "$route.params.username": {
      immediate: true,
      handler(newUsername) {
        console.log("Watcher triggered with username:", newUsername);
        this.fetchProfile();
      }
    }
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const username = this.$route.params.username;
        console.log("Fetching profile for:", username);

        const response = await axios.get(`http://127.0.0.1:8000/user/customer/profile/${username}/`, {
          headers: { Authorization: `Token ${token}` }
        });

        console.log("Profile data received:", response.data);
        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    async toggleEdit() {
      if (this.isEditing) {
        // Save changes if editing is enabled
        try {
          const token = localStorage.getItem("token");
          await axios.put(`http://127.0.0.1:8000/user/customer/profile/update/${this.profile.username}/`, this.profile, {
            headers: { Authorization: `Token ${token}` }
          });
          alert("Profile updated successfully!");
        } catch (error) {
          console.error("Error updating profile:", error);
        }
      }
      // Toggle edit mode
      this.isEditing = !this.isEditing;
    },
    verifyEmail() {
      alert("Verification mail has been sent.");
    }
  }
};
</script>

<style scoped>
.profile-container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 2rem;
  background: rgb(35, 35, 35);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 255, 170, 255);
}

.profile-wrapper {
  display: flex;
  gap: 20px;
}

/* Left Section: Personal Details */
.personal-details {
  flex: 1;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Read-only inputs are white */
.readonly {
  background-color: transparent;
  color: white;
  border: 1px solid #ccc;
}

/* Editable inputs turn black when editing is enabled */
.editable {
  background-color: white;
  color: black;
}

button {
  background: transparent; /* No default background */
  border: 2px solid #41b883; /* Vue green border */
  padding: 10px;
  font-size: 16px;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
  color: white; /* Default text color */
  cursor: pointer;
  transition: color 0.3s ease-in-out, border-color 0.3s ease-in-out;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  color: #41b883; /* Change text color on hover */
  border-color: #41b883; /* Keep border color consistent */
}

.verify-btn {
  margin-top: 10px;
  border: 2px solid #ff9900; /* Orange border for verify button */
}

.verify-btn:hover {
  color: #ff9900; /* Change text color to orange on hover */
  border-color: #ff9900;
}

.success {
  color: green;
  margin-top: 10px;
}

/* Right Section: History */
.history-section {
  flex: 1;
  background: rgb(15, 15, 15);
  padding: 15px;
  border-radius: 5px;
  max-height: 300px;
  overflow-y: auto; /* Enables scrolling inside the history section */
}

.history-content {
  height: 400px; /* Simulating long content to enable scrolling */
}

@media (max-width: 768px) {
  .profile-wrapper {
    flex-direction: column;
  }
}
</style>