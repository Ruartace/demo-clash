<script setup lang="ts">
</script>

<template>
  <nav class="navbar">
    <div class="nav-content">
      <div class="logo">ClashFlow</div>
      <div class="links">
        <router-link to="/" class="nav-link" active-class="active">Dashboard</router-link>
        <router-link to="/analysis" class="nav-link" active-class="active">Analysis</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-weight: 700;
  font-size: 20px;
  color: #1d1d1f;
}

.links {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: #86868b;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
  padding: 8px 12px;
  border-radius: 8px;
}

.nav-link:hover {
  color: #1d1d1f;
  background: rgba(0, 0, 0, 0.03);
}

.nav-link.active {
  color: #0071e3;
  background: rgba(0, 113, 227, 0.1);
}
</style>
