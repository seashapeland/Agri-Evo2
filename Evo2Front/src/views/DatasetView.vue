<template>
  <div class="dataset-view">
    <!-- 标题区域 -->
    <!--<div class="header-section">
      <div class="title-wrapper">
        <svg class="title-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.5"/>
          <path d="M7 8H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 12H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 16H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <h2 class="section-title">
          <span class="title-text">基因数据集管理</span>
        </h2>
      </div> 
      <div class="header-actions">
        <button class="action-btn refresh-btn" @click="refreshData">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 7V4C20 3.44772 19.5523 3 19 3H16M4 7V4C4 3.44772 4.44772 3 5 3H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M20 17V20C20 20.5523 19.5523 21 19 21H16M4 17V20C4 20.5523 4.44772 21 5 21H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M16 3L19 7H15C15 7 14 7 14 8V11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M8 21L5 17H9C9 17 10 17 10 16V13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>刷新数据</span>
        </button>
      </div>
    </div> -->

    <!-- 标签页导航 -->
    <div class="tab-container">
      <!--<div class="tab-nav">
        <div
          class="tab-item"
          :class="{ active: currentTab === 'list' }"
          @click="currentTab = 'list'"
        >
          <svg class="tab-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5"/>
            <path d="M7 8H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M7 12H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <circle cx="17" cy="12" r="1" fill="currentColor"/>
          </svg>
          <span class="tab-text">数据集列表</span>
          <div class="tab-indicator" v-if="currentTab === 'list'"></div>
        </div>
        
        <div
          class="tab-item"
          :class="{ active: currentTab === 'detail' }"
          @click="currentTab = 'detail'"
        >
          <svg class="tab-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 17L9 19C9 20.1046 9.89543 21 11 21H19C20.1046 21 21 20.1046 21 19V11C21 9.89543 20.1046 9 19 9H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M15 9H5C3.89543 9 3 8.10457 3 7V5C3 3.89543 3.89543 3 5 3H13C14.1046 3 15 3.89543 15 5V15C15 16.1046 14.1046 17 13 17H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M8 13L12 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 13L8 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="tab-text">数据集上传</span>
          <div class="tab-indicator" v-if="currentTab === 'detail'"></div>
        </div>
      </div> -->
      
      <!-- 内容卡片 -->
      <div class="content-card">
          <div class="content-area">
                <component :is="currentTabComponent" class="tab-content-component" />
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import DatasetList from './dataset/DatasetList.vue'
import DatasetStatistics from './dataset/DatasetStatistics.vue'

const currentTab = ref('list')

const currentTabComponent = computed(() => {
  switch (currentTab.value) {
    case 'list':
      return DatasetList
    case 'detail':
      return DatasetStatistics
    default:
      return DatasetList
  }
})


</script>

<style scoped>
.dataset-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100%;
}

/* 标题区域 */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  padding: 0 4px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: #3b82f6;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.title-text {
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}



/* 操作按钮 */
.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.action-btn:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-color: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 标签页导航 */
.tab-container {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.tab-nav {
  display: flex;
  gap: 4px;
  background: #ffffff;
  padding: 4px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  max-width: fit-content;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  color: #64748b;
  font-weight: 500;
  font-size: 14px;
}

.tab-item:hover {
  background: #f8fafc;
  color: #475569;
}

.tab-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
}

.tab-item.active:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

.tab-icon {
  width: 18px;
  height: 18px;
}

.tab-text {
  position: relative;
  z-index: 1;
}

.tab-indicator {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border-radius: 2px;
  animation: indicator-pulse 2s infinite;
}

@keyframes indicator-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 内容卡片 */
.content-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;   /* 关键 */
  min-height: 0;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.tab-content-component {
  flex: 1;
  min-height: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dataset-view {
    padding: 16px;
  }
  
  .header-section {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .tab-nav {
    width: 100%;
  }
  
  .tab-item {
    flex: 1;
    justify-content: center;
  }
}

/* 加载动画 */
.refresh-btn:active .btn-icon {
  animation: rotate 0.5s ease;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
