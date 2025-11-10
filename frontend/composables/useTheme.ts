import { computed } from 'vue'

const THEME_STORAGE_KEY = 'theme_mode'

export const useTheme = () => {
  const isDark = useState<boolean>('theme.isDark', () => false)
  const initialized = useState<boolean>('theme.initialized', () => false)

  const theme = computed(() => isDark.value ? 'dark' : 'light')

  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
    saveTheme()
  }

  const setTheme = (mode: 'light' | 'dark') => {
    isDark.value = mode === 'dark'
    applyTheme()
    saveTheme()
  }

  const applyTheme = () => {
    if (typeof document === 'undefined') return

    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  const saveTheme = () => {
    if (typeof window === 'undefined') return
    window.localStorage.setItem(THEME_STORAGE_KEY, isDark.value ? 'dark' : 'light')
  }

  const initializeTheme = () => {
    if (initialized.value) return
    initialized.value = true

    if (typeof window === 'undefined') return

    const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY)

    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }

    applyTheme()
  }

  initializeTheme()

  return {
    isDark,
    theme,
    toggleTheme,
    setTheme,
    initializeTheme
  }
}
