<template>
  <div>
    <div class="menu-icon" @click="toggleDrawer">&#9776;</div>

    <!-- Side Drawer -->
    <div class="side-drawer" v-if="isDrawerOpen">
      <ul>
        <li @click="navigateTo('/customer/profile/' + profile.username)">Profile</li>
        <li @click="navigateTo('/customer/order-history')">Order History</li>
        <li @click="navigateTo('/customer/cart')">Cart</li>
        <li @click="navigateTo('/customer/products')">Product List</li>
        <li @click="logout">Log Out</li>
      </ul>
    </div>
    <!-- Profile Section -->
    <div class="profile-container">
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
      isEditing: false,
      isDrawerOpen: false
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const username = this.$route.params.username;

        const response = await axios.get(`http://127.0.0.1:8000/user/customer/profile/${username}/`, {
          headers: { Authorization: `Token ${token}` }
        });

        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    async toggleEdit() {
      if (this.isEditing) {
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
      this.isEditing = !this.isEditing;
    },
    verifyEmail() {
      alert("Verification mail has been sent.");
    },
    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen;
    },
    navigateTo(route) {
      this.$router.push(route);
      this.isDrawerOpen = false;
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #333;
  color: white;
}

.menu-icon {
  position: absolute;
  top: 70px;
  right: 10px;
  font-size: 2rem; /* Increased size */
  cursor: pointer;
}

.side-drawer {
  position: absolute;
  top: 110px; /* Slightly below the icon */
  right: 10px;
  width: 220px; /* Increased width */
  background-color: #222;
  color: white;
  padding: 1.5rem; /* More padding for better visibility */
  border-radius: 12px; /* More rounded edges */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Deeper shadow for effect */
}

.side-drawer ul {
  list-style-type: none;
  padding: 0;
}

.side-drawer li {
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #444;
}

.side-drawer li:hover {
  background-color: #555;
}

.profile-container {
  width: 90%;
  max-width: 600px;
  margin: 5vh auto;
  padding: 2rem;
  background: rgb(35, 35, 35);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 255, 170, 255);
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.readonly {
  background-color: transparent;
  color: white;
}

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
}
</style>
