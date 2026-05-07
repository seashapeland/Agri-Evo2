<template>
  <div class="dataset-view-list">
    <div class="header-section">
      <div class="header-actions">
        <button class="action-btn refresh-btn" @click="refreshData">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 7V4C20 3.44772 19.5523 3 19 3H16M4 7V4C4 3.44772 4.44772 3 5 3H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M20 17V20C20 20.5523 19.5523 21 19 21H16M4 17V20C4 20.5523 4.44772 21 5 21H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M16 3L19 7H15C15 7 14 7 14 8V11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M8 21L5 17H9C9 17 10 17 10 16V13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>{{ t('dataset.refresh') }}</span>
        </button>
      </div>
    </div>

    <div class="main-container">
      <div class="directory-panel">
        <div class="directory-header">
          <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 5C3 3.89543 3.89543 3 5 3H9.58579C9.851 3 10.1054 3.10536 10.2929 3.29289L12 5H19C20.1046 5 21 5.89543 21 7V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M7 3V5C7 6.10457 7.89543 7 9 7H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <h3>{{ t('dataset.directoryTitle') }}</h3>
          <div class="dataset-count">{{ t('dataset.filesCount', { count: totalFiles }) }}</div>
        </div>

        <div class="dataset-list">
          <div v-for="dataset in datasets" :key="dataset.id" class="dataset-folder">
            <div class="folder-header" @click="toggleFolder(dataset.id)">
              <div class="folder-info">
                <svg class="folder-icon" :class="{ rotated: expandedFolders[dataset.id] }" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 5C3 3.89543 3.89543 3 5 3H9.58579C9.851 3 10.1054 3.10536 10.2929 3.29289L12 5H19C20.1046 5 21 5.89543 21 7V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5Z" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M7 3V5C7 6.10457 7.89543 7 9 7H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <div class="folder-name">
                  <span class="species">{{ dataset.species }}</span>
                  <span class="version">{{ dataset.version }}</span>
                </div>
              </div>
              <div class="file-count">{{ t('dataset.filesCount', { count: dataset.fileCount }) }}</div>
            </div>

            <div v-if="expandedFolders[dataset.id]" class="folder-content">
              <div
                v-for="file in dataset.files"
                :key="file.id"
                class="file-item"
                :class="{ active: selectedFile?.id === file.id }"
                @click="selectFile(file)"
              >
                <svg class="file-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 3V7C14 7.55228 14.4477 8 15 8H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M9 13L11 15L15 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H14L19 8V19C19 20.1046 18.1046 21 17 21Z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <div class="file-info">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-meta">
                    <span class="file-type">{{ file.type }}</span>
                    <span class="file-size">{{ formatFileSize(file.size) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-panel">
        <div class="content-header">
          <div class="file-header">
            <div v-if="selectedFile" class="file-title">
              <svg class="file-icon-large" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 3V7C14 7.55228 14.4477 8 15 8H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H14L19 8V19C19 20.1046 18.1046 21 17 21Z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <div class="file-details">
                <h3>{{ selectedFile.name }}</h3>
                <div class="file-meta-large">
                  <span class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    {{ selectedFile.type }}
                  </span>
                  <span class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 9H21M9 21V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    {{ formatFileSize(selectedFile.size) }}
                  </span>
                  <span class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
                    </svg>
                    {{ t('dataset.lastUpdated') }}: {{ selectedFile.updated }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="empty-title">
              <svg class="empty-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 3V7C14 7.55228 14.4477 8 15 8H19" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H14L19 8V19C19 20.1046 18.1046 21 17 21Z" stroke="#94a3b8" stroke-width="1.5"/>
              </svg>
              <h3>{{ t('dataset.selectToView') }}</h3>
            </div>
          </div>

          <div class="action-buttons">
            <button class="action-btn download-btn" @click="download_File" :disabled="!selectedFile">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3V16M12 16L8 12M12 16L16 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20 21H4C3.44772 21 3 20.5523 3 20V16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>{{ t('dataset.download') }}</span>
            </button>
          </div>
        </div>

        <div class="content-display">
          <div v-if="selectedFile" class="file-content">
            <div class="content-tabs">
              <div class="tab" :class="{ active: contentTab === 'preview' }" @click="contentTab = 'preview'">
                <svg class="tab-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2 12C2 12 5.63636 4 12 4C18.3636 4 22 12 22 12C22 12 18.3636 20 12 20C5.63636 20 2 12 2 12Z" stroke="currentColor" stroke-width="1.5"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <span>{{ t('dataset.preview') }}</span>
              </div>
              <div class="tab" :class="{ active: contentTab === 'stats' }" @click="contentTab = 'stats'">
                <svg class="tab-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 10H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M3 18H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M3 6H21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M7 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M12 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M17 3V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span>{{ t('dataset.stats') }}</span>
              </div>
            </div>

            <div class="content-area">
              <div v-if="contentTab === 'preview'" class="preview-content">
                <div class="fasta-preview">
                  <div class="fasta-header">
                    <span class="fasta-header-icon">></span>
                    <span class="fasta-header-text">{{ previewData.header || t('dataset.missingFastaHeader') }}</span>
                  </div>
                  <div class="fasta-sequence">
                    <div
                      v-for="(char, index) in previewData.sequence"
                      :key="index"
                      class="nucleotide"
                      :class="getNucleotideClass(char)"
                    >
                      {{ char }}
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="contentTab === 'stats'" class="stats-content">
                <div class="stats-grid">
                  <div class="stat-card">
                    <div class="stat-header">
                      <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="white" stroke-width="2"/>
                          <path d="M12 6V12L16 14" stroke="white" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                      </div>
                      <div class="stat-info">
                        <div class="stat-title">{{ t('dataset.statSeqCount') }}</div>
                        <div class="stat-subtitle">{{ t('dataset.statSeqCountSub') }}</div>
                      </div>
                    </div>
                    <div class="stat-value">{{ selectedFile.recordCount || 0 }}</div>
                  </div>

                  <div class="stat-card">
                    <div class="stat-header">
                      <div class="stat-icon" style="background: linear-gradient(135deg, #10b981 0%, #047857 100%);">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M8 13L12 17L20 9" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M3 12C3 12 5.63636 4 12 4C18.3636 4 22 12 22 12C22 12 18.3636 20 12 20C5.63636 20 3 12 3 12Z" stroke="white" stroke-width="2"/>
                        </svg>
                      </div>
                      <div class="stat-info">
                        <div class="stat-title">{{ t('dataset.statAvgLength') }}</div>
                        <div class="stat-subtitle">{{ t('dataset.statAvgLengthSub') }}</div>
                      </div>
                    </div>
                    <div class="stat-value">{{ selectedFile.avgLength || 0 }}</div>
                  </div>

                  <div class="stat-card">
                    <div class="stat-header">
                      <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </div>
                      <div class="stat-info">
                        <div class="stat-title">{{ t('dataset.statFileSize') }}</div>
                        <div class="stat-subtitle">{{ t('dataset.statFileSizeSub') }}</div>
                      </div>
                    </div>
                    <div class="stat-value">{{ formatFileSize(selectedFile.size) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-content">
            <svg class="empty-content-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 17L9 19C9 20.1046 9.89543 21 11 21H19C20.1046 21 21 20.1046 21 19V11C21 9.89543 20.1046 9 19 9H17" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M15 9H5C3.89543 9 3 8.10457 3 7V5C3 3.89543 3.89543 3 5 3H13C14.1046 3 15 3.89543 15 5V15C15 16.1046 14.1046 17 13 17H11" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <div class="empty-content-text">{{ t('dataset.emptyText') }}</div>
            <div class="empty-content-subtext">{{ t('dataset.emptySubText') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchDatasets, fetchFilePreview } from '@/api/dataset'
import { formatFileSize } from '@/utils/format'
import { baseURL } from '@/api/index'
import { useI18n } from '../../i18n'

const { t } = useI18n()
const expandedFolders = ref({})

const datasets = ref([])
const selectedFile = ref(null)
const previewData = ref({
  sequence: '',
  header: ''
})

const contentTab = ref('preview')

onMounted(async () => {
  try {
    const res = await fetchDatasets()
    datasets.value = res.data

    datasets.value.forEach(d => {
      expandedFolders.value[d.id] = false
    })
  } catch (err) {
    console.error('load datasets failed', err)
  }
})

const totalFiles = computed(() => datasets.value.reduce((sum, dataset) => sum + dataset.fileCount, 0))

function toggleFolder(folder) {
  expandedFolders.value[folder] = !expandedFolders.value[folder]
}

async function selectFile(file) {
  selectedFile.value = file
  previewData.value = {
    sequence: '',
    header: ''
  }

  if (file.type === 'GFF3') return

  try {
    const res = await fetchFilePreview(file.id)
    previewData.value = res.data.preview
  } catch (err) {
    console.error('preview failed', err)
  }
}

async function refreshData() {
  try {
    const res = await fetchDatasets()
    datasets.value = res.data

    datasets.value.forEach(d => {
      if (!(d.id in expandedFolders.value)) {
        expandedFolders.value[d.id] = false
      }
    })
  } catch (err) {
    console.error('refresh datasets failed', err)
  }
}

function download_File() {
  if (!selectedFile.value) return

  const a = document.createElement('a')
  a.href = `${baseURL}/datasets/files/${selectedFile.value.id}/download/`
  a.download = selectedFile.value.name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

function getNucleotideClass(char) {
  const upperChar = char.toUpperCase()
  switch (upperChar) {
    case 'A': return 'nucleotide-a'
    case 'C': return 'nucleotide-c'
    case 'G': return 'nucleotide-g'
    case 'T': return 'nucleotide-t'
    default: return 'nucleotide-other'
  }
}
</script>
<style scoped>
.dataset-view-list {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  padding: 0 4px;
}

/* 鎿嶄綔鎸夐挳 */
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

/* 涓诲鍣細鍙屾爮甯冨眬 */
.main-container {
  display: flex;
  gap: 4px;
  flex: 1;
  min-height: 0;
}

/* 宸︿晶鐩綍闈㈡澘 */
.directory-panel {
  width: 360px;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 鐩綍澶撮儴 */
.directory-header {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
}

.directory-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.directory-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  flex: 1;
}

.dataset-count {
  font-size: 14px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 500;
}



/* 鏁版嵁闆嗗垪琛?*/
.dataset-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px 16px;
}

/* 鏁版嵁闆嗘枃浠跺す */
.dataset-folder {
  margin-top: 16px;
}

.folder-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.folder-header:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.folder-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.folder-icon {
  width: 20px;
  height: 20px;
  color: #f59e0b;
  transition: transform 0.3s ease;
}

.folder-icon.rotated {
  transform: rotate(90deg);
}

.folder-name {
  display: flex;
  flex-direction: column;
}

.species {
  font-weight: 600;
  color: #1e293b;
  font-size: 15px;
}

.version {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.file-count {
  font-size: 13px;
  color: #64748b;
  background: #ffffff;
  padding: 4px 10px;
  border-radius: 10px;
  font-weight: 500;
}

/* 鏂囦欢澶瑰唴瀹?*/
.folder-content {
  margin-top: 8px;
  padding-left: 32px;
}

/* 鏂囦欢椤?*/
.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin: 4px 0;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.file-item:hover {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.file-item.active {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
}

.file-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  flex-shrink: 0;
}

.file-item.active .file-icon {
  color: #3b82f6;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  color: #1e293b;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.file-type {
  font-size: 12px;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 8px;
}

.file-size {
  font-size: 12px;
  color: #94a3b8;
}

/* 鍙充晶鍐呭闈㈡澘 */
.content-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 鍐呭澶撮儴 */
.content-header {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.file-header {
  flex: 1;
}

.file-title {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.file-icon-large {
  width: 40px;
  height: 40px;
  color: #3b82f6;
  flex-shrink: 0;
  margin-top: 4px;
}

.file-details h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  word-break: break-all;
}

.file-meta-large {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #64748b;
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: #94a3b8;
}

.empty-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  width: 40px;
  height: 40px;
  color: #94a3b8;
}

.empty-title h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #94a3b8;
}

/* 鎿嶄綔鎸夐挳 */
.action-buttons {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.download-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
}

.download-btn:not(:disabled):hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
}

/* 鍐呭灞曠ず鍖哄煙 */
.content-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.file-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* 鍐呭鏍囩椤?*/
.content-tabs {
  display: flex;
  gap: 4px;
  padding: 20px 24px 0;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
}

.tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 12px 12px 0 0;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.tab:hover {
  background: #f8fafc;
  color: #475569;
}

.tab.active {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  color: #1e293b;
  border-bottom-color: #3b82f6;
  font-weight: 600;
}

.tab-icon {
  width: 18px;
  height: 18px;
}

/* 鍐呭鍖哄煙 */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* 棰勮鍐呭 */
.preview-content {
  height: 100%;
}

.fasta-preview {
  background: #f8fafc;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.fasta-header {
  padding: 16px 20px;
  background: linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%);
  border-bottom: 1px solid #e2e8f0;
  font-family: 'Courier New', monospace;
  color: #2563eb;
}

.fasta-header-icon {
  font-weight: bold;
  margin-right: 8px;
}

/* 搴忓垪鏄剧ず */
.fasta-sequence {
  flex: 1;
  padding: 20px;
  font-family: 'Courier New', monospace;
  font-size: 15px;
  line-height: 1.8;
  word-break: break-all;
  color: #1e293b;
  background: #ffffff;
  overflow-y: auto;
  max-height: 500px;
}

/* 鏍歌嫹閰告牱寮?*/
.nucleotide {
  display: inline-block;
  font-weight: 300;
  margin: 0 1px;
}

/* 涓嶅悓鏍歌嫹閰哥殑棰滆壊 */
.nucleotide-a {
  color: #c81e1e; /* 涓瓑绾㈣壊锛屼笉鍒虹溂 */
}

.nucleotide-c {
  color: #1d4ed8; /* 涓瓑钃濊壊锛屼笓涓氭劅 */
}

.nucleotide-g {
  color: #047857; /* 涓瓑缁胯壊锛岃垝閫?*/
}

.nucleotide-t {
  color: #b45309; /* 涓瓑姗欒壊锛屾俯鍜?*/
}

.nucleotide-other {
  color: #898989; /* 鐏拌壊 - 鍏朵粬 */
}



/* 鍘熷鏁版嵁 */
.raw-content {
  height: 100%;
}

.raw-text {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  background: #f8fafc;
  padding: 20px;
  border-radius: 16px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  max-height: 500px;
  overflow-y: auto;
}

/* 缁熻鍐呭 */
.stats-content {
  height: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e2e8f0;
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-subtitle {
  font-size: 14px;
  color: #64748b;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  text-align: center;
  font-family: 'Courier New', monospace;
}

/* 绌虹姸鎬?*/
.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 64px 32px;
}

.empty-content-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  color: #cbd5e1;
}

.empty-content-text {
  font-size: 18px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 8px;
  text-align: center;
}

.empty-content-subtext {
  font-size: 14px;
  color: #cbd5e1;
  text-align: center;
}

/* 鍝嶅簲寮忚璁?*/
@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
    height: auto;
  }
  
  .directory-panel {
    width: 100%;
    height: 400px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  
  .content-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .action-btn {
    flex: 1;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .file-meta-large {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
