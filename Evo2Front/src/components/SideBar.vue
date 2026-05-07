<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-title">
        <svg class="sidebar-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3L5 6.5L9 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M5 6.5H15C17.7614 6.5 20 8.73858 20 11.5V20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>{{ t('sidebar.menu') }}</span>
      </div>
    </div>

    <div class="menu">
      <div
        class="menu-item"
        :class="{ active: current === 'dataset' }"
        @click="select('dataset')"
      >
        <svg class="menu-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.5"/>
          <path d="M7 8H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 12H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 16H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span class="menu-text">{{ t('sidebar.dataset') }}</span>
        <span class="menu-badge" v-if="current === 'dataset'"></span>
      </div>

      <div
        class="menu-item"
        :class="{ active: current === 'generate' }"
        @click="select('generate')"
      >
        <svg class="menu-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 5V19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M5 12H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M18.364 5.63604C21.8787 9.15076 21.8787 14.8492 18.364 18.3639C14.8492 21.8787 9.15076 21.8787 5.63604 18.3639C2.12132 14.8492 2.12132 9.15076 5.63604 5.63604" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span class="menu-text">{{ t('sidebar.generate') }}</span>
        <span class="menu-badge" v-if="current === 'generate'"></span>
      </div>

      <div
        class="menu-item"
        :class="{ active: current === 'analysis' }"
        @click="select('analysis')"
      >
        <svg class="menu-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 21H6.2C5.0799 21 4.51984 21 4.09202 20.782C3.71569 20.5903 3.40973 20.2843 3.21799 19.908C3 19.4802 3 18.9201 3 17.8V3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M6 15L9 18L15 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M21 11V3H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="menu-text">{{ t('sidebar.analysis') }}</span>
        <span class="menu-badge" v-if="current === 'analysis'"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../i18n'

const emit = defineEmits(['select'])
const current = ref('dataset')
const { t } = useI18n()

function select(key) {
  current.value = key
  emit('select', key)
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  box-shadow: 1px 0 3px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 5;
}

.sidebar-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-icon {
  width: 16px;
  height: 16px;
}

.menu {
  padding: 16px 12px;
  flex: 1;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  margin-bottom: 4px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748b;
  position: relative;
  border: 1px solid transparent;
}

.menu-item:hover {
  background: linear-gradient(135deg, #f0f4ff 0%, #f8fafc 100%);
  color: #475569;
  border-color: #e2e8f0;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.menu-item.active {
  background: linear-gradient(135deg, #e8f0ff 0%, #f0f9ff 100%);
  color: #2563eb;
  border-color: #dbeafe;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
}

.menu-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.menu-text {
  font-size: 15px;
  font-weight: 500;
  flex: 1;
}

.menu-badge {
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 50%;
  animation: badge-pulse 2s infinite;
}

@keyframes badge-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.menu-item,
.menu-icon,
.menu-text {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
