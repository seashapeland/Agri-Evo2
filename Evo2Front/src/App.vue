<template>
  <div class="app">
    <HeaderBar />

    <div class="main">
      <SideBar @select="currentView = $event" />

      <div class="content">
        <component :is="currentComponent" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import HeaderBar from './components/HeaderBar.vue'
import SideBar from './components/SideBar.vue'

import DatasetView from './views/DatasetView.vue'
import DNAGenerateView from './views/DNAGenerateView.vue'
import AnalysisView from './views/AnalysisView.vue'

const currentView = ref('dataset')

const currentComponent = computed(() => {
  switch (currentView.value) {
    case 'dataset':
      return DatasetView
    case 'generate':
      return DNAGenerateView
    case 'analysis':
      return AnalysisView
    default:
      return DatasetView
  }
})
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content {
  flex: 1;
  background: #f5f7fa;
  padding: 24px;
  overflow: auto;
}
</style>
