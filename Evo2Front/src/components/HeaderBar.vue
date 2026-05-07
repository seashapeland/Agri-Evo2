<template>
  <div class="header">
    <div class="logo">
      <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z"
          fill="url(#gradient)"
        />
        <path d="M12 6L15 9L12 12L9 9L12 6Z" fill="white" />
        <path d="M6 12L9 15L12 12L9 9L6 12Z" fill="white" />
        <path d="M12 12L15 15L18 12L15 9L12 12Z" fill="white" />
        <path d="M12 18L9 15L12 12L15 15L12 18Z" fill="white" />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#667eea" />
            <stop offset="100%" stop-color="#764ba2" />
          </linearGradient>
        </defs>
      </svg>
      <div class="title">
        <span class="title-main">Agri-Evo2</span>
        <span class="title-sub">{{ t('header.subtitle') }}</span>
      </div>
    </div>

    <div class="header-actions">
      <button
        class="lang-switch manual-download"
        type="button"
        :title="manualTitle"
        @click="downloadManual"
      >
        <svg class="lang-icon manual-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path
            d="M8.5 10.5L12 14L15.5 10.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path d="M5 18H19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>
        <span class="manual-text">{{ manualText }}</span>
      </button>

      <button class="lang-switch" type="button" :title="t('header.switchLanguage')" @click="toggleLocale">
        <svg class="lang-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
          <path d="M3.6001 9H20.4001" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path d="M3.6001 15H20.4001" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path
            d="M12 3C10.2094 5.07169 9.19238 8.00043 9.19238 12C9.19238 16.003 10.2103 18.9312 12 21"
            stroke="currentColor"
            stroke-width="1.5"
          />
          <path
            d="M12 3C13.7906 5.07169 14.8076 8.00043 14.8076 12C14.8076 16.003 13.7897 18.9312 12 21"
            stroke="currentColor"
            stroke-width="1.5"
          />
        </svg>
        <span class="lang-code">{{ isZh ? '中' : 'EN' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../i18n'

const { t, isZh, toggleLocale } = useI18n()

const manualHref = computed(() =>
  isZh.value ? '/manuals/cau-evo2-manual-zh.md' : '/manuals/cau-evo2-manual-en.md'
)
const manualDownloadName = computed(() =>
  isZh.value ? 'CAU-Evo2-功能手册.md' : 'CAU-Evo2-User-Manual.md'
)
const manualText = computed(() => (isZh.value ? '功能手册' : 'Manual'))
const manualTitle = computed(() => (isZh.value ? '下载功能手册' : 'Download user manual'))

function downloadManual() {
  if (typeof document === 'undefined') return
  const a = document.createElement('a')
  a.href = manualHref.value
  a.download = manualDownloadName.value
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
</script>

<style scoped>
.header {
  height: 64px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  filter: drop-shadow(0 2px 4px rgba(102, 126, 234, 0.2));
  transition: transform 0.3s ease;
}

.logo:hover .logo-icon {
  transform: scale(1.05);
}

.title {
  display: flex;
  flex-direction: column;
  line-height: 1.4;
}

.title-main {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.title-sub {
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  letter-spacing: 0.5px;
}

.header-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.manual-download,
.lang-switch {
  height: 34px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background: #f8fafc;
  color: #334155;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.manual-download {
  min-width: 100px;
}

.lang-switch {
  min-width: 72px;
}

.manual-download:hover,
.lang-switch:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.manual-download:active,
.lang-switch:active {
  transform: translateY(1px);
}

.manual-icon,
.lang-icon {
  width: 16px;
  height: 16px;
}

.manual-text,
.lang-code {
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
}
</style>
